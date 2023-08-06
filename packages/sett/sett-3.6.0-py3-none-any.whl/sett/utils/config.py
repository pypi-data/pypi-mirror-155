import enum
import json
import os
import platform
import warnings
from dataclasses import dataclass, field as _field, fields
from pathlib import Path
from typing import Dict, Optional, Callable, Union, Any

from libbiomedit.lib import deserialize as serialization

from .log import get_default_log_dir, create_logger
from .validation import REGEX_URL, PACKAGE_SUFFIX
from .get_config_path import get_config_file, CONFIG_FILE_NAME
from .. import APP_NAME_SHORT
from ..core import gpg
from ..core.error import UserError
from ..core.filesystem import reverse_expanduser, abspath_expanduser
from ..core.portal_api import PortalApi
from ..protocols import Protocol, protocol_name, parse_protocol

PKEY_PARAM_NAME = "pkey"

logger = create_logger(__name__)


class FileType(enum.Enum):
    file = enum.auto()
    directory = enum.auto()


@dataclass
class FieldMetadata:
    description: Optional[str]
    label: Optional[str]
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    file_type: Optional[FileType] = None
    regex: Optional[str] = None


def reverse_expanduser_if_path_exists(path: Optional[str]) -> Optional[str]:
    return reverse_expanduser(path) if path else path


SerializedConnection = Dict[str, Union[str, Dict[str, Any]]]


def serialize_connection(connection: Protocol) -> SerializedConnection:
    return {
        "protocol": protocol_name[type(connection)],
        "parameters": serialization.serialize(type(connection))(connection),
    }


def serialize_connections(
    connections: Dict[str, Protocol]
) -> Dict[str, SerializedConnection]:
    return {
        name: serialize_connection(connection)
        for name, connection in connections.items()
    }


def deserialize_connections(
    connections: Dict[str, SerializedConnection]
) -> Dict[str, Protocol]:
    def get_protocol(connection: SerializedConnection) -> str:
        protocol = connection["protocol"]
        if not isinstance(protocol, str):
            raise ValueError("Invalid value for connection in config")
        return protocol

    return {
        name: serialization.deserialize(parse_protocol(get_protocol(connection)))(
            connection["parameters"]
        )
        for name, connection in connections.items()
    }


def field_ext(
    serialize: Optional[Callable[[Any], Any]] = None,
    deserialize: Optional[Callable[[Any], Any]] = None,
    **kwargs: Any,
) -> Any:
    field_names = {f.name for f in fields(FieldMetadata)}
    field_kwargs = {key: val for key, val in kwargs.items() if key not in field_names}
    metadata = {
        key: val
        for key, val in kwargs.items()
        if key not in field_kwargs and val is not None
    }
    if metadata:
        # The dataclasses doc specifies, that metadata should be a mapping.
        # Therefore we wrap our dataclass in a dict:
        field_kwargs["metadata"] = {"metadata": FieldMetadata(**metadata)}
        if serialize:
            field_kwargs["metadata"]["serialize"] = serialize
        if deserialize:
            field_kwargs["metadata"]["deserialize"] = deserialize
    return _field(**field_kwargs)


LABEL_COMPRESSION_LEVEL = "Compression level"
DESCRIPTION_COMPRESSION_LEVEL = (
    "Compression level used in data encryption, from 0 (no compression) to "
    "9 (highest). Higher compression levels require more computing time."
)


