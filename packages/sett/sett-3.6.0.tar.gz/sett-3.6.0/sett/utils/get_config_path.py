import os
import platform
from typing import Tuple, Dict

from .. import APP_NAME_SHORT
from ..core.error import UserError

CONFIG_FILE_ENVIRON_VAR = "SETT_CONFIG_FILE"
CONFIG_FILE_NAME = "config.json"


def get_config_file() -> str:
    """Retrieve the platform-specific path of the config file. If the user has
    the correct config file path environmental variable defined in their
    current environment, this file gets used instead.

    :return: path of the config.
    :raises UserError:
    """
    # Case 1: a config file path environmental variable is defined.
    if CONFIG_FILE_ENVIRON_VAR in os.environ:
        config_file = os.environ[CONFIG_FILE_ENVIRON_VAR]
        if os.path.isdir(config_file):
            raise UserError(
                f"Environmental variable {CONFIG_FILE_ENVIRON_VAR} "
                f"must point to a file, not a directory "
                f"[{config_file}]."
            )
        return config_file

    # Case 2: use the default platform-specific config file.
    return os.path.join(get_config_dir(), CONFIG_FILE_NAME)


def get_config_dir() -> str:
    """Return platform specific default config direcory."""
    return os.path.join(
        os.path.expanduser("~"), *conf_sub_dir_by_os[platform.system()], APP_NAME_SHORT
    )


conf_sub_dir_by_os: Dict[str, Tuple[str, ...]] = {
    "Linux": (".config",),
    "Darwin": (".config",),
    "Windows": ("AppData", "Roaming"),
}
