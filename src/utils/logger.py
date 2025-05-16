import os
import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, chat_id: int, question_id: int, log_level: int=logging.INFO):
        self.logger = logging.getLogger(str(question_id))
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            log_file = os.path.join(f"./logs/{chat_id}", f"{question_id}.log")

            file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8")
            console_handler = logging.StreamHandler()

            formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def critical(self, message: str):
        self.logger.critical(message)
