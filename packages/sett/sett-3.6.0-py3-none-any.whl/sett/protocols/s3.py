from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Sequence

from minio import Minio
from minio.error import S3Error

from . import protocol
from ..core.error import UserError
from ..core.filesystem import to_human_readable_size
from ..core.secret import Secret
from ..utils.log import create_logger
from ..utils.progress import ProgressInterface, with_progress

logger = create_logger(__name__)


@dataclass
class Protocol(protocol.Protocol):
    host: str
    bucket: str
    access_key: str
    secret_key: Optional[Secret[str]] = None

    def required_password_args(self) -> Sequence[str]:
        return ("secret_key",)

    def upload(
        self,
        files: Sequence[str],
        two_factor_callback: Callable[[], str],
        progress: Optional[ProgressInterface] = None,
    ) -> None:
        if self.secret_key is None:
            raise UserError("Secret Key is missing")
        url_components = self.host.split("://")
        if len(url_components) > 1:
            logger.warning(
                "S3 host name should not contain scheme, ignoring '%s'",
                url_components[0],
            )
        try:
            client = Minio(
                url_components[-1],  # ignore scheme if present
                access_key=self.access_key,
                secret_key=self.secret_key.reveal(),
            )
            for f in files:
                p = Path(f)
                size = p.stat().st_size
                with open(p, "rb") as f_obj:
                    client.put_object(
                        self.bucket, p.name, with_progress(f_obj, progress), size
                    )
                logger.info(
                    "Successful transfer of %s (size: %s)",
                    f,
                    to_human_readable_size(size),
                )
        except S3Error as e:
            raise UserError(e) from e
