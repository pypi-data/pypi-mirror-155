"""Step definitions for REST API responses"""
from behave import then, use_step_matcher
from behave.runner import Context
from jsonpath import jsonpath
from loguru import logger

from nexio_behave.utils.assertions import (
    StatusCodeAssertion,
    ValueEqualsAssertion,
    ValueIsEmptyAssertion,
    ValueIsNotEmptyAssertion,
    ValueNotEqualsAssertion,
)
from nexio_behave.utils.common_behave_functions import interpolate_context_attributes

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


# ------------------------------------------------------------------------
# Generic steps for status codes
# ------------------------------------------------------------------------


@then("a (?P<status>[0-9]{3}) response is returned")
def step_assert_status_code(ctx: Context, status: int) -> None:
    """Checks if the response has the correct status code being returned

    Args:
        ctx: The behave context
        status: The expected status code

    """
    StatusCodeAssertion(int(status), ctx.response.status_code)


# ------------------------------------------------------------------------
# Generic steps for REST responses
# ------------------------------------------------------------------------


@then("the (?:JSON|json)? response should have (?P<negate>no )?content")
def step_assert_rest_response_content(ctx: Context, negate: str) -> None:
    """Checks if the JSON response has content.

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'no'. Otherwise, it will be None

    """
    logger.debug(f"Checking that the JSON response has {negate}content")
    ValueIsEmptyAssertion(ctx.response.text) if negate else ValueIsNotEmptyAssertion(
        ctx.response.text
    )
    logger.debug(f"Successfully validated that the response has {negate}content")


@then('the (?:JSON|json)? response should (?P<negate>not )?include "(?P<key>.*)"')
def step_assert_rest_response_key(ctx: Context, negate: str, key: str) -> None:
    """Checks that the JSON response contains a given key.

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None
        key: The key that should be present in the response

    """
    list_of_values = jsonpath(
        ctx.response.json(),
        interpolate_context_attributes(ctx, f"$.{key}"),
    )
    logger.debug(
        f"Checking that the JSON response should {'not ' if negate else ''}include key: {key}"
    )
    if list_of_values:
        if negate:
            ValueIsEmptyAssertion(
                list_of_values,
                f"Expected no key to be found at '{key}', but it was present. Response: {ctx.response.text}",
            )
        else:
            ValueIsNotEmptyAssertion(
                list_of_values,
                f"Expected key to be found at '{key}', but it was not present. Response: {ctx.response.text}",
            )
    else:
        raise KeyError(
            f"No key: '{key}' found in the JSON response: {ctx.response.json()}"
        )
    logger.debug(f"Validated that the JSON response did {negate}include key: {key}")


@then(
    "the (?:JSON|json)? response should (?P<negate>not )?include the following(?::|)?"
)
def step_assert_rest_response_key_table(ctx: Context, negate: str) -> None:
    """Checks that the JSON response contains all keys from a given table.

    Table Example:
        | attribute | key_value |

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        step_assert_rest_response_key(ctx, negate, row[0])


@then(
    'the (?:JSON|json)? response at "(?P<key>.*)" should (?P<negate>not )?have data type (?P<data_type>.*)'
)
def step_assert_rest_response_data_type(
    ctx: Context, key: str, negate: str, data_type: str
) -> None:
    """Checks that the key in the response is of the given data type.

    Args:
        ctx: The behave context
        key: The key in the response
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None
        data_type: The data type of the key

    """
    list_of_values = jsonpath(
        ctx.response.json(),
        interpolate_context_attributes(ctx, f"$.{key}"),
    )
    if list_of_values:
        found_value = list_of_values[0]
        class_name = found_value.__class__.__name__
        logger.debug(
            f"Checking that the JSON response at key: {key} should"
            f" {'not' if negate else ''}have data type: {data_type} ({found_value} {class_name})"
        )
        ValueNotEqualsAssertion(
            data_type, class_name
        ) if negate else ValueEqualsAssertion(data_type, class_name)
    else:
        raise KeyError(
            f"No key: '{key}' found in the JSON response: {ctx.response.json()}"
        )


@then(
    "the (?:JSON|json)? response should (?P<negate>not )?have the following data types(?::|)?"
)
def step_assert_rest_response_data_type_table(ctx: Context, negate: str) -> None:
    """Checks that the JSON response has keys of the given data types.

    Table Example:
        | attribute | data_type |

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        step_assert_rest_response_data_type(ctx, row[0], negate, row[1])


