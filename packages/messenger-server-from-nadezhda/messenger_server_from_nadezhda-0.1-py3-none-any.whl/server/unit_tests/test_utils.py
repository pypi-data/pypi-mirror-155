""" Unit-Тесты утилит """
import sys
import os
import unittest
import json

from pack_server.common.utils import send_message, get_message
from pack_server.common import ENCODING, ACTION, PRESENCE, USER, TIME, \
    ACCOUNT_NAME, RESPONSE, ERROR

sys.path.append(os.path.join(os.getcwd(), '../../..'))


class TestSocket:
    """ Тестовый класс для тестирования отправки и получения сообщения
    при создании требует словарь, который будет прогоняться
    через тестовую функцию. """

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """ Тестовая функция отправки данных, корректно кодирует сообщение,
            так же сохраняет то, что должно было отправиться в сокет. """
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(
            ENCODING)  # Кодируем сообщение
        # Сохраняем то, что должно было отправиться в сокет
        self.received_message = message_to_send

    def recv(self, max_len):
        """ Получаем данные из сокета. """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


""" Тестовый класс выполняющий тестирование. """


class Tests(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: "test_test"
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    """ Тестирование корректности работы функции отправки,для этого создаем тестовый сокет
    и проверяем корректность отправки словаря. """

    def test_send_message(self):
        # экземпляр тестового словаря хранит - словарь.
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой функции, результат в тестовом сокете
        send_message(test_socket, self.test_dict_send)
        # Проверка корректности кодирования словаря.
        self.assertEqual(
            test_socket.encoded_message,
            test_socket.received_message)
        # Дополнительная проверка, если на входе не словарь
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    """ Тест функции приема сообщения. """

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # Тест коректной расшифровки коректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)
        # Тест- корректная расшифровка ошибочного словаря ???
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
