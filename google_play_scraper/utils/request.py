from typing import Union
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ..exceptions import ExtraHTTPError, NotFoundError


def _urlopen(obj):
    try:
        resp = urlopen(obj)
    except HTTPError as e:
        if e.code == 404:
            raise NotFoundError("App not found(404).")
        else:
            raise ExtraHTTPError(
                "App not found. Status code {} returned.".format(e.code)
            )

    return resp.read().decode("UTF-8")


def post(url: str, data: Union[str, bytes], headers: dict) -> str:
    return _urlopen(Request(url, data=data, headers=headers))


def get(url: str) -> str:
    return _urlopen(url)
