import io
import json
import os
from pathlib import Path
from datetime import datetime
from functools import partial
from typing import List, Optional, Callable, Tuple, Iterable, Any, TypeVar
from zipfile import ZipFile, ZipInfo, ZIP_STORED

from ..core import gpg
from ..core.archive import (
    write_tar,
    ArchiveInMemoryFile,
    ArchiveFile,
    ArchiveFileBase,
    METADATA_FILE,
    METADATA_FILE_SIG,
    DATA_FILE_ENCRYPTED,
    CHECKSUM_FILE,
    CONTENT_FOLDER,
)
from ..core.filesystem import (
    delete_file_on_error,
    get_compression_stats,
    get_total_size,
    search_files_recursively,
    check_file_read_permission,
    check_space,
)
from ..core.crypt import (
    enforce_passphrase,
    retrieve_refresh_and_validate_keys,
    encrypt_and_sign,
    detach_sign_file,
    check_password,
    search_priv_key,
)
from ..core.checksum import generate_checksums_file_content, compute_checksum_on_write
from ..core.error import UserError
from ..core.metadata import MetaData, alnum_str, Purpose, HexStr1024, HexStr256
from ..core.secret import Secret
from ..utils.progress import ProgressInterface, subprogress, progress_file_iter
from ..utils.config import Config
from ..utils.log import create_logger, log_runtime_info, log_timing

DATE_FMT_FILENAME = "%Y%m%dT%H%M%S"
logger = create_logger(__name__)


def check_path(
    directory: bool = False, writable: bool = False
) -> Callable[[str], None]:
    """Generate a 'type definition' function that will check that a string is
    a valid path (file or directory).

    :param directory: if True, the path must be a directory.
    :param writable: if True, the user must have write access to the path.
    :returns: type check function.
    :raises ValueError:
    """

    def _check_path(path_to_check: str) -> None:
        path = Path(path_to_check)
        if not path.exists():
            raise ValueError(f"Invalid path: '{path_to_check}'. Path does not exist.")
        if directory and not path.is_dir():
            raise ValueError(
                f"Invalid path: '{path_to_check}'. Path is not a directory."
            )
        if writable and not os.access(path.as_posix(), os.W_OK):
            raise ValueError(f"Invalid path: '{path_to_check}'. Path is not writable.")

    return _check_path


def check_integer_in_range(min_value: int, max_value: int) -> Callable[[Any], None]:
    """Generate a function which checks that:
    * Its input value is an integer.
    * Its input value is in the range [min_value:max_value].
    """

    def _integer_in_range(value_to_check: Any) -> None:
        try:
            value_to_check = int(value_to_check)
        except (ValueError, TypeError) as e:
            raise ValueError("Value must be an integer") from e

        if value_to_check < min_value or value_to_check > max_value:
            raise ValueError(f"Value must be in the range: [{min_value}-{max_value}]")

    return _integer_in_range


def check_paths_on_posix(paths: Iterable[str]) -> None:
    """If the machine is POSIX, verify that the specified input path(s) do not
    contain any windows-style separators (i.e. \\).
    """

    for path in paths:
        if os.path.sep == "/" and "\\" in path:
            raise UserError(
                "On POSIX systems (this machine), backslashes are NOT allowed "
                f"as path separators. Offending value is [{path}]."
            )


check_compression_level = check_integer_in_range(min_value=0, max_value=9)


