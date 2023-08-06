""" Дескриптор. Инициализиция логера
метод определения модуля, источника запуска."""
import logging
import sys
import re

file = sys.argv[0]
if re.search(r'(server)', file):
    Logger = logging.getLogger('server')
else:
    Logger = logging.getLogger('client')


class Port:
    """ Класс - дескриптор для номера порта.
        Позволяет использовать только порты с 1023 по 65536. При попытке
        установить неподходящий номер порта генерирует исключение."""

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            Logger.critical(
                f'Попытка запуска с указанием неподходящего порта {value}.'
                f' Допустимы адреса с 1024 до 65535.')
            raise TypeError('Некорректрый номер порта')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
