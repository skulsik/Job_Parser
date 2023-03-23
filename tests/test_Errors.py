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


class Test_APIKeyError(unittest.TestCase):
    def test_APIKeyError_not_message(self):
        """ Проверка метода без данных """
        APIKeyError()
        self.assertEqual(APIKeyError.NotError, 'APIKeyError: Неизвестная ошибка.')


    def test_APIKeyError_message(self):
        """ Проверка метода с данными """
        APIKeyError('error')
        self.assertEqual(APIKeyError.NotError, 'error')


class Test_HTTPError(unittest.TestCase):
    def test_HTTPError_not_message(self):
        """ Проверка метода без данных """
        HTTPError()
        self.assertEqual(HTTPError.NotError, 'HTTPError: Неизвестная ошибка.')


    def test_Request_Error_message(self):
        """ Проверка метода с данными """
        HTTPError('error')
        self.assertEqual(HTTPError.NotError, 'error')


class Test_NameKeyError(unittest.TestCase):
    def test_NameKeyError_not_message(self):
        """ Проверка метода без данных """
        NameKeyError()
        self.assertEqual(NameKeyError.NotError, 'NameKeyError: Неизвестная ошибка.')


    def test_NameKeyError_message(self):
        """ Проверка метода с данными """
        NameKeyError('error')
        self.assertEqual(NameKeyError.NotError, 'error')
