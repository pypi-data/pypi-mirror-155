import logging
from typing import TypeVar


TFormatter = TypeVar("TFormatter", bound=logging.Formatter, covariant=True)
