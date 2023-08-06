"""Generic HEADER step definitions for REST APIs"""
from behave import given, use_step_matcher
from behave.runner import Context
from loguru import logger

from nexio_behave.utils.common_behave_functions import interpolate_context_attributes

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


@given("I send and receive JSON")
def step_set_json_headers(ctx: Context) -> None:
    """Sets the Accept anf content-type headers to application/json

    Args:
        ctx: The behave context

    """
    logger.debug("Setting headers to send and receive application/json")
    ctx.headers["Accept"] = "application/json"
    ctx.headers["content-type"] = "application/json"
    logger.debug("Headers are set to send and receive application/json")


@given('request header "(?P<header>.*)" is set to "(?P<header_value>.*)"')
def step_set_request_header(ctx: Context, header: str, header_value: str) -> None:
    """Sets a given type of request header to a given value.

    Args:
        ctx: The behave context
        header: The type of request header
        header_value: The value the request header should have

    """
    desired_value = interpolate_context_attributes(ctx, header_value)
    logger.debug(f"Attempting to set request header: {header} to: {header_value}")
    if desired_value.lower() in ("invalid", "empty", "empty string"):
        ctx.headers[header] = ""
    elif desired_value.lower() in ("none", "null"):
        ctx.headers[header] = None
    else:
        ctx.headers[header] = desired_value
    logger.debug(f"Successfully set request header: {header} to: {ctx.headers[header]}")


@given("request headers(?::|)?")
def step_set_request_headers(ctx: Context) -> None:
    """Sets a table of given request headers to given values.

    Table Example:
        | header | header_value |

    Args:
        ctx: The behave context

    """
    for row in ctx.table:
        step_set_request_header(ctx, row[0], row[1])


@given("all request headers are reset")
def clear_request_headers(ctx: Context) -> None:
    """Clears all request headers stored on the context"""
    ctx.headers = {}
