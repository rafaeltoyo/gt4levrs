import logging
import sys
import multiprocessing_logging
from logging.handlers import TimedRotatingFileHandler

from ..file_utils import get_absolute_path

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_DIRECTORY = get_absolute_path("src/logs/")
LOG_EXTENSION = ".log"
multiprocessing_logging.install_mp_handler()


class LoggingManager:

    @staticmethod
    def get_console_handler():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler

    @staticmethod
    def get_file_handler(logger_name):
        log_file = LOG_DIRECTORY + logger_name + LOG_EXTENSION
        file_handler = TimedRotatingFileHandler(log_file, when='midnight')
        file_handler.setFormatter(FORMATTER)
        return file_handler

    @staticmethod
    def get_logger(logger_name, logging_level=logging.DEBUG):
        logger = logging.getLogger(logger_name)

        if not logger.hasHandlers():
            logger.addHandler(LoggingManager.get_console_handler())
            logger.addHandler(LoggingManager.get_file_handler(logger_name))
            # with this pattern, it's rarely necessary to propagate the error up to parent
            logger.propagate = False

            logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
            logging_level_name = str(logging.getLevelName(logging_level))
            logger.info("Creating logger with name " + str(logger_name) + " and level " + logging_level_name)
            logger.setLevel(logging_level)  # better to have too much log than not enough

        return logger
