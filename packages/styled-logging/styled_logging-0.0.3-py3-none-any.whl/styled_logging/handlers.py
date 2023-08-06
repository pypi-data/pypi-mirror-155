import logging

from .decorator import prettify
from .formatters import MultiFormatter


def create_console_handler(
    level: int = logging.INFO,
    formatter: logging.Formatter = None,
):
    """
    Create a logging handler to display messages in the console

    Parameters
    ----------
    `level` : int, default logging.INFO
        The logging level to set the handler to
    `formatter` : logging.Formatter, default None
        Can be used to override the formatter.
        If None, uses styled_logging.MultiFormatter
    """
    formatter = formatter or prettify(MultiFormatter, color=True, indent=4)()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    return console_handler


def create_file_handler(
    path: str,
    level: int = logging.WARNING,
    formatter: logging.Formatter = None,
):
    """
    Create a file handler to log messages to a file

    Parameters
    ----------
    `path` : path-like
        The path to the log file
    `level` : int, default logging.WARNING
        Th logging level to set the handler to
    `formatter` : logging.Formatter, default None
        Can be used to override the formatter.
        If None, uses a prettified logging.Formatter with format:
        `"%(levelname)s:%(asctime)s:%(name)s:%(message)s"`
    """
    formatter = formatter or prettify(logging.Formatter, color=False, indent=4)(
        "%(levelname)s:%(asctime)s:%(name)s:%(message)s"
    )
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    return file_handler
