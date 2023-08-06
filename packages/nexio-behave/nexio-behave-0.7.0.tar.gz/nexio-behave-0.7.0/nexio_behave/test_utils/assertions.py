"""Test module for assertions"""
from typing import Any, List

from ansicolor import ansicolor


class StatusCodeAssertion:
    """Asserts that two given status codes are equal to each other"""

    def __init__(
        self, expected_value: int, returned_value: int, additional_message: str = ""
    ) -> None:
        """Initializing StatusCodeAssertion

        Args:
            expected_value: The expected value we are comparing against
            returned_value: The value we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert expected_value == returned_value, _error_message_formatter(
            "Status code expected",
            str(expected_value),
            "Status code returned",
            str(returned_value),
            additional_message,
        )


class ValueTrueAssertion:
    """Assert that the value will evaluate to True"""

    def __init__(self, returned_value: Any, additional_message: str = "") -> None:
        """Initializing ValueTrueAssertion

        Args:
            returned_value: The value we are expecting to be true
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert returned_value, _error_message_formatter(
            "Response expected",
            "True or Truthy",
            "Response returned",
            returned_value,
            additional_message,
        )


class ValueFalseAssertion:
    """Assert that the value will evaluate to False"""

    def __init__(self, returned_value: Any, additional_message: str = "") -> None:
        """Initializing ValueFalseAssertion

        Args:
            returned_value: The value we are expecting to be true
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert not returned_value, _error_message_formatter(
            "Response expected",
            "False or Falsy",
            "Response returned",
            returned_value,
            additional_message,
        )


class ValueEqualsAssertion:
    """Assert that two given values/types are equal to each other"""

    def __init__(
        self, expected_value: Any, returned_value: Any, additional_message: str = ""
    ) -> None:
        """Initializing ValueEqualsAssertion

        Args:
            expected_value: The expected value we are comparing against
            returned_value: The value we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        # Typecheck to ensure that the two inputs of are the same type
        assert isinstance(returned_value, type(expected_value)), TypeError
        assert expected_value == returned_value, _error_message_formatter(
            "Response expected",
            expected_value,
            "Response returned",
            returned_value,
            additional_message,
        )


class ValueNotEqualsAssertion:
    """Assert that two given values/types are NOT equal to each other"""

    def __init__(
        self, expected_value: Any, returned_value: Any, additional_message: str = ""
    ) -> None:
        """Initializing ValueNotEqualsAssertion

        Args:
            expected_value: The expected value we are comparing against
            returned_value: The value we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert expected_value != returned_value, _error_message_formatter(
            "Response expected to NOT be",
            expected_value,
            "Response returned",
            returned_value,
            additional_message,
        )


class ValueIsInAssertion:
    """Assert that the expected value is contained in the returning value.

    The returning value could be a string in which case the expected value would be a substring
        of the returning value or the returning could be an iterable where the expected value would be
        an element of the returning value. Since only a shallow check is performed, nested objects should
        be traversed before asserting.

    """

    def __init__(
        self, expected_value: Any, returned_value: Any, additional_message: str = ""
    ) -> None:
        """Initializing ValueIsInAssertion

        Args:
            expected_value: The expected value we are comparing against
            returned_value: The value we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert expected_value in returned_value, _error_message_formatter(
            "Response expected to contain",
            expected_value,
            "Response returned",
            returned_value,
            additional_message,
        )


class ValueIsNotInAssertion:
    """Assert that the expected value is NOT contained in the returning value.

    The returning value could be a string in which case the expected value would NOT be a substring
        of the returning value or the returning could be an iterable where the expected value would NOT be
        an element of the returning value. Since only a shallow check is performed, nested objects should
        be traversed before asserting.

    """

    def __init__(
        self, expected_value: Any, returned_value: Any, additional_message: str = ""
    ) -> None:
        """Initializing ValueIsNotInAssertion

        Args:
            expected_value: The expected value we are comparing against
            returned_value: The value we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert expected_value not in returned_value, _error_message_formatter(
            "Response expected NOT to contain",
            expected_value,
            "Response returned",
            returned_value,
            additional_message,
        )


class OneOfValuesInAssertion:
    """Assert that the expected value is contained in the returning value or in an element within the returning value.

    Performs the same assertion as ValueIsInAssertion except that this expects and checks multiple returning values

    """

    def __init__(
        self,
        expected_values_list: List[Any],
        returned_value: Any,
        additional_message: str = "",
    ) -> None:
        """Initializing OneOfValuesInAssertion

        Args:
            expected_values_list: The list of possible expected values we are comparing against
            returned_value: The value we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert any(
            expected_value in returned_value for expected_value in expected_values_list
        ), _error_message_formatter(
            "Response expected to contain one of the following",
            ", ".join(expected_values_list),
            "Response returned",
            returned_value,
            additional_message,
        )


