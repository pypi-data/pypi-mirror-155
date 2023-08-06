from typing import Type, Dict, Tuple

from .protocol import Protocol as _Protocol
from . import liquid_files, sftp, s3

# reexport
Protocol = _Protocol

protocols: Tuple[Type[Protocol], ...] = (
    sftp.Protocol,
    liquid_files.Protocol,
    s3.Protocol,
)
protocols_by_name: Dict[str, Type[Protocol]] = {
    p.__module__.replace(__name__ + ".", ""): p for p in protocols
}
__all__ = tuple(protocols_by_name)
protocol_name = {protocol: name for name, protocol in protocols_by_name.items()}


def parse_protocol(s: str) -> Type[Protocol]:
    try:
        return protocols_by_name[s]
    except KeyError:
        raise ValueError(f"Invalid protocol: {s}") from None
