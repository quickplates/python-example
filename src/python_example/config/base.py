from collections.abc import Iterable
from typing import Self, TextIO

from omegaconf import OmegaConf
from pydantic import BaseSettings, Extra
from pydantic.env_settings import SettingsSourceCallable
from yaml import YAMLError


class ConfigError(Exception):
    """Base class for config errors."""

    pass


class ConfigParseError(ConfigError, ValueError):
    """Raised when config parsing fails."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__("Failed to parse config!", *args, **kwargs)


class BaseConfig(BaseSettings):
    """Base configuration class."""

    class Config:
        """Pydantic configuration."""

        # Environment variables prefix
        env_prefix = "python_example_"
        # Delimiter for nested models in environment variables
        env_nested_delimiter = "__"
        # Use dotenv file if present
        env_file = ".env"
        # Don't raise errors for extra fields
        extra = Extra.allow

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings

    @classmethod
    def load(
        cls: type[Self],
        f: TextIO | None = None,
        overrides: Iterable[str] | None = None,
    ) -> Self:
        """Load config from file and/or overrides.

        Args:
            f: File-like object to load config from.
            overrides: Config overrides in the form of a dotlist.

        Returns:
            Config object.

        Raises:
            ConfigParseError: If config parsing fails.
        """

        try:
            config = OmegaConf.create()
            if f is not None:
                config = OmegaConf.merge(config, OmegaConf.load(f))
            if overrides is not None:
                config = OmegaConf.merge(
                    config, OmegaConf.from_dotlist(list(overrides))
                )
            config = OmegaConf.to_container(config, resolve=True)
            return cls.parse_obj(config)
        except (ValueError, YAMLError) as e:
            raise ConfigParseError from e
