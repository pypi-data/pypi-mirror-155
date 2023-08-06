import functools
import logging
import textwrap
from typing import Type
from pretty_traceback.formatting import exc_to_traceback_str

from .types import TFormatter


def prettify(cls: Type[TFormatter], color=True, indent=4) -> Type[TFormatter]:
    """Decorator to prettify a logging.Formatter exception output"""

    @functools.wraps(cls, updated=())
    class PrettyFormatter(cls):
        def formatException(self, ei):
            _, exc_value, traceback = ei
            return textwrap.indent(
                exc_to_traceback_str(exc_value, traceback, color=color), " " * indent
            )

        def format(self, record: logging.LogRecord):
            record.exc_text = None
            return super().format(record)

    return PrettyFormatter
