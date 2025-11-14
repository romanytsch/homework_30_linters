import logging
from logger_helper import LevelFileHandler, ASCIIOnlyFilter
from logging.handlers import TimedRotatingFileHandler, HTTPHandler

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
        },
        "http": {
            "class": "logging.handlers.HTTPHandler",
            "host": "localhost:5001",
            "url": "/log",
            "method": "POST",
            "formatter": "base"
        }
    },
    "loggers": {
        "calc": {
            "level": "DEBUG",
            "handlers": ["file", "http"],
            "propagate": False
        },
        "utils": {
            "level": "INFO",
            "handlers": ["utils_timed_handler", "http"],
            "propagate": False
        }
    },
    "root": {
        "level": "WARNING",
        "handlers": ["file", "http"]
    }
}