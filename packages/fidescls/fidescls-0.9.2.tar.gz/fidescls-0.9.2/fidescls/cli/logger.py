"""
Configure the python logger for the fidescls cli
"""

import logging
from logging.handlers import RotatingFileHandler
from fidescls.cli import config as _conf


def config_logger(logging_level: str = "DEBUG") -> logging.Logger:
    """
    Create and configure a logger that creates a rotating log file
    Args:
        logging_level: string for the logging level to be used

    Returns:
        python logger with a rotating file handler
    """
    logger = logging.getLogger(_conf.LOGGER_NAME)
    logger.setLevel(logging_level)

    handler = RotatingFileHandler(_conf.LOG_FILENAME, maxBytes=int(50e6), backupCount=1)
    handler.setLevel(logging_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    return logger
