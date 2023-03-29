from Lib.Verification import *
import json
from operator import itemgetter


class JobProcessing:
    # Путь к файлу вакансий json
    path_file_json: str = 'data/job.json'


    def __init__(self):
        """ Инициализация свойств """
        # Список вакансий
        self.job_list: list = []
        # Голова стэка вакансий
        self.head_stack_vacancy: object = None
        # Хвост стэка вакансий
        self.tail_stack_vacancy: object = None


    def recording_job_in_the_file(self, job_list: list = []):
        """ Запись в фаил списка вакансий """
        # Проверка на передачу пустого списка
        ListVerification(job_list)

        job_list = json.dumps(job_list, indent=2, ensure_ascii=False)

        # Получаем дескриптор файла
        fd = os.open(self.path_file_json, os.O_WRONLY | os.O_CREAT)

        # Превратить в файл
        with open(fd, mode='w', encoding='UTF-8', closefd=False) as file:
            file.write(job_list)

        # Закрываем дескриптор файла
        os.close(fd)


    def read_file_job(self):
        """ Чтение фаила json с вакансиями в список"""
        # Получаем дескриптор файла
        fd = os.open(self.path_file_json, os.O_RDONLY)

        # Превратить в файл
        with open(fd, mode='r', encoding='UTF-8', closefd=False) as file:
            self.job_list = file.read()

        # Проверка на целостность json
        JsonVerification(self.job_list)

        self.job_list = json.loads(self.job_list)

        # Закрываем дескриптор файла
        os.close(fd)

    @staticmethod
    def removing_characters_from_a_string(str_requirement: str = ''):
        """ Удаление ненужных тегов """
        str_requirement_new = str_requirement.replace('<highlighttext>', '')
        str_requirement_new = str_requirement_new.replace('</highlighttext>', '')
        return str_requirement_new


    def search_for_job(self, number_of_vacancies: int = 10) -> list:
        """ Метод поиска последних вакансий и запись в список """
        # Переменные для инкремента
        hh: int = 0
        sj: int = 0
        # Количество записываемых вакансий в список, делим на 2 так как два сайта вакансий(половина с одного сайта, половина с другого)
        number_of_vacancies = int(number_of_vacancies/2)

        for item in self.job_list:
            # Все вакансии приводим к единому виду
            # Берет из HH.ru
            if 'name' in item and hh < number_of_vacancies:
                # Проверка ключей существование и наличие в них данных
                KIDV: object = KeyInDictVerification(item, 'HH')
                # Возвращает словарь key=bool. True - ключ имеет данные
                key_bool_dict: dict = KIDV.get_key_in_dict_verification

                # При существовании нужных ключей
                if KIDV.pay_key_in_dict_verification and key_bool_dict['snippet'] and key_bool_dict['url']:
                    # Убирает ненужные теги
                    requirement: str = JobProcessing.removing_characters_from_a_string(item['snippet']['requirement'])
                    hh += 1
                    # Формирование вакансии
                    job_dict: dict = {'name': item['name'],
                                             'requirement': requirement,
                                             'from': item['salary']['from'],
                                             'to': item['salary']['to'],
                                             'url': item['alternate_url']}
                    # Создает стэк с вакансиями, ячейка - экземпляр с вакансией
                    vacancy = Vacancy(job_dict)
                    if self.head_stack_vacancy:
                        self.tail_stack_vacancy.next_job = vacancy
                    else:
                        self.head_stack_vacancy = vacancy
                    self.tail_stack_vacancy = vacancy


            # Берет из SuperJob
            if 'profession' in item and sj < number_of_vacancies:
                # Проверка ключей существование и наличие в них данных
                KIDV: object = KeyInDictVerification(item, 'SuperJob')
                # Возвращает словарь key=bool. True - ключ имеет данные
                key_bool_dict: dict = KIDV.get_key_in_dict_verification

                if KIDV.pay_key_in_dict_verification and key_bool_dict['snippet'] and key_bool_dict['url']:
                    sj += 1
                    # Формирование вакансии
                    job_dict: dict = {'name': item['profession'],
                                             'requirement': item['candidat'],
                                             'from': item['payment_from'],
                                             'to': item['payment_to'],
                                             'url': item['link']}
                    # Создает стэк с вакансиями, ячейка - экземпляр с вакансией
                    vacancy = Vacancy(job_dict)
                    if self.head_stack_vacancy:
                        self.tail_stack_vacancy.next_job = vacancy
                    else:
                        self.head_stack_vacancy = vacancy
                    self.tail_stack_vacancy = vacancy


    def search_for_job_not_experience(self, number_of_vacancies: int = 10):
        """ Метод поиска вакансий без опыта работы и запись в список """
        # Переменная для инкремента
        sj: int = 0
        for item in self.job_list:
            # Берем из SuperJob
            if 'profession' in item and sj < number_of_vacancies:
                # Проверка ключей существование и наличие в них данных
                KIDV: object = KeyInDictVerification(item, 'SuperJob')
                # Возвращает словарь key=bool. True - ключ имеет данные
                key_bool_dict: dict = KIDV.get_key_in_dict_verification

                if KIDV.pay_key_in_dict_verification and key_bool_dict['snippet'] and key_bool_dict['url'] and key_bool_dict['experience']:
                    # 1 без опыта
                    if item['experience']['id'] == 1:
                        sj += 1
                        # Формирование вакансии
                        job_dict: dict = {'name': item['profession'],
                                          'requirement': item['candidat'],
                                          'from': item['payment_from'],
                                          'to': item['payment_to'],
                                          'url': item['link']}
                        # Создает стэк с вакансиями, ячейка - экземпляр с вакансией
                        vacancy = Vacancy(job_dict)
                        if self.head_stack_vacancy:
                            self.tail_stack_vacancy.next_job = vacancy
                        else:
                            self.head_stack_vacancy = vacancy
                        self.tail_stack_vacancy = vacancy


    def search_for_job_top(self, number_of_vacancies: int = 10):
        """ Метод поиска самых оплачиваемых вакансий и запись в список """
        # Переменная для инкремента
        pay_inc: int = 0

        # Записывает список зарплат
        pay_list: list = []
        for item in self.job_list:
            if 'name' in item:
                # Проверка ключей существование и наличие в них данных
                KIDV_HH: object = KeyInDictVerification(item, 'HH')
                # Возвращает словарь key=bool. True - ключ имеет данные
                key_bool_dict: dict = KIDV_HH.get_key_in_dict_verification

                if key_bool_dict['pay_to'] and key_bool_dict['snippet'] and key_bool_dict['url'] and key_bool_dict['id']:
                    pay_list.append({'pay': item['salary']['to'], 'id': item['id']})

            if 'profession' in item:
                # Проверка ключей существование и наличие в них данных
                KIDV_SJ: object = KeyInDictVerification(item, 'SuperJob')
                # Возвращает словарь key=bool. True - ключ имеет данные
                key_bool_dict: dict = KIDV_SJ.get_key_in_dict_verification

                if key_bool_dict['pay_to'] and key_bool_dict['snippet'] and key_bool_dict['url'] and key_bool_dict['id']:
                    pay_list.append({'pay': item['payment_to'], 'id': item['id']})

        # сортировка от большего к меньшему
        pay_list_sorted: list = sorted(pay_list, key=itemgetter('pay'), reverse=True)

        while pay_inc < number_of_vacancies:
            for item in self.job_list:
                # Все вакансии приводим к единому виду
                # Берет из HH.ru
                if 'name' in item:
                    if pay_list_sorted[pay_inc]['id'] == item['id']:
                        # Убирает ненужные теги
                        requirement: str = JobProcessing.removing_characters_from_a_string(item['snippet']['requirement'])
                        # Формирование вакансии
                        job_dict: dict = {'name': item['name'],
                                          'requirement': requirement,
                                          'from': item['salary']['from'],
                                          'to': item['salary']['to'],
                                          'url': item['alternate_url']}
                        # Создает стэк с вакансиями, ячейка - экземпляр с вакансией
                        vacancy = Vacancy(job_dict)
                        if self.head_stack_vacancy:
                            self.tail_stack_vacancy.next_job = vacancy
                        else:
                            self.head_stack_vacancy = vacancy
                        self.tail_stack_vacancy = vacancy

                # Берет из SuperJob
                if 'profession' in item:
                    if pay_list_sorted[pay_inc]['id'] == item['id']:
                        # Формирование вакансии
                        job_dict: dict = {'name': item['profession'],
                                          'requirement': item['candidat'],
                                          'from': item['payment_from'],
                                          'to': item['payment_to'],
                                          'url': item['link']}
                        # Создает стэк с вакансиями, ячейка - экземпляр с вакансией
                        vacancy = Vacancy(job_dict)
                        if self.head_stack_vacancy:
                            self.tail_stack_vacancy.next_job = vacancy
                        else:
                            self.head_stack_vacancy = vacancy
                        self.tail_stack_vacancy = vacancy
            pay_inc += 1


    @property
    def print_job(self):
        """ Вывод стэка вакансий на экран"""
        vacancy: object = self.head_stack_vacancy
        print('\n')
        if vacancy is None:
            print("Отсуствуют экземпляры Vacancy.")
        while vacancy:
            print('****************************************************************************************************')
            print(f"Название вакансии: {vacancy.job['name']}")
            print(f"Требования к кандидату: {vacancy.job['requirement']}")
            pay: str = ''
            if vacancy.job['from']:
                pay = str(vacancy.job['from'])
            if vacancy.job['to']:
                pay = pay + f" - {vacancy.job['to']}"
            if pay == '':
                pay: str = "зарплата не указана"
            print(f"Зарплата: {pay}")
            print(f"Ссылка на вакансию: {vacancy.job['url']}")
            # Переход к следующему экземпляру
            vacancy = vacancy.next_job


class Vacancy:
    def __init__(self, job: dict = {}, next_job: object = None):
        """
        Узел стыка ячеек в стэке
        :param data: вакансия
        :param next: контейнер для следующего экземпляра
        """
        self.job = job
        self.next_job = next_job