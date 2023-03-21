from Lib.Verification import *
import unittest


class Test_RequestVerification(unittest.TestCase):
    def test_Request_Verification_not_http(self):
        """ Проверка метода без ввода данных """
        with self.assertRaises(SystemExit):
            RequestVerification()


    def test_Request_Verification_http(self):
        """ Проверка метода с неверными данными """
        with self.assertRaises(SystemExit):
            RequestVerification('https://api.superjob.ru/2.0/vacancies/')


class Test_APIKeyVerification(unittest.TestCase):
    def test_API_Key_Verification(self):
        """ Проверка метода с верными данными"""
        api_key = os.getenv('SuperJobKey')
        self.assertEqual(str(APIKeyVerification('SuperJobKey')), api_key)


    def test_API_Key_Verification_not_key(self):
        """ Проверка метода с непереданным ключем """
        with self.assertRaises(SystemExit):
            APIKeyVerification()


    def test_API_Key_Verification_error_key(self):
        """ Проверка метода с неправильным переданным ключем """
        with self.assertRaises(SystemExit):
            APIKeyVerification('hjfdshgfjd')
