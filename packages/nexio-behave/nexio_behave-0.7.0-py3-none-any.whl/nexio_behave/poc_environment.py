"""Contains functions for the nexio-behave POC"""
from typing import Callable

from loguru import logger


def poc_setup_env(func: Callable) -> Callable:
    """Decorator for the POC for overriding environment file

    Args:
        func: The function to be called to be run through the wrapper

    """

    def wrapper() -> None:
        """Will print the line below when called"""
        func()

    return wrapper


@poc_setup_env
def print_hello_world() -> None:
    """Prints Hello World!"""
    logger.debug("Hello World!")
