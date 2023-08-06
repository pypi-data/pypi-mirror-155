"""Generic CONTEXT step definitions for REST APIs"""
from behave import given, step, use_step_matcher
from behave.runner import Context
from jsonpath import jsonpath
from loguru import logger

from nexio_behave.utils.common_behave_functions import interpolate_context_attributes

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


# ------------------------------------------------------------------------
# Generic steps for context memory and variables
# ------------------------------------------------------------------------


@given('the value "(?P<value>.*)" is saved as "(?P<value_name>.*)"')
def step_save_variable_to_context(ctx: Context, value: str, value_name: str) -> None:
    """Sets a variable to an attribute of the behave context

    Args:
        ctx: The behave context
        value: The name the new attribute in the behave context should have
        value_name: The value of the new attribute in the behave context

    """
    setattr(ctx, value_name, value)
    logger.debug(f"Successfully saved value: {value} as {value_name}")


@step('the context value at "(?P<context_attribute>.*)" is logged')
def step_print_context_attribute_value(ctx: Context, context_attribute: str) -> None:
    """Prints the value of an attribute from the behave context to the debug logger

    Args:
        ctx: The behave context
        context_attribute: The attribute in the behave context that should be printed

    """
    found_value = getattr(ctx, context_attribute)
    if found_value:
        logger.debug(
            f"Context attribute: key: '{context_attribute}' value: '{found_value}'"
        )
    else:
        raise AttributeError(
            f"No attribute '{context_attribute}'' found saved on the context"
        )


# ------------------------------------------------------------------------
# Generic steps for context response and request
# ------------------------------------------------------------------------


@step('the (?:JSON|json)? response at "(?P<key>.*)" is saved as "(?P<value_name>.*)"')
def step_save_response_attribute_to_context(
    ctx: Context, key: str, value_name: str
) -> None:
    """Sets the JSON response with a given key to a value in the behave context with an attribute name of <value_name>

    Args:
        ctx: The behave context
        key: The key from the JSON response
        value_name: The new name for the new attribute in the behave context

    """
    interpolated_key = interpolate_context_attributes(ctx, f"$.{key}")
    list_of_values = jsonpath(ctx.response.json(), interpolated_key)
    logger.debug(
        f"Attempting to save JSON response at: {interpolated_key} as: {value_name}."
    )
    if list_of_values:
        found_value = list_of_values[0]
        setattr(ctx, value_name, found_value)
        logger.debug(f"Successfully saved response attribute: {key} as {value_name}.")
    else:
        raise KeyError(
            f"No key: '{interpolated_key}' found in the JSON response: {ctx.response.json()}"
        )


@step("the (?i)(?:JSON|json)? response is saved as the following(?::|)?")
def step_save_response_attributes_to_context(ctx: Context) -> None:
    """The key values in the first column are saved to context with the name under the second column.

    Table Example:
        | attribute | value |

    Args:
        ctx: The behave context

    """
    for row in ctx.table:
        step_save_response_attribute_to_context(ctx, row[0], row[1])


@given('the (?:JSON|json)? payload at "(?P<key>.*)" is saved as "(?P<value_name>.*)"')
def step_save_request_attribute_to_context(
    ctx: Context, key: str, value_name: str
) -> None:
    """Set a value from the request payload to the behave context

    Args:
        ctx: The behave context
        key: The key from the request payload to save
        value_name: The name the new attribute should have in the behave context

    """
    logger.debug(f"Attempting to save JSON payload at: {key} as: {value_name}.")
    list_of_values = jsonpath(ctx.request_data, f"$.{key}")
    if list_of_values:
        found_value = list_of_values[0]
        setattr(ctx, value_name, found_value)
        logger.debug(
            f"Successfully saved the JSON payload at: {value_name} as: {found_value}."
        )
    else:
        raise KeyError(
            f"No key: '{key}' found in the request_data saved on the context: {ctx.request_data}"
        )


@step(
    'the position where "(?P<key>.*)" is "(?P<value>.*)" is saved from the JSON response(?: at "(?P<json_key>.*)")?'
)
def step_save_position_attribute_to_context(
    ctx: Context, key: str, value: str, json_key: str = None
) -> None:
    """Attempts to obtain a key from the JSON response and set the value of that key to the behave context

    Args:
        ctx: The behave context
        key: The positional key that is being searched for
        value: The value the positional key should have
        json_key: The json key that indicates where the search for the positional key should occur

    """
    interpolated_key = interpolate_context_attributes(ctx, key)
    interpolated_value = interpolate_context_attributes(ctx, value)
    # Check if we are at the root of the json. If we are then use the '.' instead of the json key
    if json_key:
        list_of_values = jsonpath(ctx.response.json(), f"$.{json_key}")
    else:
        list_of_values = jsonpath(ctx.response.json(), ".")
    logger.debug(
        f"Attempting to find position where key: {key} is value: {value} at: {list_of_values}."
    )
    if list_of_values:
        json_objects = list_of_values[0]
        for json_object in json_objects:
            if json_object[interpolated_key] == interpolated_value:
                setattr(ctx, "position", str(json_objects.index(json_object)))
                logger.debug(
                    f"Successfully saved position as: {ctx.position} for key: {key} and value {value} at {list_of_values}."
                )
                break
        else:
            raise KeyError(
                f"No key: '{interpolated_key}' found in the dictionary: {json_object}"
            )
    else:
        raise KeyError(
            f"No collection found at '{json_key}' in the JSON response: {ctx.response.json()}"
        )
