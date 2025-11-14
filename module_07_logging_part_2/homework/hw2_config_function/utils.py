import logging
import sys
from typing import Union, Callable
from operator import sub, mul, truediv, add

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]

logger = logging.getLogger("utils")

def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        logger.debug("wrong operator type %s", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.debug("wrong operator value %s", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
