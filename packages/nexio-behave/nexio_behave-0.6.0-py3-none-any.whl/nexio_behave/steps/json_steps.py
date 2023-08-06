"""Generic JSON step definitions for REST APIs"""
import copy
from distutils.util import strtobool
import json
import os
from typing import Dict, Optional, Union
import uuid

from behave import given, use_step_matcher
from behave.runner import Context
from loguru import logger

from nexio_behave.utils.common_behave_functions import (
    interpolate_context_attributes,
    modify_json_value,
)

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


# ------------------------------------------------------------------------
# Generic steps for creating JSON payloads (dictionaries)
# ------------------------------------------------------------------------


@given('JSON from the following(?: saved as "(?P<value_name>.*)")?(?::|)?')
def step_generic_json_dictionary(ctx: Context, value_name: str = None) -> None:
    """Sets the given table representing a request payload to an attribute in the behave context as a given name.

    Table Example:
        | key | value |

    Args:
        ctx: The behave context
        value_name: The name of the attribute in the behave context

    """
    logger.debug(f"Attempting to save payload as: {value_name}.")
    payload: Dict[str, Union[str, int]] = {}
    for row in ctx.table:
        value = interpolate_context_attributes(ctx, row[1])
        if value.isdigit():
            # If value is a digit cast to int
            payload[row[0]] = int(value)
        elif get_bool(value) is not None:
            payload[row[0]] = get_bool(value)
        else:
            payload[row[0]] = value
    # If value_name is specified, set a context attribute with that name equal to the payload.
    # Else set ctx.request_data equal to the payload.
    if value_name:
        setattr(ctx, value_name, payload)
    else:
        ctx.request_data = payload
    logger.debug(f"Successfully saved payload: {payload} as: {value_name}.")


@given("request data from the previous request")
def step_set_previous_request_data(ctx: Context) -> None:
    """Sets the data from the previous request payload to the request data for the current request.

    Args:
        ctx: The behave context

    """
    logger.debug(
        "Attempting to set the request data to the last used request_data value"
    )
    ctx.request_data = ctx.previous_payload
    logger.debug(f"Successfully set the request data to: {ctx.request_data}")


@given('request data from context variable "(?P<context_variable>.*)"')
def step_set_request_data_from_ctx_var(ctx: Context, context_variable: str) -> None:
    """Reads a variable name without the {} and change to the value in context.

    It is then saved to the context as request_data.

    Args:
        ctx: The behave context
        context_variable: The context variable to search for via get_attr()

    """
    logger.debug(
        f"Attempting to set the request_data on context from a context variable: {context_variable}"
    )
    # save the value of the context attribute rather than just the reference
    # allows manipulation of the request data without alteration of the original data
    ctx.request_data = copy.deepcopy(getattr(ctx, context_variable))
    logger.debug(f"ctx.request _data is set to: {ctx.request_data}\n\n")


# ------------------------------------------------------------------------
# Generic steps for modifying JSON (dictionaries)
# ------------------------------------------------------------------------


@given(
    'the (?:JSON|json)? request payload at "(?P<target_key>.*)" is modified to be "(?P<value>.*)"'
)
def step_generic_modify_request_json(ctx: Context, target_key: str, value: str) -> None:
    """Modifies the request data in the behave context to have the actual value of the given string representation.

    Args:
        ctx: The behave context
        target_key: The key whose value is to be modified
        value: A string representation of what the new value should be

    """
    logger.debug(
        f"Attempting to modify the JSON request payload at: {target_key} to be: {value}."
    )
    desired_value = interpolate_context_attributes(ctx, value)
    parsed_key = interpolate_context_attributes(ctx, target_key)
    if desired_value.lower() in ("none", "null"):
        ctx.request_data = modify_json_value(ctx.request_data, parsed_key, None)
    elif desired_value.lower() in ("invalid", "empty", "empty string"):
        ctx.request_data = modify_json_value(ctx.request_data, parsed_key, "")
    elif desired_value.lower() in "uuid":
        ctx.request_data = modify_json_value(
            ctx.request_data, parsed_key, str(uuid.uuid4())
        )
    else:
        ctx.request_data = modify_json_value(
            ctx.request_data, parsed_key, desired_value
        )
    logger.debug("Successfully updated JSON request payload.")


@given('request data with json dataset "(?P<filename>.*)"')
def step_gen_data_object(ctx: Context, filename: str) -> None:
    """Generates a data object for a story

    Args:
        ctx: The behave context
        filename: The file name that will be uploaded

    """
    logger.debug(f"Attempting to generate request data from file: {filename}")
    filepath = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/datasets/{filename}.json"
    with open(filepath) as f:
        ctx.request_data = json.load(f)
    logger.debug(f"Successfully generated request data from file: {filename}")


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
