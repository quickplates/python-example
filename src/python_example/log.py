import logging
from enum import Enum

from rich.logging import RichHandler


class LoggingVerbosity(str, Enum):
    """Verbosity levels for logging."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def __str__(self) -> str:
        return self.value


class CustomLoggingHandler(RichHandler):
    """Custom logging handler with some default settings."""

    def __init__(
        self,
        *args,
        rich_tracebacks: bool = True,
        show_path: bool = False,
        formatter: logging.Formatter | None = None,
        **kwargs,
    ):
        if formatter is None:
            formatter = logging.Formatter(fmt="%(message)s", datefmt="[%X]")
        super().__init__(
            *args,
            rich_tracebacks=rich_tracebacks,
            show_path=show_path,
            **kwargs,
        )
        self.setFormatter(formatter)


class Logging:
    @staticmethod
    def configure(
        verbosity: LoggingVerbosity = LoggingVerbosity.INFO,
        handler: logging.Handler | None = None,
        **kwargs,
    ) -> None:
        """Call this function to configure logging."""

        if handler is None:
            handler = CustomLoggingHandler()

        logging.basicConfig(
            level=verbosity.value,
            handlers=[handler],
            **kwargs,
        )
