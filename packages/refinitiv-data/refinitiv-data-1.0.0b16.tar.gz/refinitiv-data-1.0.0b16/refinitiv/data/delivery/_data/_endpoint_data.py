# coding: utf8

import collections
from enum import Enum, unique
from typing import Any

Error = collections.namedtuple("Error", ["code", "message"])


@unique
class RequestMethod(Enum):
    """
    The RESTful Data service can support multiple methods when
    sending requests to a specified endpoint.
       GET : Request data from the specified endpoint.
       POST : Send data to the specified endpoint to create/update a resource.
       DELETE : Request to delete a resource from a specified endpoint.
       PUT : Send data to the specified endpoint to create/update a resource.
    """

    GET = 1
    POST = 2
    DELETE = 3
    PUT = 4


class EndpointData(object):
    def __init__(self, raw: Any, **kwargs):
        if raw is None:
            raw = {}
        self._raw = raw
        self._kwargs = kwargs

    @property
    def raw(self):
        return self._raw
