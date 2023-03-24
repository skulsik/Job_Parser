import os
import requests
import datetime
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


class ListVerification:
    def __init__(self, list_v: list):
        """ Проверка на содержимое списка """
        try:
            if list_v is None:
                raise ListError('ListError: На запись передан пустой список')
        except ListError:
            exit()


class FileDateVerification:
    def __init__(self):
        """
        Проверяет фаил на существование, если существует проверяет время существования.
        При запуске программы если фаил существует более 23:59, флаг self.file_date становится True,
        что приводит к обновлению фаила.
        """
        # Флаг, True запуск чтения вакансий с сайтов
        self.file_date: bool = False

        # Разница времён
        time_: object = None

        # Максимальное время в течении которого не будет обновляться база с вакансиями 23:59:59
        time_max: object = datetime.timedelta(0, 59, 0, 0, 59, 23)

        # Путь к файлу
        path: str = 'data/job.json'

        if os.path.exists(path):
            # Получает время создания фаила
            time_file: object = os.path.getmtime(path)

            # Преобразует к комфортному формату
            time_file = datetime.datetime.fromtimestamp(time_file)

            # Читает современное время
            time_now: object = datetime.datetime.now()

            # Разница времён
            time_ = time_now - time_file

            if time_max < time_:
                self.file_date = True
        else:
            self.file_date = True

    @property
    def get_file_date(self):
        return self.file_date


class KeyInDictVerification:
    def __init__(self, item_dict: dict = {}, job_site: str = ''):
        snippet_f: bool = False
        pay_f: bool = False
        url_f: bool = False
        experience_f: bool = False

        # Если проверяем HH.ru
        if job_site == 'HH':
            if 'snippet' in item_dict and 'requirement' in item_dict['snippet'] and item_dict['snippet']['requirement']:
                snippet_f = True
            if 'salary' in item_dict and 'from' in item_dict['salary'] and item_dict['salary']['from']:
                pay_f = True
            if 'salary' in item_dict and 'to' in item_dict['salary'] and item_dict['salary']['to']:
                pay_f = True
            if 'alternate_url' in item_dict and item_dict['alternate_url']:
                url_f = True

        # Если проверяем SuperJob
        if job_site == 'SuperJob':
            if 'candidat' in item_dict and item_dict['candidat']:
                snippet_f = True
            if 'payment_from' in item_dict and item_dict['payment_from']:
                pay_f = True
            if 'payment_to' in item_dict and item_dict['payment_to']:
                pay_f = True
            if 'link' in item_dict and item_dict['link']:
                url_f = True

        self.key_bool_dict = {'snippet': snippet_f,
                              'pay': pay_f,
                              'url': url_f}


    @property
    def get_key_in_dict_verification(self) -> dict:
        """
        :return: словарь key=bool. True - ключ имеет данные
        """
        return self.key_bool_dict
