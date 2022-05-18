import json
from typing import Union

import requests
from requests import Response

from framework.logger import Logger
from framework.patterns import Singleton


def check_response_status(func):
    def _check_response_status(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            body = json.dumps(response.json(), indent=4)
        except:
            body = response.text
        Logger.debug(f"Response status code={response.status_code}, elapsed time = {response.elapsed}\n\n{body}\n")
        response.raise_for_status()
        return response

    return _check_response_status


class ApiClient(metaclass=Singleton):
    def __init__(self, url: str):
        # TODO: add session support
        self._url = url

    @check_response_status
    def get(self, endpoint: str, params: Union[dict, list[tuple]] = None, **kwargs) -> Response:
        request_url = f"{self._url}/{endpoint}"
        Logger.info(f"Send 'GET' request to {request_url} with params={params}, kwargs={kwargs}")
        return requests.get(request_url, params=params, **kwargs)

    @check_response_status
    def post(self, endpoint: str, data: Union[dict, list[tuple]] = None, json: dict = None, **kwargs) -> Response:
        request_url = f"{self._url}/{endpoint}"
        return requests.post(request_url, data=data, json=json, **kwargs)

    @check_response_status
    def put(self, endpoint: str, data: Union[dict, list[tuple]] = None, **kwargs) -> Response:
        request_url = f"{self._url}/{endpoint}"
        return requests.post(request_url, data=data, **kwargs)

    @check_response_status
    def patch(self, endpoint: str, data: Union[dict, list[tuple]] = None, **kwargs) -> Response:
        request_url = f"{self._url}/{endpoint}"
        return requests.patch(request_url, data=data, **kwargs)

    @check_response_status
    def delete(self, endpoint: str, **kwargs) -> Response:
        request_url = f"{self._url}/{endpoint}"
        return requests.delete(request_url, **kwargs)
