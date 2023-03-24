from abc import ABC
from Lib.Verification import *


class Engine(ABC):
    @abstractmethod
    def get_request():
        message = 'class Engine'
        return message


    def adding_job_listings(job_list: list = []) -> list:
        """ Суммирование разных списков вакансий"""
        return sum(job_list, start=[])


class HH(Engine):
    # Адрес сайта с вакансиями
    http: str = 'https://api.hh.ru/'

    # Количество запрошенных выкансий
    number_of_vacancies_requested: int = 500

    # Количество вакансий, читаемых за один запрос <=100
    number_of_vacancies_at_once: int = 100
    per_page: str = f'per_page={str(number_of_vacancies_at_once)}'

    # Количество страниц(всего), округлит до целого числа в меньшую сторону
    pages: int = int(number_of_vacancies_requested / number_of_vacancies_at_once)


    def __init__(self, text: str = ''):
        """
        Инициализация свойств(переменных)
        :param text: название профессии, свойство поиска
        """
        # Инициализация списка, для формирования списка вакансий
        self.__requests_job_list: list = []

        # Название вакансии
        self.text: str = f'text={text}'

        # Переменная для навигации по страницам
        self.page: int = 0


    def get_request(self) -> list:
        """
        Метод чтения вакансий и заполнения списка полученными вакансиями
        Количство запрошенных профессий может отличаться от количества существующих, в связи с этим выполнена
        проверка количества страниц из запроса. requests_job["pages"] - содержит количество страниц на сайте по
        данному запросу профессии
        :return: Список вакансий по введеному названию профессии
        """
        # Проверка адреса на работаспособность
        RequestVerification(self.http)

        # Временный словарь для хранения запроса(словаря вакансий)
        requests_job: dict = requests.get(f'{self.http}vacancies?{self.text}&&{self.per_page}&&page={self.page}').json()

        # Проверка кол-ва страниц из запроса и обычная проверка страниц из заданных настроек
        if self.page < requests_job["pages"] and self.page < self.pages:
            # Добавление в список, списка вакансий с данной страницы
            self.__requests_job_list += requests_job['items']

            # Инкремент, страница
            self.page += 1

            # Запуск рекурсии
            self.get_request()


    @property
    def get_job_list(self) -> list:
        """
        :return: Список вакансий HH.ru
        """
        return self.__requests_job_list


class SuperJob(Engine):
    # API_You_Tube_KEY переменные окружения
    name_of_the_environment_variable = 'SuperJobKey'

    # Адрес сайта с вакансиями
    http: str = 'https://api.superjob.ru/2.0/vacancies/'

    # Количество запрошенных выкансий <=500
    number_of_vacancies_requested: int = 500

    # Количество вакансий, читаемых за один запрос <=100
    number_of_vacancies_at_once: int = 100

    # Количество страниц(всего), округлит до целого числа в меньшую сторону
    pages: int = int(number_of_vacancies_requested/number_of_vacancies_at_once)


    def __init__(self, keyword: str = ''):
        # Инициализация списка, для формирования списка вакансий
        self.__requests_job_list: list = []

        # Название вакансии
        self.keyword: str = f'{keyword}'

        # Переменная для навигации по страницам
        self.page: int = 1


    def get_request(self):
        """
        Метод чтения вакансий и заполнения списка полученными вакансиями
        Количство запрошенных профессий может отличаться от количества существующих, в связи с этим выполнена
        проверка количества страниц из запроса. requests_job["total"] - если равен 0, значит страница пустая
        :return: Список вакансий по введеному названию профессии
        """
        # Получает ключ, из переменных окружения Windows
        api_key = str(APIKeyVerification(self.name_of_the_environment_variable))

        # Проверка адреса на работаспособность
        RequestVerification(self.http, api_key)

        # Временный словарь для хранения запроса(словаря вакансий)
        requests_job: dict = requests.get(f'{self.http}',
                                          headers={"X-Api-App-Id": api_key},
                                          params={'keywords': self.keyword,
                                                  'count': self.number_of_vacancies_at_once,
                                                  'page': self.page}).json()

        # Проверка на пустую страницу из запроса и обычная проверка страниц из заданных настроек
        if requests_job["total"] != 0 and self.page <= self.pages:
            # Добавление в список, списка вакансий с данной страницы
            self.__requests_job_list += requests_job['objects']

            # Инкремент, страница
            self.page += 1

            # Запуск рекурсии
            self.get_request()


    @property
    def get_job_list(self) -> list:
        """
        :return: Список вакансий SuperJob
        """
        return self.__requests_job_list


class JobAssembly:
    def __init__(self, job_name: str = ''):
        """ Сборка классов разных сайтов в один. Формирование одного списка вакансий."""
        # Общий список вакансий с двух сайтов
        self.__all_requests_list: list = []

        # Берем вакансии с HH.ru
        HH_ru = HH(job_name)
        HH_ru.get_request()
        hh_requests_list = HH_ru.get_job_list

        # Берем вакансии с SuperJob
        SJ = SuperJob(job_name)
        SJ.get_request()
        sj_requests_list = SJ.get_job_list

        # Объединение списков вакансий в единый
        self.__all_requests_list = Engine.adding_job_listings([hh_requests_list, sj_requests_list])


    @property
    def get_all_requests_list(self):
        """
        :return: Список вакансий с сайтов
        """
        return self.__all_requests_list
