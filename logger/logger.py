import logging
import os
import sys

from logger.singleton import Singleton


class Logger(metaclass=Singleton):
    """
    Logger class
    """

    # Setting path for log file
    current_path = os.path.dirname(__file__)
    root = os.path.abspath(os.path.join(current_path, "../"))

    LOG_FILE = os.path.join(root, "testing.log")

    sys.path.insert(0, root)

    def __init__(self):
        """
        Default logger
        """
        # Setting up logger file and encoding
        file_log_handler = logging.FileHandler(Logger.LOG_FILE, "w", encoding="UTF-8")
        # Setting up formatter for log
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_log_handler.setFormatter(formatter)
        self.logger = logging.getLogger(Logger.LOG_FILE)
        self.logger.addHandler(file_log_handler)
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        """
        Get default logger
        :return: logger
        """
        return self.logger