class NoneOfValuesInAssertion:
    """Assert that the None of the expected values is contained in the returning value or in an element within the returning value.

    Performs the same assertion as ValueIsNotInAssertion except that this expects and checks multiple returning values

    """

    def __init__(
        self,
        expected_values_list: List[Any],
        returned_value: Any,
        additional_message: str = "",
    ) -> None:
        """Initializing NoneOfValuesInAssertion

        Args:
            expected_values_list: The list of possible expected values we are comparing against
            returned_value: The value we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert not any(
            expected_value in returned_value for expected_value in expected_values_list
        ), _error_message_formatter(
            "Response expected to contain none of the following",
            ", ".join(expected_values_list),
            "Response returned",
            returned_value,
            additional_message,
        )


class ValueIsEmptyAssertion:
    """Asserts that the passed parameter is equal to None or empty string, list, dict, set, or tuple"""

    def __init__(self, returned_value: str, additional_message: str = "") -> None:
        """Initializing ValueIsEmptyAssertion

        Args:
            returned_value: The value to be asserted against
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert (
            returned_value in (None, "[]") or len(returned_value) == 0
        ), _error_message_formatter(
            "Response expected",
            "None, '', {}, (), or []",
            "Response returned",
            returned_value,
            additional_message,
        )


class ValueIsNotEmptyAssertion:
    """Asserts that the passed parameter is NOT equal to None or empty string, list, dict, set, or tuple"""

    def __init__(self, returned_value: str, additional_message: str = "") -> None:
        """Initializing ValueIsNotEmptyAssertion

        Args:
            returned_value: The value to be asserted against
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        assert len(str(returned_value)) > 0, _error_message_formatter(
            "Response expected",
            "Some type of payload",
            "Response returned",
            "None",
            additional_message,
        )


class ListEqualsAssertion:
    """Assert that two given lists are equal to each other"""

    def __init__(
        self,
        expected_values_list: List[Any],
        returned_values_list: List[Any],
        additional_message: str = "",
    ) -> None:
        """Initializing ListEqualsAssertion

        Args:
            expected_values_list: The expected list we are comparing against
            returned_values_list: The actual list we are comparing against the control
            additional_message: (Optional) Any additional information to display with the
                error message

        """
        # Typecheck to ensure that the two inputs of are the same type
        assert isinstance(returned_values_list, type(expected_values_list)), TypeError
        expected_values_list.sort()
        returned_values_list.sort()
        assert expected_values_list == returned_values_list, _error_message_formatter(
            "Response expected",
            expected_values_list,
            "Response returned",
            returned_values_list,
            additional_message,
        )


def _error_message_formatter(
    expected_message: str,
    expected_value: Any,
    returned_message: str,
    returned_value: Any,
    additional_message: str,
) -> str:
    """Formats the False assertion error message so that it is more easily readable.

    Also makes it so that the message and only the message is red.

    Example:
        Response expected to contain one of the following:
            http://localhost:3000/signin?, http://localhost:3000/login?.
         Response returned:
            http://localhost:3000/stories/feed.

    Args:
        expected_message: The default expected message. i.e. Response expected
        expected_value: The expected value to compare against.
        returned_message: The default returned message. i.e. Response returned
        returned_value: The value we are comparing against the control
        additional_message: Any additional information to display with the
            error message

    Returns:
        Str: A string in a standard format

    """
    # using a custom tab size allows for more standard indents than \t
    TAB = "   "
    return ansicolor.red(
        "\n"
        f"{TAB}{expected_message}:\n"
        f"{TAB*2}{expected_value}.\n"
        f"{TAB}{returned_message}:\n"
        f"{TAB*2}{returned_value}.\n"
        f"{TAB}{additional_message}"
    )
