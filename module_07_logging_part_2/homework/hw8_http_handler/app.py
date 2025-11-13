
import threading
import sys
import logging.config
import time

from utils import string_to_operator
# from logger_helper import get_logger
from logging_config import dict_config
import logging_tree

def run_server():
    from server import app
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False, threaded=True)

def send_logs():
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger("calc")
    while True:
        logger.info("Test log message")
        time.sleep(5)


logging.config.dictConfig(dict_config)

logger = logging.getLogger("calc")

with open("logging_tree.txt", "w", encoding="utf-8") as f:
    f.write(logging_tree.format.build_description())

def calc(args):
    logger.info("Arguments: %s", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.exception("Error while converting number 1", exc_info=e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.exception("Error while converting number 2", exc_info=e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info("Result: %s", result)
    logger.info("%s %s %s = %s", num_1, operator, num_2, result)


if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    logs_thread = threading.Thread(target=send_logs)
    logs_thread.daemon = True
    logs_thread.start()

    # Основной поток не ждёт завершения потоков
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")