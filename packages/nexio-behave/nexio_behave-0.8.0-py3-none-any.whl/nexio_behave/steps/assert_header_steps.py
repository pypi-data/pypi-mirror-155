"""Step definitions for header assertions"""
from behave import then, use_step_matcher
from behave.runner import Context
from loguru import logger

from nexio_behave.utils.assertions import (
    ValueEqualsAssertion,
    ValueIsEmptyAssertion,
    ValueIsNotEmptyAssertion,
    ValueNotEqualsAssertion,
)
from nexio_behave.utils.common_behave_functions import interpolate_context_attributes

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


@then('the request header at "(?P<key>.*)" should (?P<negate>not )?be "(?P<value>.*)"')
def step_assert_request_header(ctx: Context, key: str, negate: str, value: str) -> None:
    """Checks if the request header at a key is a given value

    Args:
        ctx: the behave context
        key: The key in the header dict
        negate: A string representing whether a response should be negated
        value: The value expected as the header

    """
    headers = ctx.headers
    if negate:
        logger.debug(f"Asserting request header {key} is {negate}{value}")
        ValueNotEqualsAssertion(value, headers[key])
    else:
        logger.debug(f"Asserting request header {key} is {value}")
        ValueEqualsAssertion(value, headers[key])


@then("the request headers should (?P<negate>not )?be the following(?::|)?")
def step_assert_request_headers(ctx: Context, negate: str) -> None:
    """Checks if the request headers have the proper values

    Table Example:
        | header_name | header_value |

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        step_assert_request_header(ctx, row[0], negate, row[1])


@then('the request header at "(?P<key>.*)" should (?P<negate>not )?be None')
def step_assert_request_header_null(ctx: Context, key: str, negate: str) -> None:
    """Checks if the request header at a key is a given value

    Args:
        ctx: the behave context
        key: The key in the header dict
        negate: A string representing whether a response should be negated

    """
    headers = ctx.headers
    if negate:
        logger.debug(f"Asserting request header {key} is {negate}None")
        ValueIsEmptyAssertion("None", headers[key])
    else:
        logger.debug(f"Asserting request header {key} is None")
        ValueIsNotEmptyAssertion("None", headers[key])


@then("there should (?P<negate>not )?be (?P<header_count>[0-9]) headers")
def step_assert_request_header_count(
    ctx: Context, negate: str, header_count: int
) -> None:
    """Checks if the request header count is a given value

    Args:
        ctx: the behave context
        negate: A string representing whether a response should be negated
        header_count: The value to check against the header count

    """
    number_of_headers = len(ctx.headers)
    if negate:
        logger.debug(f"Asserting request header count is {negate} {header_count}")
        ValueNotEqualsAssertion(int(header_count), number_of_headers)
    else:
        logger.debug(f"Asserting request header count is {header_count}")
        ValueEqualsAssertion(int(header_count), number_of_headers)


# ------------------------------------------------------------------------
# Generic steps for header JSON response validation
# ------------------------------------------------------------------------


@then("the response content header should (?P<negate>not )?be (?:JSON|json)")
def step_assert_content_header(ctx: Context, negate: str) -> None:
    """Checks if the response is json using its content header.

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    header = ctx.response.headers.get("content-type")
    logger.debug(f"Checking that the response content is {negate}a JSON")
    ValueNotEqualsAssertion(
        "application/json; charset=utf-8", header
    ) if negate else ValueEqualsAssertion("application/json; charset=utf-8", header)
    logger.debug(f"Validated that the response content was {negate}a JSON")


@then("the response headers should (?P<negate>not )?be the following(?::|)?")
def step_assert_headers(ctx: Context, negate: str) -> None:
    """Checks that the headers have the proper values.

    Table Example:
        | header_name | header_value |

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        header = ctx.response.headers.get(row[0])
        header_value = interpolate_context_attributes(ctx, row[1])
        logger.debug(
            f"Checking that the response header: {row[0]} should {negate}be: {header_value}"
        )
        ValueNotEqualsAssertion(
            header, header_value
        ) if negate else ValueEqualsAssertion(header, header_value)
        logger.debug("Successfully validated response headers")
