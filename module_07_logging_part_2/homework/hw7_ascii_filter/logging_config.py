import logging
from logger_helper import LevelFileHandler, ASCIIOnlyFilter
from logging.handlers import TimedRotatingFileHandler

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "filters": {
        "ascii_only": {
            "()": "logging_config.ASCIIOnlyFilter"
        }
    },
    "handlers": {
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["ascii_only"]
        },
        "utils_timed_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": "utils.log",
            "when": "h",
            "interval": 10,
            "backupCount": 1,
            "encoding": "utf-8",
            "filters": ["ascii_only"]
        }
    },
    "loggers": {
        "calc": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False
        },
        "utils": {
            "level": "INFO",
            "handlers": ["utils_timed_handler"],
            "propagate": False
        }
    },
    "root": {
        "level": "WARNING",
        "handlers": ["file"]
    }
}