""" Config серверного логгера. """

import sys
import os
import logging.handlers
from pack_server.common import LOGGING_LEVEL
sys.path.append('../../')

# Создание формировщика логов.
SERVER_FORMATTER = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования.
# PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.getcwd()
PATH = os.path.join(PATH, 'server.log')

# Создание потоков вывода логов.
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(
    PATH, encoding='utf-8', interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

# Создание и настройка регистратора.
LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# Отладка.
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка!!!')
    LOGGER.error('Ошибка!')
    LOGGER.warning('Предупреждение!')
    LOGGER.debug('Отладочная информация.')
    LOGGER.info('Информационное сообщение.')
