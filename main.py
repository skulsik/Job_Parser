from Lib.GetVacancy import *
from Lib.Errors import Error
from Lib.JobProcessing import JobProcessing
from Lib.User import User
from Lib.Verification import FileDateVerification
import json # Убрать


print('Вас приветствует Парсер вакансий! В фунционале ведется работа с HH.ru и SuperJob.\n(Вы пользуетесь ограниченной версией, для покупки расширенной пишите на skulsik1@gmail.com)\n')

# Создает объект - работа с пользователем
user_obj: object = User()
# Создает объект - работа с фаилом
job_processing: object = JobProcessing()
# Проверка существования файла, если существует - проверка на свежесть 24часа
file_date: object = FileDateVerification()

# Проверка на существование пользователя
if os.path.exists('data/user.txt'):
    # Чтение имени пользователя и последней просмторенной вакансии
    user_obj.read_user_info()
    user_name: str = user_obj.get_user_name
    job_name: str = user_obj.get_job_name

    print(f'Привет {user_name}! Последний раз ты искал(а) вакансию: {job_name}')
    job_new_name: str = input(f'Продолжить поиск вакансий, по запросу {job_name}? (enter-да, либо название новой, команда all - все вакансии): ')
    job_new_name = job_new_name.lower()
    if job_new_name != '':
        job_name = job_new_name
        if job_new_name == 'all':
            job_name = ''
        # Флаг на поиск новых вакансий и запись в фаил
        file_date.file_date = True
        # Запись имени и вакансии в фаил
        user_obj.write_user_info(user_name, job_name)
else:
    # Спрашивает имя и вакансию
    user_name: str = input('Введите ваше имя: ')
    if user_name == '':
        user_name = 'Дорогой друг'
    job_name: str = input(f'Какую вакансию {user_name}, ты хотел(а) бы найти: ')

    # Запись имени и вакансии в фаил
    user_obj.write_user_info(user_name, job_name)

# Если фаила не существует или существует но ему больше 24 часов,
# либо флаг True в случае изменения названия вакансии: выполняется считывание вакансий и запись их в фаил.
if file_date.get_file_date:
    # Делает сборку классов разных сайтов в один и возвращает один список вакансий
    JA: object = JobAssembly(job_name)
    all_requests_list: list = JA.get_all_requests_list

    # Запись полученных данных о вакансиях в фаил
    job_processing.recording_job_in_the_file(all_requests_list)

# Запрос вакансий по названию вакансии
job_processing.job_request(job_name)
