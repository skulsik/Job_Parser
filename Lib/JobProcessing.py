from Lib.Verification import *
import json


class JobProcessing:
    # Путь к файлу вакансий json
    path_file_json: str = 'data/job.json'


    def __init__(self):
        """ Инициализация свойств """
        # Название профессии
        self.name_job: str = ''
        # Ссылка на вакансию
        self.url_job: str = ''
        # Описание профессии
        self.job_description: str = ''
        # Зарплата
        self.pay: int = 0


    def recording_job_in_the_file(self, job_list: list = None):
        """ Запись в фаил списка вакансий """
        # Проверка на передачу пустого списка
        ListVerification(job_list)

        job_list = json.dumps(job_list, indent=2, ensure_ascii=False)

        # Получаем дескриптор фаила
        fd = os.open(self.path_file_json, os.O_WRONLY | os.O_CREAT)

        # Превратить в настоящий файл
        with open(fd, mode='w', encoding='UTF-8', closefd=False) as file:
            file.write(job_list)

        # Закрываем дескриптор файла
        os.close(fd)


    def job_request(self, job_name: str = ''):
        print('uraaa')


    def get_job(self):
        pass
