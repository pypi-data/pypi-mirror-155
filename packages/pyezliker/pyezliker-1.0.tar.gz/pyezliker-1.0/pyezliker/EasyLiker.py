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

ez = EasyLiker("06895uX71tG3H0x9h13sxrmN6U9Yhm7i")

print(ez.get_account_balance())

#print(ez.get_services()['youtube'])
#{'quality': 'offers_medium_quality', 'price': 0.4, 'description': 'офферы, среднее качество', 'min_limit': 20}
#print(ez.create_task(website="youtube", type="likes", quality="offers_medium_quality", link="https://www.youtube.com/watch?v=bj4ul946k2o", count=150))
#{'id': 477515, 'link': 'https://www.youtube.com/watch?v=bj4ul946k2o', 'price': 60.0, 'balance': 78.4, 'status': 'Выполняется'}

print(ez.get_tasks(id=477515))
#[{'id': 477515, 'creation_date': '2022-06-16T10:17:00.126647', 'name': 'Youtube лайки | офферы, среднее качество', 'link': 'https://www.youtube.com/watch?v=bj4ul946k2o', 'sum': 60.0, 'count': 150, 'done': 0, 'status': 'Выполняется', 'date': '16.06.2022 | 10:17:00'}]


