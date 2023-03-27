from Lib.User import User
import unittest


class Test_User(unittest.TestCase):
    def test_User_name(self):
        """ Проверка метода """
        user = User()
        user.read_user_info()
        self.assertEqual(user.get_user_name, 'Алексей')


    def test_User_job(self):
        """ Проверка метода """
        user = User()
        user.read_user_info()
        self.assertEqual(user.get_job_name, 'python')


    def test_User_write(self):
        """ Проверка метода """
        user = User()
        user.write_user_info('Алексей', 'python')
        user.read_user_info()
        self.assertEqual(user.get_job_name, 'python')
        self.assertEqual(user.get_user_name, 'Алексей')
