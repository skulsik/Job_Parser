from Lib.GetVacancy import *
import unittest


class Test_Engine(unittest.TestCase):
    def test_class(self):
        """ Проверка отработки метода """
        self.assertEqual(Engine.get_request(), 'class Engine')

    def test_adding_job_listings_list(self):
        """ C данными """
        self.assertEqual(Engine.adding_job_listings([['rrr', 'ttt'], ['yyy', 'uuu']]), ['rrr', 'ttt', 'yyy', 'uuu'])


    def test_adding_job_listings_not_list(self):
        """ Без данных """
        self.assertEqual(Engine.adding_job_listings(), [])


class Test_HH(unittest.TestCase):
    def test_get_request(self):
        """ Проверка метода """
        HH_ru = HH('аналитик')
        HH_ru.pages = 1
        HH_ru.number_of_vacancies_at_once = 2
        HH_ru.get_request()
        hh_requests_list = HH_ru.get_job_list
        self.assertEqual(hh_requests_list[0]['name'], 'Аналитик')


class Test_SuperJob(unittest.TestCase):
    def test_get_request(self):
        """ Проверка метода """
        sj = SuperJob('аналитик')
        sj.pages = 1
        sj.number_of_vacancies_at_once = 2
        sj.get_request()
        hh_requests_list = sj.get_job_list
        self.assertEqual(hh_requests_list[0]['profession'], 'Маркетолог аналитик junior')


class Test_JobAssembly(unittest.TestCase):
    def test_get_request(self):
        """ Проверка метода """
        JA: object = JobAssembly('python')
        all_requests_list: list = JA.get_all_requests_list
        self.assertEqual(all_requests_list[0]['name'], 'Разработчик Python')
