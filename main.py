from Lib.GetVacancy import *
from Lib.JobProcessing import JobProcessing
from Lib.User import User
from Lib.Verification import FileDateVerification


print('Вас приветствует Парсер вакансий! В фунционале ведется работа с HH.ru и SuperJob.\n(Вы пользуетесь ограниченной версией, для покупки расширенной пишите на skulsik1@gmail.com)\n')

# Создает объект - работа с пользователем
user_obj: object = User()
# Проверка существования файла, если существует - проверка на свежесть 24часа
file_date: object = FileDateVerification()

user_name: str = ''
job_name: str = ''

# Проверка на существование пользователя
if os.path.exists('data/user.txt'):
    # Чтение имени пользователя и последней просмторенной вакансии
    user_obj.read_user_info()
    user_name = user_obj.get_user_name
    job_name = user_obj.get_job_name

    print(f'Привет {user_name}! Последний раз ты искал(а) вакансию: {job_name}.')
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
    user_name = input('Введите ваше имя: ')
    if user_name == '':
        user_name = 'Дорогой друг'
    job_name = input(f'Какую вакансию {user_name}, ты хотел(а) бы найти: ')

    # Запись имени и вакансии в фаил
    user_obj.write_user_info(user_name, job_name)

input_command: str = ''
while input_command != 'exit':
    # Создает объект - работа с фаилом
    job_processing: object = JobProcessing()

    if input_command != job_name and input_command != '':
        # Присваивает новую вакансию
        input_command = input_command.lower()
        job_name = input_command
        if input_command == 'all':
            job_name = ''
        # Флаг на поиск новых вакансий и запись в фаил
        file_date.file_date = True
        # Запись имени и вакансии в фаил
        user_obj.write_user_info(user_name, job_name)

    # Если файла не существует или существует, но ему больше 24 часов,
    # либо флаг True в случае изменения названия вакансии: выполняется считывание вакансий и запись их в фаил.
    if file_date.get_file_date:
        print('\nПожалуйста, подождите! Обновление вакансий...')
        # Делает сборку классов разных сайтов в один и возвращает один список вакансий
        JA: object = JobAssembly(job_name)
        all_requests_list: list = JA.get_all_requests_list

        # Запись полученных данных о вакансиях в фаил
        job_processing.recording_job_in_the_file(all_requests_list)


    # Запрос на количество выводимых вакансий
    number_of_vacancies: str = input(f'{user_name}, введи количество вакансий, которое нужно вывести на экран(по умолчанию 10 вакансий - enter):')
    if number_of_vacancies == '':
        number_of_vacancies = 10
    else:
        number_of_vacancies = int(number_of_vacancies)

    # Запрос на формат выдаваемых вакансий
    job_parameters: str = input(f'{user_name}, введи команду: enter - последние вакансии, top - 10 самых оплачиваемых вакансий, experience - вакансии без опыта: ')

    # Чтение фаила с вакансиями
    job_processing.read_file_job()

    # Возвращает последнии вакансии
    if job_parameters == '':
        job_processing.search_for_job(number_of_vacancies)

    # Возвращает вакансии без опыта работы
    if job_parameters == 'experience':
        job_processing.search_for_job_not_experience(number_of_vacancies)

    # Возвращает самые высокооплачиваемые
    if job_parameters == 'top':
        job_processing.search_for_job_top(number_of_vacancies)

    # Вывод вакансий
    job_processing.print_job

    input_command = input('\nПосмотьреть другую вакансию - введи вакансию, посмотреть все вакансии - введи all, продолжить - введи enter, выход - введи exit: ')

