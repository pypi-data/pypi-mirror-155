from __future__ import annotations
from requests import post
from json import loads, dumps


class SendRequestError(Exception):
    pass


class EasyLiker:
    _API_URL = "https://easyliker.ru/api"
    _HEADERS = {
        "Content-type": "application/json",
        }

    def __init__(self, token: str) -> EasyLiker:
        self._token = token

    def _call_api(self, method, data = None):
        request_data = {
            "api_token": self._token,
            "method": method,
            "version": 2.0,
            }
        if data:
            request_data.update(data)
        response = loads(post(self._API_URL, data = dumps(request_data), headers = self._HEADERS).text)
        if "error" in response.keys():
            raise SendRequestError(f"Ошибка при отправке запроса: {response['error']}")
        return response['response']

    def get_account_balance(self) -> float:
        return self._call_api("getBalance")

    def get_services(self) -> dict:
        return self._call_api("getServices")

    def create_task(
            self,
            website: str,
            type: str,
            quality: str,
            link: str,
            count: str,
            option: list | int = None) -> dict:
        data = {
            'website': website,
            'quality': quality,
            'type': type,
            'link': link,
            'count': count,
            }
        if option:
            data['option'] = option
        return self._call_api("createTask", data)

    def get_tasks(
            self,
            id: int = None,
            count: int = None,
            offset: int = None) -> dict:
        data = {}
        if id:
            data['id'] = id
        if count:
            data['count'] = count
        if offset:
            data['offset'] = offset
        return self._call_api("getTasks", data)