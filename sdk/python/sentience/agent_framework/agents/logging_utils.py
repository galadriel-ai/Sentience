import logging
import os
from logging import DEBUG
from logging import INFO

from pythonjsonlogger import jsonlogger

GALADRIEL_NODE_LOGGER = "galadriel_agent"

LOG_FILE_PATH = "logs/logs.log"
LOGGING_MESSAGE_FORMAT = "%(asctime)s %(name)-12s %(levelname)s %(message)s"


def init_logging(debug: bool):
    log_level = DEBUG if debug else INFO
    file_handler = get_file_logger()
    console_handler = get_console_logger()
    logger = logging.getLogger(GALADRIEL_NODE_LOGGER)
    logger.setLevel(log_level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    apply_default_formatter(file_handler)
    apply_default_formatter(console_handler)
    logger.propagate = False


def get_file_logger() -> logging.FileHandler:
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_console_logger() -> logging.StreamHandler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def apply_default_formatter(handler: logging.Handler):
    formatter = jsonlogger.JsonFormatter(LOGGING_MESSAGE_FORMAT)
    handler.setFormatter(formatter)


def get_agent_logger():
    return logging.getLogger(GALADRIEL_NODE_LOGGER)