@then(
    'the (?:JSON|json)? response at "(?P<key>.*)" should (?P<negate>not )?be "(?P<value>.*)"'
)
def step_assert_rest_response_value(
    ctx: Context, key: str, negate: str, value: str
) -> None:
    """Generic step definition that will read in a key using json path and traverse the json to find the value.

    Assertions are done based on the negate flag.
    Json path is a language that allows you to find values in json based on an expression.
    Find more info on json path here: https://restfulapi.net/json-jsonpath/.

    Args:
        ctx: The behave context
        negate: type of assert. Either should be or should not be. represented by optional gherkin syntax = 'no'
        key: json path key expression
        value: the expected value in the assert

    """
    list_of_values = jsonpath(
        ctx.response.json(),
        interpolate_context_attributes(ctx, f"$.{key}"),
    )
    desired_value = interpolate_context_attributes(ctx, value)
    if list_of_values:
        found_value = str(list_of_values[0])
        logger.debug(
            f"Checking that the JSON response at key: {key} should {negate}be: {value}"
        )
        ValueNotEqualsAssertion(
            desired_value, found_value
        ) if negate else ValueEqualsAssertion(desired_value, found_value)
    else:
        raise KeyError(
            f"No key: '{key}' found in the JSON response: {ctx.response.json()}"
        )


@then("the (?:JSON|json)? response should (?P<negate>not )?be the following(?::|)?")
def step_assert_rest_response_value_table_a(ctx: Context, negate: str) -> None:
    """Checks that the JSON response have the given values.

    Table Example:
        | attribute | value |

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        step_assert_rest_response_value(ctx, row[0], negate, row[1])


@then(
    'the (?:JSON|json)? response(?: at "(?P<key>.*)")? should (?P<negate>not )?have (?P<collection_size>[0-9]+)'
)
def step_assert_rest_response_collection_size(
    ctx: Context, key: str, negate: str, collection_size: str
) -> None:
    """Checks that the JSON response does or does not have a collection of the given size.

    Args:
        ctx: The behave context
        negate: A string representing whether a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None
        key: The key in the JSON response where the collection size should be checked
        collection_size: The expected size of the collection

    """

    if key:
        list_of_values = jsonpath(
            ctx.response.json(),
            interpolate_context_attributes(ctx, f"$.{key}"),
        )
        if list_of_values:
            found_value = list_of_values[0]
            if isinstance(found_value, (dict, list)):
                logger.debug(
                    f"Checking that the JSON response at key: {key} should {negate}have size: {collection_size}"
                )
                ValueNotEqualsAssertion(
                    int(collection_size), len(found_value)
                ) if negate else ValueEqualsAssertion(
                    int(collection_size), len(found_value)
                )
                logger.debug(
                    f"Validated that the JSON response at key: {key} should {negate}have size: {collection_size}"
                )
            else:
                raise TypeError(
                    f"No dict or list found at key: '{key}'. We found: {type(found_value).__name__}"
                )
        else:
            raise KeyError(
                f"No key: '{key}' found in the JSON response: {ctx.response.json()}"
            )
    else:
        logger.debug(
            f"Checking that the JSON response should have size: {collection_size}"
        )
        ValueEqualsAssertion(int(collection_size), len(ctx.response.json()))
        logger.debug(
            f"Validated that the JSON response did have size: {collection_size}"
        )
