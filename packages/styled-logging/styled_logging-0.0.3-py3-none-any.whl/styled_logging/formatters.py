import logging
import typing as t

from .decorator import prettify
from .color import style
from .types import TFormatter


DEBUG_FMT = style("DEBUG", fg="cyan") + " | " + style("%(message)s", fg="cyan")
INFO_FMT = "%(message)s"
WARNING_FMT = style("WARN ", fg="yellow") + " | " + style("%(message)s", fg="yellow")
ERROR_FMT = style("ERROR", fg="red") + " | " + style("%(message)s", fg="red")
CRITICAL_FMT = (
    style("FATAL", fg="white", bg="red", bold=True)
    + " | "
    + style("%(message)s", fg="red", bold=True)
)

DEFAULT_FORMATS = {
    logging.DEBUG: DEBUG_FMT,
    logging.INFO: INFO_FMT,
    logging.WARNING: WARNING_FMT,
    logging.ERROR: ERROR_FMT,
    logging.CRITICAL: CRITICAL_FMT,
}


def make_formatters(
    formats: t.Dict[int, str], cls: t.Union[t.Type[TFormatter], None] = None, **kwargs
) -> t.Dict[int, TFormatter]:
    """
    Create a mapping of level number to formatter, given:
    - a mapping of level number to format string
    - the formatter class
    - additonal kwargs to pass to the constructor
    """
    if cls is None:
        cls = prettify(logging.Formatter)

    return {level: cls(fmt, **kwargs) for level, fmt in formats.items()}


DEFAULT_FORMATTERS: t.Dict[int, logging.Formatter] = make_formatters(DEFAULT_FORMATS)


class MultiFormatter(logging.Formatter):
    """
    Format log messages differently for each log level

    Parameters
    ----------
    `formatters` : dict of int to logging.Formatter
        This is a mapping of log level to its formatter.
        If a level is omitted, the base logging.Formatter will be used for that level.
    `kwargs` : dict
        Keyword arguments to forward to logging.Formatter.
    """

    def __init__(self, formatters: t.Dict[int, logging.Formatter] = None, **kwargs):
        super().__init__(**kwargs)

        if formatters is None:
            formatters = DEFAULT_FORMATTERS

        self.formatters = formatters

    def format(self, record: logging.LogRecord):
        formatter = self.formatters.get(record.levelno)

        if formatter is None:
            return super().format(record)

        return formatter.format(record)
