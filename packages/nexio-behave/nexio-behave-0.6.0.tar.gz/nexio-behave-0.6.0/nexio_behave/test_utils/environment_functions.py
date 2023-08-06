"""Functions for globally common environment actions used by before and after behave hooks

Keeping this file clean with only global functions is very important for dependency management.
We do not want to load dependencies in test environments that are not needed. Specific functions for
very specific actions should be kept somewhere else.
"""
from behave.runner import Context
from loguru import logger


def setup_logging(ctx: Context) -> None:
    """Sets up logging for the behave logger using loguru

    Args:
        ctx: The behave context

    """
    pass


def initialize_context_variables(ctx: Context) -> None:
    """Initializes variables on the behave context

    Args:
        ctx: The behave context

    """
    # Start the framework with these variables set
    ctx.headers = {}


def reset_context_vars(ctx: Context) -> None:
    """Resets a few context vars that should be cleared

    Args:
        ctx: The behave context

    """
    logger.debug("Resetting context vars")
    ctx.headers = {}
    logger.debug("Context vars successfully reset")


def set_user_data(ctx: Context) -> None:
    """Retrieves behave user data from the behave.ini and saves it to the context

    Args:
        ctx: The behave context

    """
    logger.debug("Setting user data from the behave.ini or environment variables")
    user_data = ctx.config.userdata
    ctx.base_url = user_data.get("base_url", "http://localhost")
    ctx.environment = user_data.get("environment", "local")
    logger.debug(f"User data from configs and environment variables: {user_data}")
