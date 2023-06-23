import logging
from typing import Optional

import typer

from python_example.config import Config, ConfigError
from python_example.foo import foo
from python_example.log import Logging, LoggingVerbosity

cli = typer.Typer()
logger = logging.getLogger(__name__)


@cli.command()
def main(
    config_file: Optional[typer.FileText] = typer.Option(
        None,
        "--config-file",
        "-C",
        dir_okay=False,
        help="Configuration file.",
    ),
    config_overrides: Optional[list[str]] = typer.Option(
        None,
        "--config",
        "-c",
        help="Configuration entries.",
    ),
    verbosity: LoggingVerbosity = typer.Option(
        LoggingVerbosity.INFO,
        "--verbosity",
        "-v",
        help="Verbosity level.",
    ),
) -> None:
    """Main entry point."""

    Logging.configure(verbosity)

    logger.info("Loading config...")
    try:
        cfg = Config.load(config_file, config_overrides)
    except ConfigError as e:
        logger.exception("Failed to load config!", exc_info=e)
        raise typer.Exit(1) from e
    logger.info("Config loaded!")

    logger.info(f"Config: {cfg}")
    logger.info(f"foo() = {foo()}")


if __name__ == "__main__":
    cli()