@dataclass
class Config:
    """dataclass holding config data"""

    dcc_portal_url: str = field_ext(
        default="https://portal.dcc.sib.swiss",
        label="DCC portal URL",
        description="URL of portal instance. The portal is used for key signing and "
        "DTR (Data Transfer Request) validation.",
        regex=REGEX_URL,
    )
    keyserver_url: Optional[str] = field_ext(
        default="keyserver.dcc.sib.swiss",
        label="Keyserver URL",
        description="URL of the keyserver: used for publishing/fetching public PGP keys.",
        # no validation, as specifying http:// is optional
    )
    gpg_home_dir: str = field_ext(
        serialize=reverse_expanduser_if_path_exists,
        deserialize=abspath_expanduser,
        default=gpg.get_default_gnupg_home_dir(),
        label="GPG home directory",
        description="Path of the directory where GnuPG stores its keyrings and "
        "configuration files.",
        file_type=FileType.directory,
    )
    key_authority_fingerprint: Optional[str] = field_ext(
        default="B37CE2A101EBFA70941DF885881685B5EE0FCBD3",
        label="Key validation authority fingerprint",
        description="Fingerprint (40 characters) of the key validation authority's "
        "PGP key. If a value is specified, only keys signed the "
        "authority's key can be used.",
    )
    sign_encrypted_data: bool = field_ext(
        default=True,
        label="Sign encrypted data",
        description="Whether encrypted data should be signed with sender's key.",
    )
    always_trust_recipient_key: bool = field_ext(
        default=True,
        label="Always trust recipient key",
        description="If unchecked, the encryption key must be signed by the local user.",
    )
    repo_url: str = field_ext(
        default="https://pypi.org",
        label="Repo URL",
        description="Python package repository, used when looking for updates.",
        regex=REGEX_URL,
    )
    check_version: bool = field_ext(
        default=True,
        label="Check version",
        description="Check whether you have the latest version of sett on startup.",
    )
    offline: bool = field_ext(
        default=False,
        label="Offline mode",
        description="In offline mode, sett will not make any network connections: "
        "DTR verification and automatic PGP key downloading/updating is disabled.",
    )
    log_dir: str = field_ext(
        serialize=reverse_expanduser_if_path_exists,
        deserialize=abspath_expanduser,
        default=get_default_log_dir(),
        label="Log directory",
        description="Path to log files directory.",
        file_type=FileType.directory,
    )
    error_reports: bool = field_ext(
        default=True,
        label="Create error reports",
        description="Write an error report if some error happens.",
    )
    log_max_file_number: int = field_ext(
        default=1000,
        label="Log max. file number",
        description="Maximum number of log files to keep as backup. "
        "Set to 0 to disable logging.",
        minimum=0,
    )
    connections: Dict[str, Protocol] = field_ext(
        serialize=serialize_connections,
        deserialize=deserialize_connections,
        label="Connections",
        description="List of used-defined connections for data transfer.",
        default_factory=dict,
    )
    output_dir: Optional[str] = field_ext(
        serialize=reverse_expanduser_if_path_exists,
        deserialize=abspath_expanduser,
        default=None,
        label="Output directory",
        description="Default output directory, relevant for encryption/decryption.",
        file_type=FileType.directory,
    )
    ssh_password_encoding: str = field_ext(
        default="utf_8",
        label="SSH password encoding",
        description="Character encoding used for the SSH key password.",
    )
    default_sender: Optional[str] = field_ext(
        default=None,
        label="Default sender",
        description="Default sender fingerprint for encryption.",
    )
    gui_quit_confirmation: bool = field_ext(
        default=True,
        label="Quit confirmation",
        description="Ask for confirmation before closing the application.",
    )
    compression_level: int = field_ext(
        default=5,
        label=LABEL_COMPRESSION_LEVEL,
        description=DESCRIPTION_COMPRESSION_LEVEL,
        minimum=0,
        maximum=9,
    )
    package_name_suffix: Optional[str] = field_ext(
        default=None,
        label="Default package suffix",
        description="Default suffix for encrypted package name",
        regex=PACKAGE_SUFFIX,
    )
    max_cpu: int = field_ext(
        default=0,
        label="Max CPU",
        description="Maximum number of CPU cores for parallel computation "
        "(use all CPU cores if value equals 0)",
        minimum=0,
        maximum=os.cpu_count()
        or 4,  # In case cpu_count fails to detect the number of available cores
        # use a reasonable default
    )
    gpg_key_autodownload: bool = field_ext(
        default=True,
        label="Allow PGP key auto-download",
        description="Allow the automatic download and refresh of PGP keys "
        "from the Keyserver.",
    )

    verify_package_name: bool = field_ext(
        default=True,
        label="Verify package name",
        description="Verify that the name of data packages follows the "
        f"{APP_NAME_SHORT} naming convention",
    )

    def __post_init__(self) -> None:
        for url in ("dcc_portal_url", "repo_url"):
            setattr(
                self, url, getattr(self, url).rstrip("/")  # pylint: disable=no-member
            )

    @property
    def portal_api(self) -> PortalApi:
        return PortalApi(self.dcc_portal_url)

    @property
    def gpg_store(self) -> gpg.GPGStore:
        return open_gpg_dir(self.gpg_home_dir)

    @property
    def allow_gpg_key_autodownload(self) -> bool:
        """Property indicating whether GPG keys can be automatically downloaded
        and refreshed from a keyserver, if a keyserver is specified.
        Key auto-download is not allowed in the following situations:
         * There is no defined validation authority. If keys do not need to be
           certified by a central key authority, auto-downloading them presents
           a security risk (keys should be manually downloaded and checked) and
           is therefore not allowed.
         * The 'offline' mode is activated, no network access is allowed.
         * The user has decided to not allow it.
        """
        return (
            self.key_authority_fingerprint is not None
            and not self.offline
            and self.gpg_key_autodownload
        )


