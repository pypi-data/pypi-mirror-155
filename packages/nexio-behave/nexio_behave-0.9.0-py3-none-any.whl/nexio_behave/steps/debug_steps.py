"""Generic step definitions for behave debugging"""
import pdb

from behave import step, use_step_matcher
from behave.runner import Context
from loguru import logger

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


@step("set pdb")
def step_debug_pdb(ctx: Context) -> None:
    """Sets a pdb to be used for debugging.

    The gherkin-linter will catch this step to prevent a pdb being pushed.
    Multiple if statements log everything a dev would need to start debugging the issue.

    Args:
        ctx: The behave context object

    """
    logger.debug(
        "Behave PDB step was set. Current context attributes broken down by context layer:"
    )
    pdb.set_trace()
