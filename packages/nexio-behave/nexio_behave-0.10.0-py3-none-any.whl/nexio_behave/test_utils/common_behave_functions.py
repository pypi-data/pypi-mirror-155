"""All common behave functions that are used in behave frameworks"""
import re
from typing import Union

from behave.runner import Context
from loguru import logger


def interpolate_context_attributes(ctx: Context, value: str) -> str:
    """Function that will check the context to see if we have an attribute stored with that name.

    This function will parse out variable names with the following regex: {.*} taking all chars between braces
    If the string value read in is None at the start -> return None

    Args:
        ctx: behave context that holds our attribute and value for parsing
        value: the string to traverse for attributes on the context

    Returns:
        the new string with all context vars replaced with values

    """
    if value is None:
        logger.debug("No value passed in to interpolate... failsafe is to return none!")
        return None
    else:
        # Replace all properties with the context value of the property
        parameters = re.findall(r"\{([.,\w-]+)\}", value)
        namespace = {param: getattr(ctx, param) for param in parameters}
        return value.format(**namespace)


def modify_json_value(
    current_payload: dict, path_to_value: str, new_value: str
) -> dict:
    """Function that will recursively traverse a dictionary and replace a value at a given key.

    The "key" is evaluated using JSON path such as "first_key.nested_key" when we have nested dictionaries.

    Args:
        current_payload: the dictionary we want to recursively search for a key value pair to replace
        path_to_value: the JSON path expression of the key to search for
        new_value: The new value we will replace at the key once found

    """
    if "." not in path_to_value and "[" not in path_to_value:
        current_payload[path_to_value] = new_value
        return current_payload
    else:
        __set_dict_attribute(current_payload, path_to_value, new_value)
        return current_payload


def __set_dict_attribute(dictionary: dict, key_string: str, value: str) -> None:
    """Sets a deep value in a given dict to a new value given a string representation of the key

        Example key_string: expression_group.plural_expression.display_string

    Args:
        dictionary: The outermost dictionary (usually ctx.request_data)
        key_string: A string representation of the key being inserted
        value: The value the key should have

    """
    inner_dict = dictionary
    key_list = key_string.split(".")
    latest = key_list.pop()
    for key in key_list:
        if re.match(r".*\[\d+\].*", key):
            inner_dict = __set_list_attribute(inner_dict, key)  # type: ignore
            continue
        else:
            inner_dict = inner_dict.setdefault(key, {})
    if re.match(r".*\[\d+\].*", latest):
        __set_list_attribute(inner_dict, latest, value)
    else:
        inner_dict.setdefault(latest, {})
        inner_dict[latest] = value


def __set_list_attribute(
    dictionary: dict, key_string: str, value: str = None
) -> Union[dict, str]:
    """Sets a value in a given dict to a new value.

    The new value will contain at least a key that wraps a list
        which may warp another key or a string

    Examples:
         key_string: expression_group.plural_expression[0]display_string
         key_string: expression_group.plural_expression[0] (will always take a value in this case)

    Args:
        dictionary: The dictionary that will wrap the outer dict
        key_string: A string representation of the key being upserted
            Format should be <outer_key>[<integer>]<(optional)inner_key>
        value: (Optional) The value the inner key should have

    Returns:
        dictionary: The most inner dictionary value. Could be a dict or a string depending on whether
            the value parameter is provided

    """
    search = re.search(r"(.*)\[(\d)\](.*)", key_string)
    outer_key, index, inner_key = search.group(1), int(search.group(2)), search.group(3)
    # ensures a key error is not thrown and that nothing is overwritten
    if not dictionary.get(outer_key) or not isinstance(dictionary[outer_key], list):
        dictionary[outer_key] = [{}]
    # enables users to set any list index to a given value
    if len(dictionary[outer_key]) <= index:
        dictionary[outer_key] = dictionary[outer_key] + [{}] * (
            index + 1 - len(dictionary[outer_key])
        )
    if inner_key and value:
        dictionary[outer_key][index] = {inner_key: value}
        dictionary = dictionary[outer_key][index][inner_key]
    elif inner_key:
        # want set default here so other values are not overwritten
        dictionary[outer_key][index].setdefault(inner_key, {})
        dictionary = dictionary[outer_key][index][inner_key]
    elif value:
        dictionary[outer_key][index] = value
        dictionary = dictionary[outer_key][index]
    return dictionary
