from typing import Optional, Dict, Callable, Any, TypeVar
from urllib.error import HTTPError, URLError
import base64
import json
from functools import wraps

from .request import post, urlopen
from .metadata import MetaData
from .error import UserError


class PortalApi:
    sign_request = "/backend/pgpkey/sign-request/"
    dpkg_check = "/backend/data-package/check/"

    def __init__(self, base_url: str):
        self.base_url = base_url

    @staticmethod
    def auth_header(
        username: Optional[str] = None, password: Optional[str] = None
    ) -> Dict[str, str]:
        auth_str = (
            username
            and password
            and base64.b64encode(":".join((username, password)).encode()).decode()
        )
        return {"Authorization": f"Basic {auth_str}"} if auth_str else {}

    def verify_transfer(self, metadata: MetaData, filename: str) -> str:
        """Verify transfer_id using external API.

        Return project_code for a valid transfer_id.
        """
        data = json.dumps(
            {"file_name": filename, "metadata": json.dumps(MetaData.asdict(metadata))}
        ).encode()
        response = handle_errors(post)(self.base_url + self.dpkg_check, data)
        try:
            project_code: str = json.loads(response)["project_code"]
            return project_code
        except json.decoder.JSONDecodeError as e:
            raise UserError(
                "PortalApi.verify_transfer: got invalid json from portal: "
                + response.decode()
            ) from e
        except KeyError as e:
            raise UserError(
                "PortalApi.verify_transfer: json response from portal does "
                "not include field `project_code`: " + response.decode()
            ) from e

    def request_key_signature(self, keyid: str) -> bool:
        """Request key signature"""
        url = self.base_url + self.sign_request
        if not url.lower().startswith("http"):
            raise ValueError(f"Invalid scheme: '{url}'")
        data = f"pgpkey_id={keyid}".encode()
        result: bool = handle_errors(get)(url, data)
        return result


def get(url: str, data: bytes) -> bool:
    with urlopen(url, data):
        return True


R = TypeVar("R")


def handle_errors(f: Callable[..., R]) -> Callable[..., R]:
    @wraps(f)
    def _f(*args: Any, **kwargs: Any) -> R:
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            msg_raw = e.read()
            try:
                msg = json.loads(msg_raw)["detail"]
            except (json.decoder.JSONDecodeError, KeyError, TypeError):
                msg = msg_raw.decode()
            raise UserError("PortalApi: " + msg) from e
        except URLError:
            raise UserError("Could not connect to the server.") from None

    return _f
