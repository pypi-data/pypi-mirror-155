"""Common REST behave steps"""
from behave import use_step_matcher, when
from behave.runner import Context
from loguru import logger
from requests import Session

from nexio_behave.utils.common_behave_functions import interpolate_context_attributes
from nexio_behave.utils.generic_requests import GenericRequests

# Enable the regex step matcher
use_step_matcher("re")


@when(
    "(?:a|an)? (?P<method>POST|GET|PUT|PATCH|DELETE|OPTIONS) request is sent to (?i)(?P<endpoint>.*)"
)
def step_send_generic_rest_request(ctx: Context, method: str, endpoint: str) -> None:
    """Send a rest request to an endpoint.

    This is a generic behave step that will allow for multiple types of requests to be sent.

    Supports:
    - POST
    - GET
    - PUT
    - PATCH
    - DELETE
    - OPTIONS

    Args:
        ctx: The behave context
        method: The REST method. ie: POST, GET, etc.
        endpoint: The URL to send the request to. NOTE: BASE URL is already defined in framework setup

    Returns:
        response saved on the behave context

    """
    # First form a URL using any variables that were stored in the context and denoted in the endpoint
    # Don't forget to tag on the base URL if it exists
    if hasattr(ctx, "base_url"):
        url = f"{ctx.base_url}/{interpolate_context_attributes(ctx=ctx, value=endpoint.lower())}"
    else:
        url = interpolate_context_attributes(ctx=ctx, value=endpoint.lower())

    # Define our headers. If we have none on the context set to None
    if hasattr(ctx, "headers"):
        headers = getattr(ctx, "headers")
    else:
        headers = None

    # Define our payload that we will send - ctx.text comes from the behave feature file if present.
    if ctx.text is not None or "":
        payload = getattr(ctx, "text")
    elif hasattr(ctx, "request_data"):
        payload = getattr(ctx, "request_data")
    else:
        payload = None

    # Define our file payload to send if we have one
    if hasattr(ctx, "file"):
        file = getattr(ctx, "file")
        logger.debug(f"We found a file to use as our payload. File path: {file}")
    else:
        file = None

    # Check to see which session client to use. If there is no client saved to context
    # create a new client session to use.
    if hasattr(ctx, "client"):
        client = getattr(ctx, "client")
    else:
        logger.debug(
            "There was no client saved to the context. Generating a new client for this request..."
        )
        client = Session()

    # Send the request
    ctx.response = GenericRequests.generic_request(
        client, method.lower(), url, headers=headers, json=payload, file_path=file
    )
    # Reset the request data but save on context in case we need it still
    ctx.previous_payload = payload
    ctx.request_data = None
