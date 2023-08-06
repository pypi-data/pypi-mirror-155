import os
import urllib
import urllib.request
from http.client import HTTPResponse
from typing import Tuple, Union, Callable

from .error import UserError


UrlOpener = Callable[..., HTTPResponse]


def build_opener(default_opener: UrlOpener = urllib.request.urlopen) -> UrlOpener:
    proxy_env = os.environ.get("HTTPS_PROXY") or os.environ.get("ALL_PROXY")
    if proxy_env is not None and proxy_env.startswith("socks"):
        protocol, host, port = proxy_env.split(":")
        return socks_opener((protocol, host.lstrip("/"), int(port)))
    return default_opener


def socks_opener(proxy_settings: Tuple[str, str, int]) -> UrlOpener:
    """Returns an opener based on proxy settings: Normal opener if no proxy
    settings are given, PySocks opener if proxy settings are given
    """
    return urllib.request.build_opener(socks_handler(*proxy_settings)).open


def socks_handler(
    protocol: str, host: str, port: int
) -> Union[urllib.request.HTTPSHandler, urllib.request.HTTPHandler]:
    try:
        import socks  # pylint: disable=import-outside-toplevel

        # pylint: disable=import-outside-toplevel
        from sockshandler import (
            SocksiPyHandler,
        )
    except ModuleNotFoundError:
        raise UserError(
            "module PySocks needs to be available when using a proxy"
        ) from None
    protocol_mapping = {"socks4": socks.SOCKS4, "socks5": socks.SOCKS5}
    try:
        protocol = protocol_mapping[protocol]
    except KeyError:
        raise UserError("Invalid scheme " + protocol) from None
    handler: Union[
        urllib.request.HTTPSHandler, urllib.request.HTTPHandler
    ] = SocksiPyHandler(protocol, host, port)
    return handler


urlopen = build_opener()


def post(url: str, data: bytes) -> bytes:
    request = urllib.request.Request(
        url,
        data,
        method="POST",
        headers={"Content-Type": "application/json; charset=UTF-8"},
    )
    with urlopen(request) as response:
        response_text = response.read()
        return response_text
