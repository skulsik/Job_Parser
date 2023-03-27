import os
import requests
import datetime
import json
from Lib.Errors import *


class RequestVerification:
    def __init__(self, http: str = '', key: str = ''):
        """
        Проверка адреса на существование или работоспособность
        Запрос адреса может быть выполнен как с ключем API, так и без него
        """
        try:
            if http == '' or 'http' not in http:
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
    def __init__(self, name_key: str = ''):
        """ Проверка наличия ключа (имени) в переменных окружения Windows """
        self.api_key: str = ''
        try:
            if name_key == '':
                raise NameKeyError('NameKeyError: Имя ключа не передано.')
            if os.getenv(name_key):
                self.api_key = os.getenv(name_key)
            else:
                raise APIKeyError('APIKeyError: В переменных окружения Windows отсутствует ключ API SuperJob.')
        except APIKeyError:
            exit()
        except NameKeyError:
            exit()


    def __str__(self) -> str:
        """
        :return: Ключ API из переменных окружения
        """
        return self.api_key


class ListVerification:
    def __init__(self, list_v: list):
        """ Проверка на содержимое списка """
        try:
            list_v
        except ValueError as e:
            ListError('ListError: На запись передан пустой список')
            exit()


class JsonVerification:
    def __init__(self, json_list: list = []):
        """ Проверка на содержимое списка """
        try:
            json.loads(json_list)
        except ValueError as e:
            JsonError('JsonError: Ошибка чтения json файла.')
            exit()


class FileDateVerification:
    # Путь к файлу
    path: str = 'data/job.json'


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

        if os.path.exists(self.path):
            # Получает время создания фаила
            time_file: object = os.path.getmtime(self.path)

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
        """
        :return: True - обновить фаил
        """
        return self.file_date


class KeyInDictVerification:
    def __init__(self, item_dict: dict = {}, job_site: str = ''):
        """ Проверка ключей в словарях взятых с разных сайтов вакансий"""
        # Описание вакансии
        snippet_f: bool = False
        # Зарплата от
        pay_f_from: bool = False
        # Зарплата до
        pay_f_to: bool = False
        # Ссылка на вакансию
        url_f: bool = False
        # Требуемый опыт
        experience_f: bool = False
        # Индификатор вакансии
        id_f: bool = False

        # Проверяем ключи HH.ru
        if job_site == 'HH':
            # Проверка ключа (описание вакансии)
            if 'snippet' in item_dict and item_dict['snippet']:
                if 'requirement' in item_dict['snippet'] and item_dict['snippet']['requirement']:
                    snippet_f = True

            # Проверка ключей (зп)
            if 'salary' in item_dict and item_dict['salary']:
                # Проверка ключа (зп от)
                if 'from' in item_dict['salary'] and item_dict['salary']['from']:
                    pay_f_from = True

                # Проверка ключа (зп до)
                if 'to' in item_dict['salary'] and item_dict['salary']['to']:
                    pay_f_to = True

            # Проверка ключа (ссылка на вакансию)
            if 'alternate_url' in item_dict and item_dict['alternate_url']:
                url_f = True

        # Проверяем ключи SuperJob
        if job_site == 'SuperJob':
            # Проверка ключа (описание вакансии)
            if 'candidat' in item_dict and item_dict['candidat']:
                snippet_f = True

            # Проверка ключа (зп от)
            if 'payment_from' in item_dict and item_dict['payment_from']:
                pay_f_from = True

            # Проверка ключа (зп до)
            if 'payment_to' in item_dict and item_dict['payment_to']:
                pay_f_to = True

            # Проверка ключа (ссылка на вакансию)
            if 'link' in item_dict and item_dict['link']:
                url_f = True

            # Проверка ключа (требуемый опыт)
            if 'experience' in item_dict and item_dict['experience']:
                if 'id' in item_dict['experience'] and item_dict['experience']['id']:
                    experience_f = True

        # Проверка ключа (Индификатор вакансии)
        if 'id' in item_dict and item_dict['id']:
            id_f = True

        # Заполняем словарь ключ -> значение(bool)
        self.key_bool_dict: dict = {'snippet': snippet_f,
                                    'pay_from': pay_f_from,
                                    'pay_to': pay_f_to,
                                    'url': url_f,
                                    'experience': experience_f,
                                    'id': id_f}


    @property
    def pay_key_in_dict_verification(self) -> bool:
        """
        :return: Если зп есть в одном из ключей, вернет True
        """
        if self.key_bool_dict['pay_from'] or self.key_bool_dict['pay_to']:
            return True
        return False


    @property
    def get_key_in_dict_verification(self) -> dict:
        """
        :return: словарь key=bool. True - ключ имеет данные
        """
        return self.key_bool_dict