@log_timing(logger)
@log_runtime_info(logger)
def encrypt(  # pylint: disable=too-many-statements
    files: List[str],
    *,
    config: Config,
    recipient: List[str],
    dtr_id: Optional[int] = None,
    sender: Optional[str] = None,
    passphrase: Optional[Secret[str]] = None,
    output: Optional[str] = None,
    output_suffix: Optional[str] = None,
    dry_run: bool = False,
    verify_dtr: bool = True,
    force: bool = False,
    compression_level: Optional[int] = None,
    purpose: Optional[Purpose] = None,
    progress: Optional[ProgressInterface] = None,
) -> Optional[str]:
    """Compress and encrypt files and/or directories.

    Main function of the encryption workflow. It compresses the input files
    into a single archive file, which is then encrypted for the specified
    recipients and signed by the specified sender.

    Finally, the encrypted data is bundled with a metadata file in a single
    .zip archive.

    The function returns the file name of the created data package.
    """

    with logger.log_task(
        f"Input data verification{' (dry_run)' if dry_run else ''}..."
    ):

        # Verify user has specified at least 1 file to encrypt and that the
        # file(s) have read permission for the user.
        logger.info("Verify files to encrypt")
        if not files:
            raise UserError("Empty file list.")
        files_to_encrypt = list(search_files_recursively(files))
        if not files_to_encrypt:
            raise UserError(
                "No input files found. Did you try encrypting an empty directory?"
            )
        check_file_read_permission(files_to_encrypt)

        # If no sender is specified, retrieve default sender from config.
        if sender is None:
            sender = config.default_sender or config.gpg_store.default_key()
            if sender is None:
                raise UserError("Sender not specified with no default sender.")

        # If no compression level is specified, retrieve it from config.
        if compression_level is None:
            compression_level = config.compression_level
        check_arg_value(
            arg_value=compression_level,
            arg_name="compression level",
            arg_type_checker=check_compression_level,
        )

        # Retrieve the sender's public and private keys, as well as the
        # recipient's public key:
        #  - sender private key: needed to sign the encrypted data.
        #  - sender public key : will be checked to make sure it is signed by
        #       the DCC. Only private keys with a matching public key that is
        #       signed by the DCC will be allowed to be used.
        #  - recipient public key: needed to encrypt the data.
        #
        # The sender/recipient information can be either an email, a keyID or
        # a full fingerprint.
        logger.info("Retrieve sender and recipient GnuPG keys")
        sender_pub_key, *recipients_pub_key = retrieve_refresh_and_validate_keys(
            key_search_terms=(sender, *recipient),
            gpg_store=config.gpg_store,
            key_authority_fingerprint=config.key_authority_fingerprint,
            keyserver_url=config.keyserver_url,
            validate_key_origin=False,
            allow_key_download=config.allow_gpg_key_autodownload,
        )

        # Verify a private key matching the user's public key exists. The key
        # itself is not needed because it shares the fingerprint with the
        # public key.
        search_priv_key(sender_pub_key.fingerprint, config.gpg_store)
        logger.info(
            "Sender: %s",
            f"{sender_pub_key.uids[0]} ({sender_pub_key.fingerprint})",
        )
        logger.info(
            "Recipients: %s",
            ", ".join(
                f"{key.uids[0]} ({key.fingerprint})" for key in recipients_pub_key
            ),
        )

        # If requested, verify data transfer related information.
        if verify_dtr:
            logger.info("Verify Data Transfer ID")
            # Connect to the portal API to retrieve the code (abbreviation)
            # associated with the DTR ID.
            project_code = verify_dtr_info_and_get_project_code(
                dtr_id, purpose, config, sender_pub_key, recipients_pub_key
            )
            logger.info("DTR ID '%s' is valid for project '%s'", dtr_id, project_code)
        else:
            project_code = None

        logger.info("Verify available disk space")
        # The default value for the output name is based on date and time
        # when the script is being run.
        # Example output name: "20191011T145012.zip".
        timestamp = datetime.now().astimezone()
        output_name = generate_output_archive_name(
            prefix=project_code,
            timestamp=timestamp,
            suffix=output_suffix or config.package_name_suffix,
            dir_or_name_override=output,
        )
        total_input_file_size = get_total_size(files_to_encrypt)
        check_space(total_input_file_size, os.path.dirname(output_name), force=force)

        # Create a list of file paths (i.e. the files to package) as they will
        # appear in the output archive file. For this we start by retrieving
        # the lowest common directory of all input files/directories.
        root_dir = os.path.commonpath(
            [Path(x).absolute().parent.as_posix() for x in files]
        )
        archive_paths = [
            os.path.join(CONTENT_FOLDER, os.path.relpath(f, start=root_dir))
            for f in files_to_encrypt
        ]
        check_paths_on_posix(archive_paths)

        # If the user asked to sign the data, check that the GPG key password
        # is correct.
        if config.sign_encrypted_data and not dry_run:
            logger.info("Verify data sender GPG password")
            check_password(
                password=enforce_passphrase(passphrase),
                key_fingerprint=sender_pub_key.fingerprint,
                gpg_store=config.gpg_store,
            )

    if dry_run:
        logger.info("Dry run completed successfully")
        return None

    with logger.log_task("Compute sha256 checksum on input files..."):
        # Write input file checksums to a file that will be added to the
        # encrypted .tar.gz archive. This information must be encrypted as
        # file names sometimes contain information about their content.
        checksums = generate_checksums_file_content(
            zip(archive_paths, files_to_encrypt),
            # `max_workers` accepts only None and positive integers. Make
            # sure that zero and negative values are converted into None.
            max_workers=config.max_cpu if config.max_cpu > 0 else None,
        )
        if progress is not None:
            progress.update(0.1)

    with logger.log_task("Compress and encrypt input data [this can take a while]..."):
        # Encryption is done with the recipient's public key and the optional
        # signing with the user's (i.e sender) private key. The user's private
        # key passphrase is needed to sign the encrypted file.
        encrypted_checksum_buf = io.StringIO()
        with delete_file_on_error(output_name), ZipFile(
            output_name, mode="w", compression=ZIP_STORED
        ) as zip_obj:
            with subprogress(progress, step_completion_increase=0.9) as scaled_progress:
                # Create a tar archive containing all input files
                archive_content: Tuple[ArchiveFileBase, ...] = (
                    ArchiveInMemoryFile(CHECKSUM_FILE, checksums),
                ) + tuple(
                    ArchiveFile(a_path, f)
                    for a_path, f in zip(
                        archive_paths,
                        progress_file_iter(
                            files=files_to_encrypt, mode="rb", progress=scaled_progress
                        ),
                    )
                )
                with zip_obj.open(
                    ZipInfo(DATA_FILE_ENCRYPTED, date_time=timestamp.timetuple()[:6]),
                    mode="w",
                    force_zip64=True,
                ) as fout:
                    encrypt_and_sign(
                        source=partial(
                            write_tar,
                            archive_content,
                            compress_level=compression_level,
                            compress_algo="gz",
                        ),
                        output=partial(
                            compute_checksum_on_write,
                            fout=fout,
                            checksum_buffer=encrypted_checksum_buf,
                        ),
                        gpg_store=config.gpg_store,
                        recipients_fingerprint=[
                            key.fingerprint for key in recipients_pub_key
                        ],
                        signature_fingerprint=sender_pub_key.fingerprint
                        if config.sign_encrypted_data
                        else None,
                        passphrase=enforce_passphrase(passphrase)
                        if config.sign_encrypted_data
                        else None,
                        always_trust=config.always_trust_recipient_key,
                    )
                encrypted_checksum = encrypted_checksum_buf.read()

            logger.info("Generating metadata")
            # Create a dictionary with all the info we want to store in the
            # .json file, then pass this dictionary to json.dump that will
            # convert it to a json file.
            # Use indent=4 to make the output file easier on the eye.
            metadata = MetaData(
                transfer_id=dtr_id,
                sender=HexStr1024(sender_pub_key.fingerprint),
                recipients=[HexStr1024(key.fingerprint) for key in recipients_pub_key],
                purpose=purpose,
                checksum=HexStr256(encrypted_checksum),
                compression_algorithm="gzip" if compression_level > 0 else "",
            )
            metadata_bytes, metadata_signature_bytes = byte_encode_metadata(
                metadata,
                config.gpg_store,
                passphrase,
                sender_pub_key if config.sign_encrypted_data else None,
            )

            in_memory_files = (
                (METADATA_FILE, metadata_bytes),
                (METADATA_FILE_SIG, metadata_signature_bytes),
            )
            for name, contents in in_memory_files:
                zip_obj.writestr(
                    ZipInfo(name, date_time=datetime.utcnow().timetuple()[:6]),
                    contents,
                )

    logger.info(
        "Completed data encryption: %s [%s]",
        output_name,
        get_compression_stats(total_input_file_size, os.path.getsize(output_name)),
    )
    return output_name


