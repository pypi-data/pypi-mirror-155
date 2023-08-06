import io
import os
import tarfile
import time
from abc import ABC, abstractmethod
from contextlib import contextmanager
from itertools import filterfalse
from pathlib import Path
from typing import List, Iterable, IO, Sequence, Union, Optional, Generator

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from libbiomedit.archive import archive_reader

from .error import UserError
from .filesystem import delete_files
from ..utils.progress import ProgressInterface, with_progress

tarfile.DEFAULT_FORMAT = tarfile.PAX_FORMAT

METADATA_FILE = "metadata.json"
METADATA_FILE_SIG = "metadata.json.sig"
CHECKSUM_FILE = "checksum.sha256"
DATA_ARCHIVE = "data.tar.gz"
DATA_FILE_ENCRYPTED = DATA_ARCHIVE + ".gpg"
PACKAGE_CONTENT = {
    METADATA_FILE: "'{}' file with metadata",
    METADATA_FILE_SIG: "'{}' file with a detached signature of the metadata",
    DATA_FILE_ENCRYPTED: "'{}' file with the encrypted data",
}
CONTENT_FOLDER = "content"
EXACTNESS_MSG = (
    "BioMedIT input archive files MUST EXACTLY contain following files:\n"
    + "\n".join(
        ["  - " + template.format(entry) for entry, template in PACKAGE_CONTENT.items()]
    )
)


def check_package(path: str) -> None:
    """Check package (path) file name extension and content.

    Package must be a .zip or .tar archive and contain exactly one .json and
    one .tar.gz.gpg file.

    :param path: path to the archive file to check.
    :raises UserError:
    """
    path = os.path.realpath(path)
    try:
        with archive_reader(path) as archive:
            content = archive.namelist()
    except TypeError as e:
        raise UserError(e) from e
    if not content:
        raise UserError(f"Input archive '{path}' is empty.")
    assert_relative(content)
    diff = PACKAGE_CONTENT.keys() - set(content)
    if diff:
        raise UserError(
            f"Input file '{path}' has non-compliant content.\n"
            "Following files are missing:\n  - '"
            + "'\n  - '".join(diff)
            + "'\n\n"
            + EXACTNESS_MSG
        )
    diff = set(content) - PACKAGE_CONTENT.keys()
    if diff:
        raise UserError(
            f"Input archive '{path}' has non-compliant content.\n"
            "Following files are NOT part of the specification and are rejected:\n  - '"
            + "'\n  - '".join(diff)
            + "'\n\n"
            + EXACTNESS_MSG
        )


class ArchiveFileBase(ABC):
    def __init__(self, archive_path: str):
        self.archive_path = archive_path

    @abstractmethod
    def add_to_tar(self, tar: tarfile.TarFile) -> None:
        pass


class ArchiveInMemoryFile(ArchiveFileBase):
    """An ArchiveFileBase whose content_container is a bytes instance."""

    def __init__(self, archive_path: str, content_container: bytes):
        super().__init__(archive_path)
        self.content_container = content_container

    def add_to_tar(self, tar: tarfile.TarFile) -> None:
        t = tarfile.TarInfo(self.archive_path)
        t.size = len(self.content_container)
        t.mtime = int(time.time())
        tar.addfile(t, io.BytesIO(self.content_container))


class ArchiveFile(ArchiveFileBase):
    """An ArchiveFileBase whose content_container is a file like object."""

    def __init__(self, archive_path: str, content_container: IO[bytes]):
        super().__init__(archive_path)
        self.content_container = content_container

    def add_to_tar(self, tar: tarfile.TarFile) -> None:
        t = tar.gettarinfo(
            name=self.content_container.name, arcname=self.archive_path, fileobj=None
        )
        with self.content_container as f_opened:
            tar.addfile(t, f_opened)


