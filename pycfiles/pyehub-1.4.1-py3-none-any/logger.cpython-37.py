# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/logger.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1532 bytes
__doc__ = '\nThis script is an interface for using the logging module to log the running of energy hub model.\n'
import logging

def create_logger(filename: str) -> None:
    """
    Add logging to the application.

    Args:
        filename: The name of the log file
    """
    logging.getLogger().setLevel(logging.DEBUG)
    add_console_handler()
    add_file_handler(filename)


def add_console_handler() -> None:
    """Add a logging handler for stderr."""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(get_default_formatter())
    logging.getLogger().addHandler(console_handler)


def add_file_handler(filename: str) -> None:
    """
    Add a logging handler for a log file.

    Args:
        filename: The name of the log file
    """
    file_handler = logging.FileHandler(filename, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(get_default_formatter())
    logging.getLogger().addHandler(file_handler)


def get_default_formatter() -> logging.Formatter:
    """
    Return a default formatter for logging.

    The format is:
        Hours:Minutes:Second.Milliseconds - Location - [level]: message

    Returns:
        A logging.Formatter for the default format
    """
    return logging.Formatter('%(asctime)s.%(msecs)03d - %(filename)s:%(lineno)d - [%(levelname)s]: %(message)s',
      datefmt='%H:%M:%S')