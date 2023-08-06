import platform
import sys
from email.message import Message
from typing import Optional, Any

try:
    from importlib.metadata import (
        metadata as _importlib_get_metadata,
        version as _version,
        PackageNotFoundError,
    )

    # Note: using "Any" here as return type because the type returned by
    # importlib.metadata.metadata() changes between python versions.
    #  -> python < 3.10: email.message.Message
    #  -> python >= 3.10: PackageMetadata
    # This can be changed the day python < 3.10 support is dropped.
    def _get_metadata(distribution_name: str) -> Optional[Any]:
        try:
            return _importlib_get_metadata(distribution_name)
        except PackageNotFoundError:
            return None

    def _get_version(dep: str) -> Optional[str]:
        try:
            return _version(dep)
        except PackageNotFoundError:
            return None

except ImportError:
    from pkg_resources import get_distribution, DistributionNotFound
    import email.parser

    def _get_version(dep: str) -> Optional[str]:
        try:
            return get_distribution(dep).version
        except DistributionNotFound:
            return None

    def _get_metadata(distribution_name: str) -> Optional[Any]:
        try:
            dist = get_distribution(distribution_name)
        except DistributionNotFound:
            return None
        raw_metadata = dist.get_metadata(dist.PKG_INFO)
        return email.parser.Parser().parsestr(raw_metadata)


from .version import __version__ as _v

# re-exports
__version__ = _v
_metadata = _get_metadata(__name__)

if _metadata is not None:
    APP_NAME_LONG = _metadata["Summary"]
    __project_name__ = _metadata["Name"]
    _urls = dict(entry.split(", ") for entry in _metadata.get_all("Project-URL"))
else:
    APP_NAME_LONG = "No description available"
    __project_name__ = __name__
    _urls = {}

APP_NAME_SHORT = __name__
URL_GITLAB = _urls.get("Source", "<Not available>")
URL_GITLAB_ISSUES = URL_GITLAB + "/-/issues"
URL_READTHEDOCS = _urls.get("Documentation", "<Not available>")
VERSION_WITH_DEPS = (
    f"{APP_NAME_SHORT} {__version__} ("
    + ", ".join(
        f"{n} {_get_version(n) or 'not_found'}"
        for n in ("gpg-lite", "libbiomedit", "sett-rs")
    )
    + ")"
)
RUNTIME_INFO = f"{VERSION_WITH_DEPS} (Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}, platform: {platform.platform()})"
