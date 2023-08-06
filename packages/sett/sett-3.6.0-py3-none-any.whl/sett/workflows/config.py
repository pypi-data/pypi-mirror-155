import os

from ..utils.config import create_config
from ..utils.get_config_path import get_config_file
from ..utils.log import create_logger, log_runtime_info

logger = create_logger(__name__)


@log_runtime_info(logger)
def create() -> None:
    """Creates a new default config file in the users config dir."""
    config_file = get_config_file()
    if os.path.isfile(config_file):
        logger.info("The config file already exists at '%s'.", config_file)
    else:
        create_config()
        logger.info("Created config file at '%s'", config_file)
