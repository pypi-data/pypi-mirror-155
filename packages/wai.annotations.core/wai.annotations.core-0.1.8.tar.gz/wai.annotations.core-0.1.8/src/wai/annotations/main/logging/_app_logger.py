"""
Provides the application logger for wai.annotations.
"""
import logging
import os

from wai.common.logging import create_standard_handler, DEBUG_HANDLER_NAME, INFO_HANDLER_NAME, \
    WARNING_HANDLER_NAME, ERROR_HANDLER_NAME


def create_application_root_logger() -> logging.Logger:
    """
    Sets up a root logger and returns it. If the root
    logger has already been configured, issues a warning but leaves
    the logger unchanged.

    :return:        The root logger.
    """
    # Get the root logger
    logger = logging.getLogger()

    # If the logger already has been configured, warn and abort
    if len(logger.handlers) > 0:
        logger.warning("Attempted to reconfigure root logger")
        return logger

    # Create a debug handler to print debug info to std-out
    debug_handler = create_standard_handler(
        True,
        DEBUG_HANDLER_NAME,
        logging.DEBUG,
        "{levelname:8} {created:023} - {name} - {lineno} - {funcName} - {pathname}\n"
        "{message}"
    )

    # Create an info handler to print info messages to std-out
    info_handler = create_standard_handler(
        True,
        INFO_HANDLER_NAME,
        logging.INFO,
        "{levelname:8} {asctime:23} - {name} - {message}"
    )

    # Create a warning handler to print warning messages to std-err
    warning_handler = create_standard_handler(
        False,
        WARNING_HANDLER_NAME,
        logging.WARNING,
        "{levelname:8} {asctime:23} - {name} - {message}"
    )

    # Create a final handler to print all error/critical messages to std-err
    error_handler = create_standard_handler(
        False,
        ERROR_HANDLER_NAME,
        logging.ERROR,
        "{levelname:8} {asctime:23} - {name} - {message}",
        False
    )

    # Capture all log events by default, unless an environment variable is set
    level_str = os.getenv("WAIANN_LOG_LEVEL", str(logging.DEBUG))
    if len(level_str.strip()) == 0:
        level = logging.DEBUG
    else:
        try:
            level = int(level_str)
        except:
            print("Failed to parse log level (10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR): %s" % level_str)
            level = logging.DEBUG

    # Add the handlers to the logger and set the level
    logger.setLevel(level)
    if level <= logging.DEBUG:
        logger.addHandler(debug_handler)
    if level <= logging.INFO:
        logger.addHandler(info_handler)
    if level <= logging.WARNING:
        logger.addHandler(warning_handler)
    if level <= logging.ERROR:
        logger.addHandler(error_handler)

    return logger


# Setup logging
_logger = create_application_root_logger()

# Remove the PIL logging from the debug logger
for handler in _logger.handlers:
    if handler.name == DEBUG_HANDLER_NAME:
        handler.addFilter(lambda record: record.name != 'PIL.PngImagePlugin')


def get_app_logger() -> logging.Logger:
    """
    Gets the root application logger for wai.annotations.
    """
    return _logger
