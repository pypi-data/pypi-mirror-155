import logging
from .handlers import create_console_handler, create_file_handler
from .color import style
from .context import LoggingContext, MultiContext, logging_context
from .formatters import (
    MultiFormatter,
    DEFAULT_FORMATS,
    DEFAULT_FORMATTERS,
    make_formatters,
    DEBUG_FMT,
    INFO_FMT,
    WARNING_FMT,
    ERROR_FMT,
    CRITICAL_FMT,
)
from .decorator import prettify


def setup(
    console_level: int = logging.INFO,
    filename: str = None,
    file_level: int = logging.WARNING,
):
    """Quick logging setup. Supports setting log level, and logging to a file."""
    handlers = [create_console_handler(level=console_level)]
    if filename:
        handlers.append(create_file_handler(filename, level=file_level))

    logging_context(handlers=handlers).__enter__()


__all__ = [
    "create_console_handler",
    "create_file_handler",
    "style",
    "LoggingContext",
    "MultiContext",
    "logging_context",
    "MultiFormatter",
    "DEFAULT_FORMATS",
    "DEFAULT_FORMATTERS",
    "make_formatters",
    "DEBUG_FMT",
    "INFO_FMT",
    "WARNING_FMT",
    "ERROR_FMT",
    "CRITICAL_FMT",
    "setup",
    "prettify",
]

__version__ = "0.0.2"
