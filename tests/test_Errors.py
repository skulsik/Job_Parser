from Lib.Errors import *
import unittest


class Test_Error(unittest.TestCase):
    def test_Error_(self):
        """ Проверка метода """
        self.assertEqual(Error.NotError, None)


class Test_RequestError(unittest.TestCase):
    def test_Request_Error_not_message(self):
        """ Проверка метода без данных"""
        RequestError()
        self.assertEqual(RequestError.NotError, 'RequestError: Неизвестная ошибка.')


    def test_Request_Error(self):
        """ Проверка метода без данных"""
        RequestError(400)
        self.assertEqual(RequestError.NotError, 'RequestError: Ошибка клиента.')
