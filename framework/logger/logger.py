import logging
import os
from logging.handlers import RotatingFileHandler

from framework.logger.logger_config import LoggerConfig


class Logger:
    """
    Class with configure logger and methods for edit logger configuration
    """
    if not os.path.isdir(LoggerConfig.LOGS_DIR_NAME):
        os.makedirs(LoggerConfig.LOGS_DIR_NAME)
    __logger = logging.getLogger(LoggerConfig.LOGGER_NAME)
    __logger.setLevel(LoggerConfig.LOGS_LEVEL)
    __handler = RotatingFileHandler(LoggerConfig.LOGS_FILE_NAME, maxBytes=LoggerConfig.MAX_BYTES,
                                    backupCount=LoggerConfig.BACKUP_COUNT)
    __logger.addHandler(__handler)

    @staticmethod
    def set_level(level: int):
        """
        Sets logger level
        :param level(str, int): one of CRITICAL = 50, FATAL = CRITICAL, ERROR = 40, WARNING = 30,
                                        WARN = WARNING, INFO = 20, DEBUG = 10, NOTSET = 0
        :return: None
        """
        Logger.__logger.setLevel(level)

    @staticmethod
    def info(message: str):
        """
        Logs message with level=INFO
        :param message(str): message to log
        :return: None
        """
        Logger.__logger.info(msg=message)

    @staticmethod
    def debug(message: str):
        """
        Logs message with level=DEBUG
        :param message(str): message to log
        :return: None
        """
        Logger.__logger.debug(msg=message)

    @staticmethod
    def warning(message: str):
        """
        Logs message with level=WARNING
        :param message(str): message to log
        :return: None
        """
        Logger.__logger.warning(msg=message)

    @staticmethod
    def error(message: str):
        """
        Logs message with level=ERROR
        :param message(str): message to log
        :return: None
        """
        Logger.__logger.error(msg=message)

    @staticmethod
    def fatal(message: str):
        """
        Logs message with level=INFO
        :param message(str): message to log
        :return: None
        """
        Logger.__logger.fatal(msg=message)

    @staticmethod
    def step(message: str):
        """
        Logs message with level=STEP
        :param message(str): message to log
        :return: None
        """
        Logger.__logger.info(msg=message)