T = TypeVar("T")


def check_arg_value(
    arg_value: T,
    arg_name: str,
    arg_type_checker: Callable[[T], Any],
) -> None:
    """Verify that the value of variable arg_value that is named arg_name is
    following type arg_type. arg_type_checker is a function that does a check
    of the type of the variable.
    """
    try:
        arg_type_checker(arg_value)
    except ValueError as e:
        raise UserError(f"Invalid value for argument '{arg_name}': {e}.") from e


def byte_encode_metadata(
    metadata: MetaData,
    gpg_store: gpg.GPGStore,
    passphrase: Optional[Secret[str]],
    sender_pub_key: Optional[gpg.Key],
) -> Tuple[bytes, bytes]:
    """Encodes the provided metadata and creates a detached PGP signature file
    for the metadata if a PGP key (sender_pub_key) is specified.

    The function returns both the metadata and associated detached signature in
    encoded form.
    """
    metadata_bytes = json.dumps(MetaData.asdict(metadata), indent=4).encode()
    metadata_signature_bytes = b""
    if sender_pub_key is not None:
        metadata_signature_bytes = detach_sign_file(
            metadata_bytes,
            sender_pub_key.fingerprint,
            enforce_passphrase(passphrase),
            gpg_store,
        )
    return metadata_bytes, metadata_signature_bytes


