import logging
from typing import Sequence

from .handlers import create_console_handler


class LoggingContext:
    """A context manager that will change the log settings temporarily"""

    def __init__(
        self,
        logger: logging.Logger = None,
        level: int = None,
        handler: logging.Handler = None,
        close: bool = True,
    ):
        self.logger = logger or logging.root
        self.level = level
        self.handler = handler
        self.close = close

    def __enter__(self):
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)

        if self.handler:
            self.logger.addHandler(self.handler)

    def __exit__(self, *exc_info):
        if self.level is not None:
            self.logger.setLevel(self.old_level)

        if self.handler:
            self.logger.removeHandler(self.handler)

        if self.handler and self.close:
            self.handler.close()


class MultiContext:
    """Can be used to dynamically combine context managers"""

    def __init__(self, *contexts) -> None:
        self.contexts = contexts

    def __enter__(self):
        return tuple(ctx.__enter__() for ctx in self.contexts)

    def __exit__(self, *exc_info):
        for ctx in self.contexts:
            ctx.__exit__(*exc_info)


def create_base_context(
    handlers: Sequence[logging.Handler],
    logger: logging.Logger = None,
):
    """Create a base logging context to set the minimum log level between multiple handlers"""
    return LoggingContext(logger=logger, level=min(h.level for h in handlers))


def logging_context(
    logger: logging.Logger = None,
    handlers: Sequence[logging.Handler] = None,
):
    """
    Create a logging context

    Parameters
    ----------
    `logger` : logging.Logger, default None
        The logger to configure, defaults to the root logger

    `handlers` : sequence logging.Handler, default None
        logging handlers to use
        Create a console handler with create_console_handler
        Create a file handler with styled_logging.create_file_handler
        If None, creates a console handler with default values.
    """
    handlers = handlers or [create_console_handler()]

    contexts = [create_base_context(handlers, logger)]

    contexts.extend(
        LoggingContext(logger=logger, handler=handler) for handler in handlers
    )

    return MultiContext(*contexts)
