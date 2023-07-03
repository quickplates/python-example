from pydantic import Field

from python_example.config.base import BaseConfig


class Config(BaseConfig):
    """Configuration for the application."""

    foo: str = Field(
        "bar",
        title="Foo",
        description="Some random field to demonstrate configuration.",
    )
