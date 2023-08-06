"""Behave framework environment configuration. This file holds all hooks and environment setup."""
from behave.model import Feature, Scenario, Step, Tag
from behave.runner import Context
from loguru import logger

from nexio_behave.utils.environment_functions import (
    initialize_context_variables,
    reset_context_vars,
    set_user_data,
    setup_logging,
)


def before_all(ctx: Context) -> None:
    """Hook that runs before all features

    Args:
        ctx: The behave context

    """
    log_before_all()
    setup_logging(ctx)
    set_user_data(ctx)
    initialize_context_variables(ctx)
    log_before_all_complete()


def before_tag(ctx: Context, tag: Tag) -> None:
    """Hook that runs before a specific tag

    Args:
        ctx: The behave context
        tag: Behave tag

    """
    pass


def before_feature(ctx: Context, feature: Feature) -> None:
    """Hook that runs before every feature

    Args:
        ctx: The behave context
        feature: The behave feature

    """
    pass


def before_scenario(ctx: Context, scenario: Scenario) -> None:
    """Hook that runs before every scenario

    Args:
        ctx: The behave context
        scenario: The behave scenario

    """
    pass


def before_step(ctx: Context, step: Step) -> None:
    """Hook that runs before every step

    Args:
        ctx: The behave context
        step: The behave step

    """
    pass


def after_all(ctx: Context) -> None:
    """Hook that runs after all features

    Args:
        ctx: The behave context

    """
    log_after_all()
    log_after_all_complete()


def after_tag(ctx: Context, tag: Tag) -> None:
    """Hook that runs after a specific tag

    Args:
        ctx: The behave context
        tag: the behave tag

    """
    pass


def after_feature(ctx: Context, feature: Feature) -> None:
    """Hook that runs after every feature

    Args:
        ctx: The behave context
        feature: The behave feature

    """
    reset_context_vars(ctx)


def after_scenario(ctx: Context, scenario: Scenario) -> None:
    """Hook that runs after every scenario

    Args:
        ctx: The behave context
        scenario: The behave scenario

    """
    pass


def after_step(ctx: Context, step: Step) -> None:
    """Hook that runs after every step

    Args:
        ctx: The behave context
        step: The behave step

    """
    pass


# -------------------------------------------------------------------------------------
# Logging functions
# -------------------------------------------------------------------------------------


def log_before_all() -> None:
    """Log the before all setup for the integration test framework"""
    logger.info(
        "Welcome to the Narrative Science Integration Test Framework. Hang tight while we set a few things up."
    )


def log_before_all_complete() -> None:
    """Log the before all complete"""
    logger.info("Framework and environment setup is complete! Starting tests...")


def log_after_all() -> None:
    """Log the after all tear down"""
    logger.info(
        "Integration tests have finished execution. "
        "Hang tight while we clean up a few things and publish test results."
    )


def log_after_all_complete() -> None:
    """Log the after all teardown complete"""
    logger.info(
        "Clean up is complete. Test results published. "
        "Shutting down the Narrative Science Integration Test Framework. Goodbye!"
    )
