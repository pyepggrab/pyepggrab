"""Classes used in the configuration file."""

from dataclasses import asdict, dataclass
from typing import List, Type

from pyepggrab.configbase import ConfigBase, ConfigRootBase, T

try:
    from typing import override  # type: ignore # noqa: F401, RUF100
except ImportError:
    from typing_extensions import override  # type: ignore # noqa: F401, RUF100


@dataclass
class Channel(ConfigBase):
    """A channel entry in the config file."""

    id_: str
    name: str
    enabled: bool

    @override
    @classmethod
    def from_dict(cls: Type[T], d: dict) -> "Channel":
        id_ = d.get("id", "")
        name = d.get("name", "")
        enabled = d.get("enabled", False)
        return Channel(id_, name, enabled)


@dataclass
class GrabberConfig(ConfigRootBase):
    """Root of the grabber config with a channels list to store its settings."""

    channels: List[Channel]

    @override
    @classmethod
    def from_dict(cls: Type[T], d: dict) -> "GrabberConfig":
        channels = [Channel.from_dict(ch) for ch in d.get("channels", [])]
        conf = ConfigRootBase.from_dict(d)
        return GrabberConfig(**asdict(conf), channels=channels)
