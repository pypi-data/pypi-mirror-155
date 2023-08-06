import requests
import json
import threading
from .exceptions import *

class VkApiSimple:
    """
    :param token: Токен аккаунта ВК
    :type token: str
    
    :param v: Версия используемого api
    :type v: int
    """

    def __init__(self, token, v=5.131):
        self.token = token
        self.v = v
        self.lock = threading.Lock()

    def method(self, method, params={}):
        """ Вызов метода API

        :param method: Название метода
        :type method: str
        
        :param params: Параметры
        :type params: dict

        Бросает `ApiHttpError` в случае неуспешного кода возварата http запроса
        
        Бросает `ApiError` в случае неуспешного запроса к API

        Возвращает `response['response']` в случае успеха
        """

        params = params.copy() if params else {}
        if 'v' not in params:
            params['v'] = self.v

        params["access_token"] = self.token

        with self.lock:
            response = requests.get(
                f"https://api.vk.com/method/{method}",
                params=params
            )

        if response.ok:
            response = response.json()
        else:
            raise ApiHttpError(self, method, params, response)

        if 'error' in response:
            raise ApiError(self, method, params, response['error'])

        return response['response']