def verify_dtr_info_and_get_project_code(
    dtr_id: Optional[int],
    purpose: Optional[Purpose],
    config: Config,
    sender_pub_key: gpg.Key,
    recipients_pub_key: Iterable[gpg.Key],
) -> str:
    """Determine the "code" (i.e. short name) of a project based on its DTR ID
    (Data Transfer ID) and perform some sanity checks on data associated with
    the tranfer by querying the portal API:
     * Verify the data sender's key (sender_pub_key) is authorized.
     * Verify the data recipients' keys (recipients_pub_key) is authorized and
       that the recipient is a DM (data manager) for the project.
     * Verify that the purpose is correct.

    If all these checks complete successfully, the project "code" is returned.
    """

    error_prefix = "Cannot verify DTR (Data Transfer Request) ID"
    if dtr_id is None:
        raise UserError(f"{error_prefix}: 'DTR ID' is missing.")
    if not purpose:
        raise UserError(f"{error_prefix}: 'purpose' is missing.")
    if config.offline:
        raise UserError(f"{error_prefix}: offline mode is on.")
    if not config.portal_api:
        raise UserError(f"{error_prefix}: no portal URL specified in config.")

    try:
        project_code = config.portal_api.verify_transfer(
            metadata=MetaData(
                transfer_id=dtr_id,
                sender=HexStr1024(sender_pub_key.fingerprint),
                recipients=[HexStr1024(key.fingerprint) for key in recipients_pub_key],
                checksum=HexStr256("0" * 64),
                purpose=purpose,
            ),
            filename="missing",
        )
    except RuntimeError as e:
        raise UserError(format(e)) from e
    return project_code


def generate_output_archive_name(
    prefix: Optional[str] = None,
    timestamp: Optional[datetime] = None,
    suffix: Optional[str] = None,
    dir_or_name_override: Optional[str] = None,
) -> str:
    """Generates the path + name of the output archive file of the encrypt
    workflow and verify the user has write access to the output directory.

    By default, the generated output name has the following structure:

        <current work dir>/<prefix>_<date_and_time>_<suffix>.zip

    Where <prefix> and <suffix> are optional and omitted if absent.
    If an override value is passed (dir_or_name_override), it is used as
    output name and/or output directory.

    :param prefix: optional prefix for the output archive file.
    :param timestamp: date and time to be used in archive file name (if no override
        value is passed). If no value is provided, the current time is used.
    :param suffix: optional suffix for the output archive file.
    :param dir_or_name_override: directory, name or directory + name to use
        for the output archive. If this value is None, a default output name
        is generated as explained above.
    :return: path and name of the output archive file.
    :raises UserError:
    """

    # If no timestamp was provided, use the current time instead. Note that
    # we might need this even if dir_or_name_override is provided since at
    # this point we don't know whether the latter is a directory or file name.
    if not timestamp:
        timestamp = datetime.now().astimezone()
    default_name = "_".join(
        filter(None, [prefix, timestamp.strftime(DATE_FMT_FILENAME), suffix])
    )

    if dir_or_name_override is None:
        output_name = default_name
        output_dir = Path.cwd().as_posix()
    else:
        override_path = Path(dir_or_name_override)
        if override_path.is_dir():
            output_name = default_name
            output_dir = os.path.realpath(override_path.as_posix())
        else:
            output_name = override_path.name
            output_dir = os.path.realpath(override_path.parent.as_posix())

    # Add '.zip' extension to output name if needed.
    if not output_name.endswith(".zip"):
        output_name += ".zip"

    # Verify that output name and path follow the conventions. This also
    # verifies that the specified output directory exists and that the user
    # has write access to it.
    check_arg_value(
        output_name,
        "output name",
        alnum_str(min_length=1, max_length=60, allow_dots=True),
    )
    check_arg_value(
        output_dir, "path in output name", check_path(directory=True, writable=True)
    )

    # Return output archive name in posix format.
    return (Path(output_dir) / output_name).as_posix()