class ConnectionStore:
    """Sftp/LiquidFiles connection configuration storage manager."""

    config_field_name = "connections"

    def __init__(self, config_path: Optional[str] = None):
        self.path = get_config_file() if config_path is None else config_path

    def _read(self) -> Dict[str, Any]:
        """Load data from config file"""
        return load_config_dict(self.path)

    def _write(self, data: Dict[str, Any]) -> None:
        """Write data to config file"""
        save_config(data, self.path)

    def save(self, name: str, connection: Protocol) -> None:
        """Save a new connection to the config file.

        :param name: name of the new connection.
        :param connection: new connection object to write to the config file.
        """
        # Load entire sett configuration file data as a dict. It might or might
        # not already contain a "connections" field containing data for one or
        # more connections. If not, an empty "connections" field is added.
        data = self._read()
        connections = data.setdefault(self.config_field_name, {})
        connections[name] = serialize_connection(connection)
        self._write(data)

    def delete(self, name: str) -> None:
        """Delete a new connection from the config file"""
        data = self._read()
        try:
            data.get(self.config_field_name, {}).pop(name)
            self._write(data)
        except KeyError as e:
            raise UserError(f"Connection '{name}' does not exist.") from e

    def rename(self, old: str, new: str) -> None:
        """Rename an existing connection from the config file"""
        data = self._read()
        try:
            connection = data.get(self.config_field_name, {}).pop(old)
            data[self.config_field_name][new] = connection
            self._write(data)
        except KeyError as e:
            raise UserError(f"Connection '{new}' does not exist.") from e


def load_config() -> Config:
    """Loads the config, returning a Config object."""

    # TODO: remove migration (see issue 283)
    migrate_user_config_file()

    cfg_dct = {}
    try:
        cfg_dct = sys_config_dict()
        cfg_dct.update(load_config_dict(get_config_file()))
    except UserError as e:
        warnings.warn(format(e))

    return serialization.deserialize(Config)(cfg_dct)


def save_config(config: Dict[str, Any], path: Optional[str] = None) -> str:
    """Save the specified config values to the specified path (file name).
    If no path is specified, the config file is saved in the default location.

    :param config: application config values in the form of a dictionary.
    :param path: path + name of the config file to write to disk.
    :return: path of the created config file.
    """
    config_file = Path(get_config_file() if path is None else path)
    if not config_file.parent.is_dir():
        config_file.parent.mkdir(parents=True)

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, sort_keys=True)

    return config_file.as_posix()


def create_config() -> str:
    """Creates a new config file in the home directory's config folder
    :return: path of the created config file.
    """
    return save_config(config_to_dict(default_config()))


def config_to_dict(config: Config) -> Dict[str, Any]:
    """Converts a Config object into a dict."""
    data: Dict[str, Any] = serialization.serialize(Config)(config)
    return data


def default_config() -> Config:
    """Creates a new Config object with default values."""
    return serialization.deserialize(Config)(sys_config_dict())


def sys_config_dict() -> Dict[str, Any]:
    """On linux only: try to load global sys config. If the env variable
    SYSCONFIG is set search there, else in /etc/{APP_NAME_SHORT}.
    """
    if platform.system() == "Linux":
        sys_cfg_dir = os.environ.get("SYSCONFIG", os.path.join("/etc", APP_NAME_SHORT))
        return load_config_dict(os.path.join(sys_cfg_dir, CONFIG_FILE_NAME))
    return {}


def load_config_dict(path: str) -> Dict[str, Any]:
    """Load raw config as a dict."""
    try:
        with open(path, encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
            if not isinstance(data, dict):
                raise UserError(
                    f"Failed to load configuration from '{path}'. Wrong format."
                )
            return data
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError as e:
        raise UserError(f"Failed to load configuration from '{path}'. {e}") from e


def open_gpg_dir(gpg_dir: str) -> gpg.GPGStore:
    """Open the database inside a GnuPG directory and return it as a gpg
    object.

    :param gpg_dir: path of the GnuPG directory to open.
    :return: a gpg-lite GPGStore
    :raises UserError:
    """
    if not Path(gpg_dir).is_dir():
        os.makedirs(gpg_dir, mode=0o700)

    try:
        return gpg.GPGStore(gnupg_home_dir=gpg_dir)
    except ValueError:
        raise UserError(f"unable to open GnuPG directory [{gpg_dir}].") from None


def migrate_user_config_file() -> None:
    """Temporary migrations to auto-update a user's config file after arguments
    are modified or deprecated in sett.
    """
    config_file = get_config_file()
    config_needs_update = False

    try:
        config_dict = load_config_dict(config_file)
    except UserError:
        return

    # Migration to remove "temp_dir" from config.
    # Migration added in July 2021, can be removed after about a year.
    if "temp_dir" in config_dict:
        del config_dict["temp_dir"]
        config_needs_update = True

    if "connections" in config_dict:
        for connection in config_dict["connections"].values():
            if "pkey_password" in connection["parameters"]:
                del connection["parameters"]["pkey_password"]
                config_needs_update = True

    if config_needs_update:
        save_config(config_dict, path=config_file)
