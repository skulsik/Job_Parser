import os

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


class Test_ListVerification(unittest.TestCase):
    def test_ListVerification(self):
        """ Проверка метода с верными данными"""
        with self.assertRaises(TypeError):
            ListVerification()


class Test_JsonVerification(unittest.TestCase):
    def test_JsonVerification(self):
        """ Проверка метода с неверными данными"""
        with self.assertRaises(TypeError):
            JsonVerification([{8768998}])


class Test_FileDateVerification(unittest.TestCase):
    def test_FileDateVerification(self):
        """ Проверка метода с верными данными """
        fdv = FileDateVerification()
        self.assertEqual(fdv.get_file_date, False)


class Test_KeyInDictVerification(unittest.TestCase):
    def test_KeyInDictVerification_HH(self):
        """ Проверка метода с верными данными """
        item = {'snippet': {'requirement': 'gfdgfd'}, 'salary': {'from': 999, 'to': 777}, 'alternate_url': 'jghfdj', 'id': 54654}
        HH = KeyInDictVerification(item, 'HH')
        self.assertEqual(HH.pay_key_in_dict_verification, True)
        self.assertEqual(HH.get_key_in_dict_verification['snippet'], True)
        self.assertEqual(HH.get_key_in_dict_verification['pay_from'], True)
        self.assertEqual(HH.get_key_in_dict_verification['pay_to'], True)
        self.assertEqual(HH.get_key_in_dict_verification['url'], True)
        self.assertEqual(HH.get_key_in_dict_verification['id'], True)


    def test_KeyInDictVerification_SuperJob(self):
        """ Проверка метода с верными данными """
        item = {'candidat': 'fdshgfhgf', 'payment_from': 888, 'payment_to': 777, 'link': 'jghfdj', 'id': 54654, 'experience': {'id': 454}}
        SJ = KeyInDictVerification(item, 'SuperJob')
        self.assertEqual(SJ.pay_key_in_dict_verification, True)
        self.assertEqual(SJ.get_key_in_dict_verification['snippet'], True)
        self.assertEqual(SJ.get_key_in_dict_verification['pay_from'], True)
        self.assertEqual(SJ.get_key_in_dict_verification['pay_to'], True)
        self.assertEqual(SJ.get_key_in_dict_verification['url'], True)
        self.assertEqual(SJ.get_key_in_dict_verification['id'], True)
        self.assertEqual(SJ.get_key_in_dict_verification['experience'], True)
