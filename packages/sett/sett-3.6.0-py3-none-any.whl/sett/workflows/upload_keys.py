from typing import Sequence

from ..core.crypt import (
    upload_keys as crypt_upload_keys,
    verify_key_length,
    search_pub_key,
)
from ..core.error import UserError
from ..utils.log import create_logger, log_runtime_info
from ..utils.config import Config


logger = create_logger(__name__)


@log_runtime_info(logger)
def upload_keys(key_ids: Sequence[str], *, config: Config) -> None:
    """Upload one or more public PGP keys to the keyserver specified in the
    config.
    """
    if config.offline:
        raise UserError("Uploading keys is not possible in the offline mode.")
    if config.keyserver_url is None:
        raise UserError("Keyserver URL is undefined.")
    keys = frozenset(search_pub_key(k, config.gpg_store, sigs=False) for k in key_ids)
    for key in keys:
        verify_key_length(key)
    if keys:
        logger.info("Uploading keys '%s'", ", ".join(k.key_id for k in keys))
        crypt_upload_keys(
            [k.fingerprint for k in keys],
            keyserver=config.keyserver_url,
            gpg_store=config.gpg_store,
        )
