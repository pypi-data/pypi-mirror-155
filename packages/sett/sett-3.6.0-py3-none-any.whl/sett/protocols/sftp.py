import re
import os
import io
from datetime import datetime
from socket import socket
from dataclasses import dataclass, field
from typing import (
    Optional,
    Union,
    Callable,
    Tuple,
    List,
    Sequence,
    Type,
    Generator,
    Any,
    cast,
)
from pathlib import Path, PurePosixPath
from contextlib import contextmanager

import sett_rs
from paramiko import (
    RSAKey,
    DSSKey,
    ECDSAKey,
    Ed25519Key,
    Transport,
    ssh_exception,
    SSHClient,
    AutoAddPolicy,
    Agent,
    Channel,
    SFTPClient,
)
from paramiko.pkey import PKey
from paramiko import SSHException as _SSHException

from ..utils.progress import ProgressInterface
from ..utils.log import create_logger
from ..utils.get_config_path import get_config_file
from ..core.error import UserError
from ..core.filesystem import (
    to_human_readable_size,
    reverse_expanduser,
    abspath_expanduser,
)
from ..core.secret import Secret, reveal
from .defs import ENVELOPE_DIR_FMT
from . import protocol

# Re-exports
SSHException = _SSHException


logger = create_logger(__name__)


def opt_reverse_expanduser(path: Optional[str]) -> Optional[str]:
    return reverse_expanduser(path) if path else None


@dataclass
class Protocol(protocol.Protocol):
    host: str
    username: str
    destination_dir: str
    envelope_dir: Optional[str] = None
    pkey: Optional[str] = field(
        default=None,
        metadata={
            "serialize": opt_reverse_expanduser,
            "deserialize": abspath_expanduser,
        },
    )
    pkey_password: Optional[Secret[str]] = None
    pkey_password_encoding: str = (
        "utf_8"  # nosec (False Positive: pkey_password_encoding)
    )
    jumphost: Optional[str] = None

    def __post_init__(self) -> None:
        # Turn empty strings into None and check that the ssh key file exists
        self.pkey = os.path.expanduser(self.pkey) if self.pkey else None
        self.pkey_password = self.pkey_password or None

    def required_password_args(self) -> Sequence[str]:
        if self.pkey is not None and self.pkey_password is None:
            return ("pkey_password",)
        return ()

    def upload(
        self,
        files: Sequence[str],
        two_factor_callback: Callable[[], str],
        progress: Optional[ProgressInterface] = None,
    ) -> None:
        if self.pkey and not os.path.exists(self.pkey):
            raise UserError(f"SSH key not found: {self.pkey}")

        if self.jumphost:
            self.upload_paramiko(
                files, progress=progress, two_factor_callback=two_factor_callback
            )
        else:
            host, port = parse_host(self.host)
            try:
                sett_rs.sftp_upload(
                    files,
                    f"{host}:{port}",
                    self.username,
                    self.destination_dir,
                    self.envelope_dir,
                    self.pkey,
                    reveal(self.pkey_password),
                    progress.update if progress is not None else None,
                    two_factor_callback=two_factor_callback,
                )
            except RuntimeError as e:
                logger.warning(format(e))
                self.upload_paramiko(
                    files, progress=progress, two_factor_callback=two_factor_callback
                )

    def upload_paramiko(
        self,
        files: Sequence[str],
        two_factor_callback: Callable[[], str],
        progress: Optional[ProgressInterface] = None,
    ) -> None:
        if self.envelope_dir is None:
            envelope_dir = datetime.now().strftime(ENVELOPE_DIR_FMT)
        progress_callback = (
            (lambda x, y: progress.update(x / y)) if progress is not None else None
        )
        remote_dir = PurePosixPath(self.destination_dir) / envelope_dir
        try:
            with sftp_connection(
                host=self.host,
                username=self.username,
                pkey=self.pkey,
                jumphost=self.jumphost,
                pkey_password=self.pkey_password,
                pkey_password_encoding=self.pkey_password_encoding,
                two_factor_callback=two_factor_callback,
            ) as sftp:
                try:
                    sftp.mkdir(str(remote_dir))
                except FileNotFoundError as e:
                    raise UserError(
                        "Remote destination directory does not exist: "
                        f"{self.destination_dir}"
                    ) from e
                except PermissionError as e:
                    raise UserError(
                        "You don not have enough permissions to write "
                        f"to the remote directory: {self.destination_dir}"
                    ) from e
                for package in files:
                    remotepath = str(remote_dir / Path(package).name)
                    remotepath_part = remotepath + ".part"
                    status = sftp.put(
                        localpath=os.path.realpath(package),
                        remotepath=remotepath_part,
                        callback=progress_callback,
                        confirm=True,
                    )
                    remote_size = status.st_size
                    local_size = os.path.getsize(os.path.realpath(package))

                    if local_size != remote_size:
                        raise UserError(
                            f"Incomplete file transfer: '{package}'\n"
                            f"Remote: {remote_size}\nLocal: {local_size}"
                        )

                    try:
                        sftp.posix_rename(remotepath_part, remotepath)
                    except IOError as e:
                        raise UserError(format(e)) from e
                    logger.info(
                        "Successful transfer of %s (size: %s)",
                        package,
                        to_human_readable_size(local_size),
                    )
                with io.BytesIO(b"") as fl:
                    sftp.putfo(
                        fl=fl,
                        remotepath=str(remote_dir / "done.txt"),
                        callback=progress_callback,
                        confirm=True,
                    )
        except ssh_exception.AuthenticationException as e:
            raise UserError(format(e)) from e


