from __future__ import annotations
from requests import post
from json import loads, dumps


class SendRequestError(Exception):
    pass



class EasyLiker(object):


    def __init__(self, token) -> EasyLiker:
        self.token = token
        self.headers = {
            "Content-type": "application/json"
            }
        self.api_url="https://easyliker.ru/api"

        self.default_data = {
            "api_token": self.token, 
            "method": "None", 
            "version": 2.0}

    def __req_worker(self, data):
        response = loads(post(self.api_url, data=dumps(data), headers=self.headers).text)
        if "error" in response.keys():
            raise SendRequestError(f"Ошибка при отправке запроса: {response['error']}")
        return response['response']

    def get_account_balance(self) -> float:
        temp_data = self.default_data
        temp_data['method']  = "getBalance"
        return self.__req_worker(temp_data)

    def get_services(self) -> dict:
        temp_data = self.default_data
        temp_data['method']  = "getServices"
        return self.__req_worker(temp_data)

    def create_task(self, 
            website: str, type: str,
            quality: str, link: str,
            count: str, option: list | int = None
            ) -> dict:

        temp_data = self.default_data
        temp_data['method']  = "createTask"
        temp_data['website'] = website
        temp_data['quality'] = quality
        temp_data['type'] = type
        temp_data['link'] = link
        temp_data['count'] = count
        if option:
            temp_data['option'] = option

        return self.__req_worker(temp_data)

    def get_tasks(self,
            id : int =None, count : int=None, 
            offset : int=None,) -> dict:
        
        temp_data = self.default_data

        if id:
            temp_data['id'] = id
        if count:
            temp_data['count'] = count
        if offset:
            temp_data['offset'] = offset
        temp_data['method']  = "getTasks"
        return self.__req_worker(temp_data) 

