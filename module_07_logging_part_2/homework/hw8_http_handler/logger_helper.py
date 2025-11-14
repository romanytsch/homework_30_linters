import logging
import sys


class LevelFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.files = {
            logging.DEBUG: open('calc_debug.log', 'a', encoding='utf-8'),
            logging.INFO: open('calc_info.log', 'a', encoding='utf-8'),
            logging.WARNING: open('calc_warning.log', 'a', encoding='utf-8'),
            logging.ERROR: open('calc_error.log', 'a', encoding='utf-8'),
            logging.CRITICAL: open('calc_critical.log', 'a', encoding='utf-8'),
        }

    def emit(self, record):

        if record.levelno == logging.CRITICAL:
            file = self.files[logging.CRITICAL]
        elif record.levelno == logging.ERROR:
            file = self.files[logging.ERROR]
        elif record.levelno == logging.WARNING:
            file = self.files[logging.WARNING]
        elif record.levelno == logging.INFO:
            file = self.files[logging.INFO]
        elif record.levelno == logging.DEBUG:
            file = self.files[logging.DEBUG]

        msg = self.format(record)
        file.write(msg + '\n')
        file.flush()

    def close(self):
        for f in self.files.values():
            f.close()
        super().close()

class ASCIIOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().isascii()

