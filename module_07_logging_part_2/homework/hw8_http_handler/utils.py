
from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging


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
        logger.debug("wrong operator type: %s", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.debug("wrong operator value: %s", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]

