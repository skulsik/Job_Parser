class User:
    # Путь к фаилу
    path = "data/user.txt"


    def __init__(self):
        """ Инициализация свойств """
        # Имя пользоваетля
        self.name: str = ''
        # Последняя просмотренная вакансия
        self.job: str = ''


    def read_user_info(self):
        """ Чтение имени и вакансии """
        with open(self.path, mode='r', encoding='UTF-8') as file:
            for info in file:
                info_list: list = info.split('=')
                if 'name' == info_list[0]:
                    self.name = info_list[1].strip()
                if 'job' == info_list[0]:
                    self.job = info_list[1].strip()


    def write_user_info(self, name: str, job: str = ''):
        """ Запись имени пользователя и вакансии в фаил """
        with open(self.path, mode='w', encoding='UTF-8') as file:
            file.write(f'name={name}\njob={job}')


    @property
    def get_user_name(self) -> str:
        """
        :return: Имя пользователя
        """
        return self.name


    @property
    def get_job_name(self) -> str:
        """
        :return: Имя вакансии
        """
        return self.job
