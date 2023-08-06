# Styled Logging

A collection of logging utilities to prettify logs in Python applications.

## Install

```
pip install styled-logging
```

## Usage

The most basic usage:

```py
from styled_logging import setup
setup()
```

This will print pretty messages to the console, and does not log to a file.

By default, the console will log at INFO level.

You can also use the context manager (recommended):

```py
from styled_logging import logging_context

with logging_context():
    ...
```

## Recipes

### Logging to a file

With quick setup:

```py
from styled_logging import setup
setup(filename="test.log")
```

Or with more options:

```py
import logging
from styled_logging import (
    logging_context,
    create_file_handler,
    create_console_handler,
)


if __name__ == "__main__":

    with logging_context(
        handlers=[
            create_console_handler(level=logging.DEBUG),
            create_file_handler("test.log"),
        ],
    ):
        try:
            logging.debug("A debug message")
            logging.info("An info message")
            logging.warning("A warning message")
            logging.error("An error message")
            raise ValueError("A critical message from an exception")
        except Exception as exc:
            # adding exc_info=True should not be done in production!
            logging.critical(str(exc), exc_info=True)
```

This will print the following in the console:

![example](images/example.png)

And write output in `test.log`:

```log
WARNING:2022-06-14 17:59:51,794:root:A warning message
ERROR:2022-06-14 17:59:51,794:root:An error message
CRITICAL:2022-06-14 17:59:51,794:root:A critical message from an exception
    Traceback (most recent call last):
        /home/eb/projects/cli-logging/example.py  <module>  20: raise ValueError("A critical message from an exception")
    ValueError: A critical message from an exception
```

### Change the format of a specific level

You can pass a custom formatter to `create_console_formatter` which contains an overridden format for a specific log level:

```py
import logging
from styled_logging import (
    cli_logging_context,
    create_file_handler,
    create_console_handler,
    MultiFormatter,
    DEFAULT_FORMATS,
    make_formatters,
    style,
    prettify,
)


if __name__ == "__main__":

    my_formats = {
        **DEFAULT_FORMATS,
        logging.INFO: style("INFO ", fg="white") + " | %(message)s",
    }

    my_formatters = make_formatters(my_formats)

    with logging_context(
        handlers=[
            create_console_handler(
                level=logging.DEBUG,
                formatter=prettify(MultiFormatter)(formatters=my_formatters),
            ),
            create_file_handler("test.log"),
        ],
    ):
        try:
            logging.debug("A debug message")
            logging.info("An info message")
            logging.warning("A warning message")
            logging.error("An error message")
            raise ValueError("A critical message from an exception")
        except Exception as exc:
            logging.critical(str(exc), exc_info=True)

```

![example with format](./images/example-fmt.png)

### Use a custom file handler for file rotation

Creating your own handler is simple:

```py
import logging
from styled_logging import prettify

formatter = prettify(logging.Formatter, color=False)(
    "%(levelname)s:%(asctime)s:%(name)s:%(message)s"
)
# rotate the file every day
file_handler = logging.handlers.TimedRotatingFileHandler(path, when="D")
file_handler.setFormatter(formatter)
file_handler.setLevel(level)
```

Then, use the custom handler:

```py
with logging_context(handlers=[file_handler]):
    ...
```

### Configure logging permanently

The logging context is a context manager, so just call its `__enter__` method:

```py
logging_context(...).__enter__()
```

This can be useful for setting up the logging inside a `click` main function, for example.

### Adding pretty exceptions

This package provides a `prettify` class wrapper to prettify exceptions for a formatter:

```py
from styled_logging import prettify

@prettify(color=True, indent=4)
class MyFormatter(logging.Formatter)
    ...
```

Or, just wrap the base formatter:

```py
from styled_logging import prettify
import logging

PrettyFormatter = prettify(logging.Formatter, color=True, indent=4)
```

`color` controls whether or not the exception text contains color. `indent` will indent the exception text underneath the log message.
