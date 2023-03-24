from Lib.Verification import *
import json


class JobProcessing:
    # Путь к файлу вакансий json
    path_file_json: str = 'data/job.json'


    def __init__(self):
        """ Инициализация свойств """
        # Список вакансий
        self.job_list: list = []
        # Список вакансий для вывода пользователю
        self.print_job_list: list = []


    def recording_job_in_the_file(self, job_list: list = None):
        """ Запись в фаил списка вакансий """
        # Проверка на передачу пустого списка
        ListVerification(job_list)

        job_list = json.dumps(job_list, indent=2, ensure_ascii=False)

        # Получаем дескриптор фаила
        fd = os.open(self.path_file_json, os.O_WRONLY | os.O_CREAT)

        # Превратить в файл
        with open(fd, mode='w', encoding='UTF-8', closefd=False) as file:
            file.write(job_list)

        # Закрываем дескриптор файла
        os.close(fd)


    def read_file_job(self) -> list:
        """ Чтение фаила json с вакансиями в список"""
        # Получаем дескриптор фаила
        fd = os.open(self.path_file_json, os.O_RDONLY)

        # Превратить в файл
        with open(fd, mode='r', encoding='UTF-8', closefd=False) as file:
            self.job_list = file.read()
        self.job_list = json.loads(self.job_list)

        # Закрываем дескриптор файла
        os.close(fd)


    def search_for_job(self, number_of_vacancies: int = 10, job_parameters:str = '') -> list:
        """ Метод поиска вакансий по заданным критериям """
        # Переменные для инкримента
        hh: int = 0
        sj: int = 0
        # Количество записываемых вакансий в список, делим на 2 так как два сайта вакансий(половина с одного сайта, половина с другого)
        number_of_vacancies = number_of_vacancies/2

        for item in self.job_list:
            # Все вакансии приводим к единому виду
            # Берем из HH.ru
            if 'name' in item and hh < number_of_vacancies:
                # Проверка ключей на наличие в них данных
                KIDV: object = KeyInDictVerification(item, 'HH')
                # Возвращает словарь key=bool. True - ключ имеет данные
                key_bool_dict: dict = KIDV.get_key_in_dict_verification

                hh += 1
                self.print_job_list += [{'name': item['name'],
                                         'requirement': item['snippet']['requirement'],
                                         'from': item['salary']['from'],
                                         'to': item['salary']['to'],
                                         'url': item['alternate_url']}]

            # Берем из SuperJob
            if 'profession' in item and sj < number_of_vacancies:
                # Проверка ключей на наличие в них данных
                KIDV: object = KeyInDictVerification(item, 'SuperJob')
                # Возвращает словарь key=bool. True - ключ имеет данные
                key_bool_dict: dict = KIDV.get_key_in_dict_verification

                sj += 1
                self.print_job_list += [{'name': item['profession'],
                                         'requirement': item['candidat'],
                                         'from': item['payment_from'],
                                         'to': item['payment_to'],
                                         'url': item['link']}]

                # для поиска без опыта
                # if 'experience' in item and 'name' in item:
                #     print(item['experience']['id'])


    @property
    def print_job(self):
        """ Вывод списка вакансий на экран"""
        print('\n')
        for item in self.print_job_list:
            print('****************************************************************************************************')
            print(f"Название вакансии: {item['name']}")
            print(f"Требования к кандидату: {item['requirement']}")
            pay: str = ''
            if item['from']:
                pay = str(item['from'])
            if item['to']:
                pay = pay + f" - {item['to']}"
            if pay == '':
                pay: str = "зарплата не указана"
            print(f"Зарплата: {pay}")
            print(f"Ссылка на вакансию: {item['url']}")

        print('****************************************************************************************************')