@contextmanager
def sftp_connection(  # nosec
    host: str,
    username: str,
    two_factor_callback: Callable[[], str],
    pkey: Optional[str] = None,
    pkey_password: Optional[Secret[str]] = None,
    pkey_password_encoding: str = "utf_8",
    jumphost: Optional[str] = None,
) -> Generator[SFTPClient, None, None]:
    key = (
        private_key_from_file(
            str(Path(pkey).expanduser()), pkey_password, encoding=pkey_password_encoding
        )
        if pkey
        else None
    )
    if jumphost is not None:
        pw = two_factor_callback()
        sock: Union[str, Channel] = proxy_socket(
            host, jumphost, username, pkey=key, password=pw
        )
    else:
        sock = host
    trans = Transport(cast(Union[str, socket], sock))
    trans.connect()
    try:
        auth(trans, username, key, two_factor_callback)
        sftp_client = None
        try:
            sftp_client = trans.open_sftp_client()
            if sftp_client is None:
                raise UserError(f"Could not open a sftp connection to {host}")
            yield sftp_client
        finally:
            if sftp_client:
                sftp_client.close()
    finally:
        trans.close()


def auth(
    trans: Transport,
    username: str,
    key: Optional[PKey],
    two_factor_callback: Callable[[], str],
) -> None:
    allowed_types = []
    if key is not None:
        allowed_types = trans.auth_publickey(username, key)
    else:
        try:
            allowed_types = auth_from_agent(trans, username)
        except SSHException:
            trans.auth_timeout = 120
            trans.auth_interactive(username, auth_handler)
    two_factor = bool(set(allowed_types) & _TWO_FACTOR_TYPES)
    if two_factor:
        f2_code = two_factor_callback()
        trans.auth_password(username, f2_code)


def proxy_socket(host: str, jumphost: str, username: str, **kwargs: Any) -> Channel:
    tunnel = SSHClient()
    tunnel.set_missing_host_key_policy(AutoAddPolicy())
    tunnel.connect(
        jumphost,
        username=username,
        allow_agent=True,
        **kwargs,
    )
    transport = tunnel.get_transport()
    if transport is None:
        raise UserError(f"Could not open sftp channel to {host}")
    return transport.open_channel(
        "direct-tcpip", parse_host(host), parse_host(jumphost)
    )


def parse_host(host: str) -> Tuple[str, int]:
    try:
        _host, port = host.split(":")
        return _host, int(port)
    except ValueError:
        return host, 22


def auth_handler(_title: Any, _instructions: Any, prompt_list: Any) -> List[str]:
    if prompt_list:
        auth_url = re.findall(r"(https?://\S+)", prompt_list[0][0])
        if auth_url:
            logger.info("Authenticate at: %s", auth_url[0])
    return ["" for _ in prompt_list]


def is_ascii(s: str) -> bool:
    return all(ord(c) < 128 for c in s)


def private_key_from_file(
    path: str, password: Optional[Secret[str]], encoding: str = "utf_8"
) -> PKey:
    errors = set()
    pass_bytes = None if password is None else password.reveal().encode(encoding)
    pkey_class: Type[PKey]
    for pkey_class in (RSAKey, DSSKey, ECDSAKey, Ed25519Key):
        try:
            return pkey_class.from_private_key_file(path, pass_bytes)  # type: ignore
        except (SSHException, ValueError) as e:
            errors.add(format(e).lower())
    if password is not None and not is_ascii(password.reveal()):
        errors.add(
            "Your ssh secret key's password seems to contain "
            "some non-ascii characters. "
            "Either change your password ("
            "`ssh-keygen -f <path to your private key> -p`)"
            " or make sure the config option "
            "`ssh_password_encoding` is set to the same "
            "encoding that your key has been created with. "
            f"Your config file is here: {get_config_file()}. "
            "The encoding is usually `utf_8` on linux "
            "/ mac and `cp437` on windows for keys generated "
            "with ssh-keygen."
        )
    raise UserError(
        "Could not load private key. "
        f"Please make sure that the password for {path} is not empty and correct. "
        f"Original errors: {'; '.join(sorted(errors, key=len))}."
    )


def auth_from_agent(transport: Transport, username: str) -> List[str]:
    agent = Agent()
    try:
        for key in agent.get_keys():
            try:
                logger.debug("Trying SSH agent key %s", key.get_fingerprint())
                # for 2-factor auth a successfully auth'd key password
                # will return an allowed 2fac auth method
                return transport.auth_publickey(username, key)
            except SSHException:
                pass
    finally:
        agent.close()
    raise SSHException("Could not load key from ssh agent")


_TWO_FACTOR_TYPES = {"keyboard-interactive", "password"}
