import logging
from logger_helper import LevelFileHandler

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base"
        }
    },
    "loggers": {
        "calc": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False
        }
    },
    "root": {
        "level": "WARNING",
        "handlers": ["file"]
    }
}