def write_tar(
    content: Sequence[ArchiveFileBase],
    output: Union[str, IO[bytes]],
    compress_level: int = 6,
    compress_algo: str = "gz",
) -> None:
    """Create a ".tar" or ".tar.gz" archive from files on disk or from a
    data stream, i.e. in-memory files.

    :param content: (in-memory) files to be added to the tar archive.
    :param output: path (or file object) or stream for the output tarball.
    :param compress_algo: compression algorithm to use when compressing
        the tar file (if compress_level > 0). Possible choices are
        'gz' (for gzip compression) and 'bz2' (for bzip2 compression).
    :param compress_level: gzip/bzip2 compression level in the range 0 (no
        compression) to 9 (highest compression).
    :raises UserError:
    """

    # Create a TypedDict class so that the mypy linter does not complain
    # about "Incompatible types in assignment".
    class TarfileArguments(TypedDict, total=False):
        name: str
        fileobj: IO[bytes]
        mode: str
        compresslevel: int

    archive_file_names = set(f.archive_path for f in content)
    assert_relative(archive_file_names)

    # Set correct mode depending on compression level and type of output,
    # i.e. file vs fileobject.
    # Note that currently the "w|gz" mode do not support the "compresslevel"
    # argument, so we use "w:gz" instead.
    tarfile_arguments: TarfileArguments = {
        "mode": f"w:{compress_algo}"
        if compress_level > 0
        else "w"
        if isinstance(output, str)
        else "w|"
    }
    if isinstance(output, str):
        tarfile_arguments["name"] = output
    else:
        tarfile_arguments["fileobj"] = output
    tarfile_arguments["mode"] = (
        f"w:{compress_algo}"
        if compress_level > 0
        else "w"
        if isinstance(output, str)
        else "w|"
    )
    if compress_level > 0:
        tarfile_arguments["compresslevel"] = compress_level

    # Compress input files into tarball.
    with tarfile.open(**tarfile_arguments) as tar:
        for archive_file in content:
            archive_file.add_to_tar(tar)

    if isinstance(output, str):
        # Verify the tarball file was created correctly. If not, delete it.
        if not Path(output).is_file():
            raise UserError(
                f"compression failed for [{output}]: " f"tarball not created."
            )
        with tarfile.open(output, "r") as tar:
            missing_files = {Path(p) for p in archive_file_names} - {
                Path(p) for p in tar.getnames()
            }
        if missing_files:
            delete_files(output)
            raise UserError(
                f"compression failed for [{output}]: "
                f"one or more files are missing in tarball."
            )


def is_relative(path: str) -> bool:
    return not (os.path.isabs(path) or os.path.normpath(path).startswith(".."))


def assert_relative(files: Iterable[str]) -> None:
    """Asserts that each path in the list is relative"""
    non_relative = [f for f in files if not is_relative(f)]
    if non_relative:
        raise UserError(
            "The archive contains files with absolute path or paths ending "
            "in a parent directory:\n" + "\n".join(non_relative)
        )


def check_extracted(paths: Iterable[str]) -> None:
    """Tests if all paths in :paths: exist now on the file system"""
    failed = tuple(filterfalse(os.path.exists, paths))
    if failed:
        raise UserError("Failed to extract to following files: \n" + "\n".join(failed))


@contextmanager
def extract_with_progress(
    path: str, progress: Optional[ProgressInterface], member_path: str
) -> Generator[IO[bytes], None, None]:
    """Extracts given files from given archive.

    If only one file is specified, then progression scales with extracting of
    this specific file. Otherwise, each file takes an equal part (independent
    of its size) to progression.

    :param path: path to the archive file.
    :param progress: the ProgressInterface. Must be specified.
    :param member_path: the tar member we want to extract.
    :raises UserError: if a 'KeyError' is thrown
    :returns: yields an io.BufferedReader or a casted 'FileObjectProgress'
    """
    with archive_reader(path) as archive:
        try:
            member = archive.extract_member(member_path)
            yield with_progress(member, progress)
        except KeyError as e:
            raise UserError(f"In archive {path}: {e}") from e


@contextmanager
def extract(path: str, member_path: str) -> Generator[IO[bytes], None, None]:
    with archive_reader(path) as archive:
        try:
            yield archive.extract_member(member_path)
        except KeyError as e:
            raise UserError(f"In archive {path}: {e.args[0]}") from e


@contextmanager
def extract_multiple(
    path: str, member_paths: Iterable[str]
) -> Generator[Iterable[IO[bytes]], None, None]:
    with archive_reader(path) as archive:
        try:
            yield (archive.extract_member(file_name) for file_name in member_paths)
        except KeyError as e:
            raise UserError(f"In archive {path}: {e.args[0]}") from e


def unpack_from_stream(
    archive: IO[bytes], dest: str, content: List[str], mode: str = "r|*"
) -> None:
    """Extract all files in the tarball from a stream.
    After unpacking the function checks that all files have been properly
    extracted by comparing the new files on disk to the list of files present
    in the tarball.

    :param archive: tarball stream
    :param dest: destination directory for the unpacked data
    :param content: a list container to store the file names compressed in
        the tarball
    :param mode: Mode to be passed to tarfile, i.e. `'r|*'`
    """
    if not os.path.isdir(dest):
        os.makedirs(dest)
    with tarfile.open(mode=mode, fileobj=archive) as tar:
        for f in tar:
            assert_relative((f.name,))
            content.append(f.name)
            tar.extract(f, dest)
    check_extracted((os.path.join(dest, f) for f in content))
