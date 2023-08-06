"""Step definitions for header assertions"""
from distutils.util import strtobool
from typing import Any, Dict, Optional

from behave import then, use_step_matcher
from behave.runner import Context
from loguru import logger

from nexio_behave.utils.assertions import ValueEqualsAssertion, ValueNotEqualsAssertion
from nexio_behave.utils.common_behave_functions import interpolate_context_attributes

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


@then(
    'the JSON stored at "(?P<key>.*)" should (?P<negate>not )?be the following(?::|)?'
)
def step_assert_json_context_variable(ctx: Context, key: str, negate: str) -> None:
    """Assert that JSON stored as request data is as expected

    Args:
        ctx: The behave context
        key: The context key the JSON is stored at
        negate: A string representing whether to assert the negated

    """
    expected_request_data: Dict[str, Any] = {}
    for row in ctx.table:
        value = interpolate_context_attributes(ctx, row[1])
        if value.isdigit():
            # If value is a digit cast to int
            expected_request_data[row[0]] = int(value)
        elif get_bool(value) is not None:
            expected_request_data[row[0]] = get_bool(value)
        else:
            expected_request_data[row[0]] = value
    if negate:
        ValueNotEqualsAssertion(expected_request_data, getattr(ctx, key))
        logger.debug(
            f"Asserting that the JSON stored at {key} is not: {expected_request_data}"
        )
    else:
        logger.debug(
            f"Asserting that the JSON stored at {key} is: {expected_request_data}"
        )
        ValueEqualsAssertion(expected_request_data, getattr(ctx, key))


# ------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------


def get_bool(value: str) -> Optional[bool]:
    """Try to cast a string to a boolean

    Args:
        value: String value to cast

    Returns:
        boolean or None if the string could not be cast

    """
    try:
        return bool(strtobool(value))
    except ValueError:
        return None
