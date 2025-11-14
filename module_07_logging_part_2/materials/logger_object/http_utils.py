import logging
import time

import requests

utils_logger = logging.getLogger('logger_utils.http_utils')
utils_logger.setLevel('INFO')

GET_IP_URL = 'https://api.ipify.org?format=json'


def get_ip_address() -> str:
    utils_logger.debug('Start getting IP address')
    start = time.time()
    try:
        ip = requests.get(GET_IP_URL).json()['ip']
    except Exception as e:
        utils_logger.exception(e)
        raise e
    utils_logger.debug('Done requesting ip in {:.4f} seconds'.format(time.time() - start))
    utils_logger.info('Ip address: {}'.format(ip))
    return ip
