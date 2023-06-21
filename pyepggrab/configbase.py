"""Base classes used in the configuration management.

These also provides the default config functionality
"""

from dataclasses import dataclass
from json import JSONEncoder
from typing import Any, Dict, Type, TypeVar

try:
    from typing import override  # type: ignore # noqa: F401, RUF100
except ImportError:
    from typing_extensions import override  # type: ignore # noqa: F401, RUF100

T = TypeVar("T", bound="ConfigBase")


@dataclass
class ConfigBase:
    """Base class for any class that used in the configuration."""

    @classmethod
    def from_dict(cls: Type[T], d: dict) -> T:
        """Recreate this class from the supplied dict."""
        raise NotImplementedError()


@dataclass
class ConfigRootBase(ConfigBase):
    """Base class for config root that supports arguments stored in the config."""

    options: Dict[str, Any]

    @override
    @classmethod
    def from_dict(cls: Type[T], d: dict) -> "ConfigRootBase":
        options = d.get("options", {})
        return ConfigRootBase(options)


class ConfigEncoder(JSONEncoder):
    """Default config encoder. Saves every member variable of the class."""

    @override
    def default(self, o: Any) -> dict:
        return vars(o)
