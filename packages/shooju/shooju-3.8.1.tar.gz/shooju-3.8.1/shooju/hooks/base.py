from __future__ import division, absolute_import, print_function, unicode_literals

import abc
import dataclasses
from typing import Dict, Any, Union


@dataclasses.dataclass
class Request:
    """
    Represents low level API requests that is about to be made.

    :param str method: HTTP method name
    :param str url: a full url with scheme, host, path, but with no url params
    :param dict params: url parameters
    :param dict headers: request HTTP headers
    :param bytes data: url encoded content
    :param bytes data_raw: raw payload data
    :param dict data_json: parsed (if not binary) api payload
    """

    method: str
    url: str
    params: Union[Dict[str, Any], None]
    headers: Dict[str, str]
    data: bytes
    data_raw: bytes
    data_json: Union[Dict[str, Any], None]


@dataclasses.dataclass
class Response:
    """
    Represents low level API response

    :param str content: raw content of the response
    :param dict headers: response headers
    :param dict status_code: HTTP status code
    :param dict json: parsed (if not binary) content
    """
    content: str
    headers: Dict[str, str]
    status_code: int
    json: Union[Dict[str, Any], None]


class BaseHook:
    """
    An object that is able to modify API requests before they made, and API responses after they received.
    """
    @abc.abstractmethod
    def before_request(self, request: Request) -> Request:
        return request

    @abc.abstractmethod
    def after_request(self, response: Response) -> Response:
        return response
