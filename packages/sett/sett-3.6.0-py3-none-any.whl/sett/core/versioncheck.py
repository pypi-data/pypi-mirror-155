import warnings
import re
import urllib.error
from typing import Optional

from sett import URL_READTHEDOCS, APP_NAME_SHORT
from ..core.request import urlopen
from .. import __version__, __project_name__


def check_version(repo_url: str, gui_formatting: bool = False) -> None:
    latest = get_latest_version(repo_url)
    if (
        not __version__.startswith("0.0.0.dev")
        and __version__ != latest
        and latest is not None
    ):
        line_break = "\n"
        update_doc_url = (
            f"{URL_READTHEDOCS}/en/stable/" "sett_installation.html#updating-sett"
        )
        if gui_formatting:
            line_break = "<br>"
            update_doc_url = f"<a href='{update_doc_url}'>{update_doc_url}</a>"
        warnings.warn(
            f"Your {APP_NAME_SHORT} version ({__version__}) is "
            f"outdated and no longer supported.{line_break}"
            f"Please upgrade to the latest version ({latest}) as "
            f"soon as possible.{line_break * 2}"
            f"In most cases, {APP_NAME_SHORT} can be upgraded with "
            f"the following commmand:{line_break}"
            f"pip install --upgrade --user sett{line_break * 2}"
            f"Documentation on how to upgrade your {APP_NAME_SHORT} "
            f"installation can also be found at:{line_break}"
            f"{update_doc_url}{line_break}"
        )


def get_latest_version(repo_url: str) -> Optional[str]:
    try:
        url = repo_url + "/simple/" + __project_name__ + "/"
        with urlopen(url) as response:
            versions = re.findall(
                __project_name__.encode() + b"-([0-9]*.[0-9]*.[0-9]*).tar.gz",
                response.read(),
            )
            version = max(tuple(map(int, v.split(b"."))) for v in versions)
    except urllib.error.URLError:
        warnings.warn(
            "Could not connect to pypi repository to query the latest version. "
            "You might have an outdated version. Please check yourself!"
        )
        return None
    except IndexError:
        warnings.warn(
            "No releases found on the pypi repository! "
            "Please contact the developers!"
        )
        return None
    return ".".join(map(str, version))
