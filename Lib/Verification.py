import os
import requests
from Lib.Errors import *


class RequestVerification:
    def __init__(self, http: str = None, key: str = None):
        """
        Проверка адреса на существование или работоспособность
        Запрос адреса может быть выполнен как с ключем API, так и без него
        """
        try:
            if http is None or 'http' not in http:
                raise HTTPError('HTTPError: Не передан адрес, либо передан некорректно.')

            # Запрос
            response = requests.get(http, headers={"X-Api-App-Id": key})
            if response.status_code >= 400:
                raise RequestError(response.status_code)
        except RequestError:
            exit()
        except HTTPError:
            exit()


class APIKeyVerification:
    def __init__(self, name_key: str = None):
        """ Проверка наличия ключа (имени) в переменных окружения Windows """
        self.api_key: str = ''
        try:
            if name_key is None:
                raise NameKeyError('NameKeyError: Имя ключа не передано.')
            if os.getenv(name_key):
                self.api_key = os.getenv(name_key)
            else:
                raise APIKeyError('APIKeyError: В переменных окружения Windows отсутствует ключ API SuperJob.')
        except APIKeyError:
            exit()
        except NameKeyError:
            exit()


    def __str__(self) -> object:
        return self.api_key
