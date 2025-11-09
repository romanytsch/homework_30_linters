
from typing import Union, Callable
from operator import sub, mul, truediv, add
from logger_helper import get_logger


OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]

logger = get_logger("utils")

def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        logger.debug("wrong operator type: %s", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.debug("wrong operator value: %s", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]
