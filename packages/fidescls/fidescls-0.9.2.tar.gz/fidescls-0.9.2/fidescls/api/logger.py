# pylint: skip-file
"""
Configure the python logger
"""
import logging
from logging.handlers import RotatingFileHandler

from fidescls.api import config as _aconf


def config_logger(logging_level: str = "DEBUG") -> logging.Logger:
    """
    Create and configure a logger that creates a rotating log file
    Args:
        logging_level: string for the logging level to be used

    Returns:
        python logger with a rotating file handler
    """
    logger = logging.getLogger(_aconf.LOGGER_NAME)
    logger.setLevel(logging_level)

    handler = RotatingFileHandler(
        _aconf.LOG_FILENAME, maxBytes=int(50e6), backupCount=1
    )
    handler.setLevel(logging_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    return logger
