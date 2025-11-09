import logging
import subprocess
import shlex


KERNEL_VERSION = None

utils_logger = logging.getLogger('logger_utils.subprocess_utils')
utils_logger.setLevel('DEBUG')

def get_kernel_version() -> str:
    utils_logger.info('Start calling subprocess')
    command = shlex.split('uname -a')
    global KERNEL_VERSION
    if KERNEL_VERSION is None:
        utils_logger.debug('Kernel version is not defined. Start subprocess call')
        try:
            out = subprocess.run(command, capture_output=True, encoding='utf-8')
        except Exception as e:
            utils_logger.exception(e)
            raise e
        KERNEL_VERSION = out.stdout.strip()
        utils_logger.debug('Kernel version: {}'.format(KERNEL_VERSION))
    utils_logger.info('Return kernel version')
    return KERNEL_VERSION
