# """ Тестирование сервера. """
# import unittest
#
# from common.variables import RESPONSE, ERROR, TIME, USER, ACCOUNT_NAME, \
#     ACTION, PRESENCE
# from server import process_client_message
#
#
# class TestServer(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     err_dict = {
#         RESPONSE: 400,
#         ERROR: 'Bad Request'
#     }
#     ok_dict = {RESPONSE: 200}
#
#     # Тест-ошибка, если нет действия
#     def test_no_action(self):
#         self.assertEqual(process_client_message(
#             {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)
#
#     # Тест-ошибка, если действие не корректное
#     def test_wrong_action(self):
#         self.assertEqual(process_client_message(
#             {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}),
#             self.err_dict)
#
#     # Тест на наличие штампа времени
#     def test_no_time(self):
#         self.assertEqual(process_client_message(
#             {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)
#
#     # Тест на наличие пользователя
#     def test_no_user(self):
#         self.assertEqual(process_client_message(
#             {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)
#
#     # Тест неизвестный пользователь
#     def test_unknown_user(self):
#         self.assertEqual(process_client_message(
#             {ACTION: PRESENCE, TIME: 1.1,
#              USER: {ACCOUNT_NAME: 'Guest1'}}),
#             self.err_dict)
#
#     # Тест на корректный запрос
#     def test_ok_check(self):
#         self.assertEqual(process_client_message(
#             {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
#             self.ok_dict)
#
#     def tearDown(self):
#         pass
#
#
# if __name__ == '__main__':
#     unittest.main()

# разобраться почему где-то TIME: 1.1 а где-то TIME: '1.1' ???????????????
