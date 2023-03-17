from utils.utils import *
import unittest


class Test_Engine(unittest.TestCase):
    def test_class(self):
        self.assertEqual(Engine.get_request(), 'class Engine')


class Test_HH(unittest.TestCase):
    def test_get_request(self):
        """

        :return:
        """
        HH_ru = HH('аналитик')
        HH_ru.pages = 1
        HH_ru.number_of_vacancies_at_once = 2
        hh_requests_list = HH_ru.get_request()
        self.assertEqual(hh_requests_list[0]['name'], 'Аналитик')


class Test_SuperJob(unittest.TestCase):
    def test_get_request_api_key_error(self):
        """
        Проверка c неверно введеным ключем, либо ключ отсутствует в переменных окружениях
        :return:
        """
        sj = SuperJob()
        sj.name_of_the_environment_variable = ''
        with self.assertRaises(ValueError):
            sj.get_request()


    def test_get_request(self):
        """

        :return:
        """
        sj = SuperJob('аналитик')
        sj.pages = 1
        sj.number_of_vacancies_at_once = 2
        hh_requests_list = sj.get_request()
        self.assertEqual(hh_requests_list[0]['profession'], 'Консультант-аналитик 1С')
