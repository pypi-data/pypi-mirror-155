"""POC steps DELETE when complete with POC"""
from behave import use_step_matcher, when
from behave.runner import Context
from loguru import logger

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


# ------------------------------------------------------------------------
# Generic steps for context memory and variables
# ------------------------------------------------------------------------


@when("hello world is printed")
def step_hello_world(ctx: Context) -> None:
    """Hello world

    Args:
        ctx: The behave context

    """
    logger.debug("Hello World!")
