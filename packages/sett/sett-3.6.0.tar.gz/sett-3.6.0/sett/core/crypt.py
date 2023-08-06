import enum
import io
import re
import warnings
from typing import (
    Iterable,
    List,
    Sequence,
    Tuple,
    Optional,
    Union,
    Type,
    IO,
    Callable,
    cast,
    Any,
    TypeVar,
)
from functools import wraps, partial

from libbiomedit import crypt
from . import gpg
from .error import UserError
from .request import urlopen
from .secret import Secret, reveal
from ..utils.config import Config


GPGStore = gpg.GPGStore
ExceptionType = Union[Type[BaseException], Tuple[Type[BaseException], ...]]

R = TypeVar("R")


def to_user_error(
    error_types: ExceptionType,
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """A decorator to turn errors of type :error_types: into UserError"""

    def _to_user_error(f: Callable[..., R]) -> Callable[..., R]:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> R:
            try:
                return f(*args, **kwargs)
            except error_types as e:
                raise UserError(format(e)) from e

        return wrapped

    return _to_user_error


def to_user_error_gen(
    error_types: ExceptionType,
) -> Callable[[Callable[..., Iterable[R]]], Callable[..., Iterable[R]]]:
    """A decorator to turn errors of type :error_types: into UserError"""

    def _to_user_error(f: Callable[..., Iterable[R]]) -> Callable[..., Iterable[R]]:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> Iterable[R]:
            try:
                yield from f(*args, **kwargs)
            except error_types as e:
                raise UserError(format(e)) from e

        return wrapped

    return _to_user_error


validate_pub_key = to_user_error(RuntimeError)(crypt.validate_pub_key)
retrieve_refresh_and_validate_keys = to_user_error_gen((RuntimeError, gpg.GPGError))(
    partial(crypt.retrieve_refresh_and_validate_keys, url_opener=urlopen)
)
fingerprint2keyid = to_user_error(RuntimeError)(crypt.fingerprint2keyid)
verify_metadata_signature = to_user_error(RuntimeError)(
    partial(crypt.verify_metadata_signature, url_opener=urlopen)
)


@to_user_error((gpg.GPGError, gpg.KeyserverError))
def search_keyserver(search_term: str, keyserver: str) -> List[gpg.KeyInfo]:
    """Search keyserver for keys matching the query"""
    return list(gpg.search_keyserver(search_term, keyserver, url_opener=urlopen))


@to_user_error(gpg.GPGError)
def import_keys(key_data: str, gpg_store: GPGStore) -> None:
    """Import keys from text"""
    return gpg_store.import_file(key_data.encode())


@to_user_error(gpg.GPGError)
def delete_pub_keys(fingerprints: List[str], gpg_store: GPGStore) -> None:
    """Delete public key"""
    return gpg_store.delete_pub_keys(*fingerprints)


@to_user_error(gpg.GPGError)
def create_revocation_certificate(
    fingerprint: str, passphrase: str, gpg_store: GPGStore
) -> bytes:
    """Create a revocation certificate for the key"""
    return gpg_store.gen_revoke(fingerprint, passphrase=passphrase)


def verify_key_length(key: gpg.Key, min_key_length: int = 4096) -> None:
    if key.key_length < min_key_length:
        raise UserError(
            f"Key {key.key_id} is shorter than the minimal "
            f"required length of {min_key_length} bit"
        )


@to_user_error(gpg.KeyserverError)
def upload_keys(fingerprints: List[str], keyserver: str, gpg_store: GPGStore) -> None:
    """Upload public key to keyserver"""
    gpg_store.send_keys(*fingerprints, keyserver=keyserver, url_opener=urlopen)


@to_user_error((gpg.KeyserverError, gpg.KeyserverKeyNotFoundError))
def download_keys(fingerprints: List[str], keyserver: str, gpg_store: GPGStore) -> None:
    """Download public key to keyserver"""
    gpg_store.recv_keys(*fingerprints, keyserver=keyserver, url_opener=urlopen)


def detach_sign_file(
    src: Union[bytes, IO[bytes]],
    signature_fingerprint: str,
    passphrase: Secret[str],
    gpg_store: GPGStore,
) -> bytes:
    """Sign a file with a detached signature"""
    try:
        with gpg_store.detach_sig(
            src, passphrase.reveal(), signature_fingerprint
        ) as out:
            return out.read()
    except gpg.GPGError as e:
        raise UserError(f"File signing failed. {e}") from e


def enforce_passphrase(passphrase: Optional[Secret[str]]) -> Secret[str]:
    """Verify that a passphrase is not empty, and return it"""
    if passphrase is None:
        raise ValueError("No password given")
    return passphrase


def check_password(
    password: Secret[str], key_fingerprint: str, gpg_store: GPGStore
) -> None:
    """Verify that the provided password matches the specified PGP key.

    The verification is done by trying to use the key specified via its
    fingerprint to sign some mock data. If this opperation fails, the password
    is incorrect and an error is raised.
    """
    try:
        with gpg_store.detach_sig(
            src=b"test", passphrase=password.reveal(), signee=key_fingerprint
        ):
            pass
    except gpg.GPGError:
        raise UserError("GPG password is incorrect") from None


def check_password_matches_any_key(
    password: Secret[str], keys: Iterable[gpg.Key], gpg_store: GPGStore
) -> None:
    """Check whether a password matches any of the provided GPG keys.

    If the password does not match with any of the keys, an error is raised.

    :param keys: list of GPG keys to check.
    :param password: password to check against the different keys.
    :param gpg_store: GnuPG database containing the keys to check.
    :raises UserError:
    """
    for key in keys:
        try:
            check_password(
                password=password,
                key_fingerprint=key.fingerprint,
                gpg_store=gpg_store,
            )
            break
        except UserError:
            pass
    else:
        raise UserError(
            "The provided password does not match any of the GPG keys with "
            "which the data was encrypted"
        )


class KeyType(enum.Enum):
    public = enum.auto()
    secret = enum.auto()


def search_pub_key(search_term: str, gpg_store: GPGStore, sigs: bool = True) -> gpg.Key:
    """Search for a single public key in the local keyring based on the input
    search term. If no or more than one key is matching the search term, an
    error is raised.

    :param gpg_store: key database as gnupg object.
    :param search_term: search term for the key, e.g. fingerprint or key owner
        email address.
    :param sigs: if True, return key with signatures.
    :return: PGP key matching the search term.
    :raises UnpackError:
    """
    keys = gpg_store.list_pub_keys(search_terms=(search_term,), sigs=sigs)
    try:
        (key,) = keys
    except ValueError:
        raise UnpackError(
            keys, key_type=KeyType.public, search_value=search_term
        ) from None
    return key


def search_priv_key(search_term: str, gpg_store: GPGStore) -> gpg.Key:
    """Searches the user's local keyring for a secret key matching the search
    term. Raises an error if no or more than one key are found.
    """
    keys = gpg_store.list_sec_keys(search_terms=(search_term,))
    try:
        (key,) = keys
    except ValueError:
        raise UnpackError(
            keys, key_type=KeyType.secret, search_value=search_term
        ) from None
    return key


class UnpackError(UserError):
    """Error class that displays an error message for the cases when a search
    for a public/secret key on the user's local keyring does not yield exactly
    one match"""

    def __init__(self, keys: Sequence[gpg.Key], key_type: KeyType, search_value: str):
        if not keys:
            msg_start = f"No {key_type.name} key"
        else:
            msg_start = f"Multiple {key_type.name} keys"
        super().__init__(msg_start + f" matching: {search_value}")


def encrypt_and_sign(
    source: gpg.cmd.ISource,
    output: gpg.cmd.OSource,
    gpg_store: GPGStore,
    recipients_fingerprint: List[str],
    signature_fingerprint: Optional[str] = None,
    passphrase: Optional[Secret[str]] = None,
    always_trust: bool = True,
) -> None:
    """Encrypt input data with a PGP public key and sign it with a private key.

    In this function, the compression level of the "encrypt()" method is set
    to 0 as we are only encrypting data that has already been compressed, or
    has explicitely been requested by the user not to be compressed.

    There is no check of the validity of the sender and recipient keys, as it
    is assumed that this is already done earlier.

    :param source: callable writing data to encrypt.
    :param output: callable reading encrypted data.
    :param gpg_store: directory containing GnuPG keyrings as gnupg object.
    :param recipients_fingerprint: fingerprint of public key(s) with which
        the data should be encrypted.
    :param signature_fingerprint: fingerprint of private key with which the
        data should be signed. If the parameter value is set to None the
        encrypted file is not signed.
    :param passphrase: password associated to 'signature_fingerprint'. This
        parameter value can be set to None if the encrypted file should not be
        signed.
    :param always_trust: if False, the encryption key must be signed by the
        local user.
    :raises UserError:
    """
    try:
        # Note: gpg.CompressAlgo.NONE evaluates to "uncompressed", which
        # tells GnuPG to not compress the input data.
        gpg_store.encrypt(
            source=source,
            recipients=recipients_fingerprint,
            output=output,
            passphrase=reveal(passphrase),
            trust_model=gpg.TrustModel.always if always_trust else gpg.TrustModel.pgp,
            sign=signature_fingerprint,
            compress_algo=gpg.CompressAlgo.NONE,
        )
    except gpg.GPGError:
        raise UserError(
            "Encryption failed. Maybe you entered a wrong passphrase."
        ) from None


def get_recipient_email(key: gpg.Key) -> str:
    """Retrieve the email address associated with a PGP key, and generate a
    an error if the email address is missing or could not be retrieved.
    """
    try:
        email = key.uids[0].email
    except (IndexError, UnpackError):
        raise UserError(
            f"Could not determine email address for PGP key {key.key_id}."
        ) from None
    if not email:
        raise UserError(
            f"PGP key [{key.key_id}] does not contain a valid email address."
        )
    return email


def decrypt(
    source: gpg.cmd.ISource,
    output: Union[str, gpg.cmd.OSource],
    gpg_store: GPGStore,
    passphrase: Optional[Secret[str]],
) -> List[str]:
    """Decrypt data.

    :param source: data to encrypt.
    :param output: encrypted data.
    :param gpg_store: directory containing GnuPG keyrings as gnupg object.
    :param passphrase: password associated to 'signature_fingerprint'. This
        parameter value can be set to None if the encrypted file should not be
        signed.
    :return: fingerprint or keyid of the signee's key.
    :raises UserError:
    """
    try:
        if isinstance(output, str):
            with open(output, "wb") as fout:
                sender_fprs = gpg_store.decrypt(
                    source=source,
                    output=cast(io.FileIO, fout),
                    passphrase=reveal(passphrase),
                )
        else:
            sender_fprs = gpg_store.decrypt(
                source=source, output=output, passphrase=reveal(passphrase)
            )
    except gpg.GPGError as e:
        raise UserError(
            "Failed to decrypt. Error message from gpg:\n" + format(e)
        ) from e
    if not sender_fprs:
        warnings.warn("Encrypted package is not signed by the sender")
    elif len(sender_fprs) > 1:
        warnings.warn(
            "Encrypted package has multiple signatures. "
            "This is not compliant with the BiomedIT Protocol"
        )
    return sender_fprs


def create_key(
    full_name: str,
    email: str,
    pwd: Secret[str],
    gpg_store: GPGStore,
    key_type: str = "RSA",
    key_length: int = 4096,
) -> gpg.Key:
    """Create a new PGP public/private key"""
    min_pwd_len = 10
    if len(full_name) < 5:
        raise UserError("Full name must be at least 5 characters long.")
    if not re.search(r"[^@]+@[^@]+\.[^@]+", email):
        raise UserError("Invalid email address.")
    if len(pwd.reveal()) < min_pwd_len:
        raise UserError("Password is too short (min length: " f"{min_pwd_len})")
    fingerprint = gpg_store.gen_key(
        key_type=key_type,
        key_length=key_length,
        full_name=full_name,
        email=email,
        passphrase=pwd.reveal(),
    )
    pkey = gpg_store.list_sec_keys(search_terms=(fingerprint,))
    if not pkey:
        raise UserError(f"No private keys found for: {fingerprint}")
    if len(pkey) > 1:
        raise UserError(f"Multiple private keys found for: {fingerprint}")
    return pkey[0]


def load_authority_key(sett_config: Config) -> Optional[gpg.Key]:
    """Load (download if needed) and refresh the key authority's PGP key

    The function returns None if either:
     * No key authority fingerprint is given in the config.
     * The key matching the fingerprint could not be retrieved, neither from
       the local keyring nor from the keyserver.
    """
    if sett_config.key_authority_fingerprint:
        try:
            return crypt.retrieve_and_refresh_certification_authority_key(
                key_fingerprint=sett_config.key_authority_fingerprint,
                gpg_store=sett_config.gpg_store,
                keyserver_url=sett_config.keyserver_url,
                validate_key_origin=False,
                allow_key_download=sett_config.allow_gpg_key_autodownload,
                url_opener=urlopen,
            )
        except RuntimeError as e:
            warnings.warn(
                "The key validation authority's PGP key "
                f"[{sett_config.key_authority_fingerprint}] could not be "
                "found in your local keyring, nor could it be downloaded.\n"
                "Please verify that the key validation authority fingerprint "
                "and the keyserver URL settings are correct. Also verify that "
                "you are not in offline mode and that PGP key auto-download "
                "is enabled.\n"
                f"Reason for failure: {e}"
            )

    return None
