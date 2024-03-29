"""Configuration manager for grabber configuration files.

Configuration files are JSON files.

Using the default parameters the config only stores the `options` dict.

{
    options: {
        ...
    }
}

If a grabber want to store more data in the config file the `root` can be
changed to a subclass of `ConfigBase`, but subclass of `ConfigRootBase` is
recommended to keep the `options` dict in the config. Other classes used in the
config are recommended to be a subclass of `ConfigBase`, but any other class
can be used in the config.
"""

import json
import sys
from json import JSONDecoder, JSONEncoder
from pathlib import Path
from typing import Generic, Optional, Type

from pyepggrab.configbase import ConfigEncoder, ConfigRootBase, T
from pyepggrab.log import Log


class ConfigManager(Generic[T]):
    """Handles reading and writing grabber configurations."""

    def __init__(
        self,
        path: Optional[str] = None,
        root: Type[T] = ConfigRootBase,  # type: ignore # see:python/mypy#3737
        encoder: Type[JSONEncoder] = ConfigEncoder,
        decoder: Optional[Type[JSONDecoder]] = None,
    ) -> None:
        """Initialize `ConfigManager`.

        :param path: path of the configuration file, if empty, autogenerated.
        ~/.xmltv/{grabber name}.conf
        :param root: type of the configuration root, if custom configuration
        stored this should be changed
        :param encoder: encoder for the config file, the default usually enough
        :param decoder: optional decoder for the config file, usually not needed
        """
        self._root = root
        self._encoder = encoder
        self._decoder = decoder

        if path:
            self._path = Path(path)
        else:
            self._path = self.get_default_config_path()

    def get_config_path(self) -> Path:
        """Return the path to the config file."""
        return self._path

    def is_config_exists(self) -> bool:
        """Return true is the config file exists."""
        return self._path.exists()

    def read_config(self) -> T:
        """Read the config file and return the contents as `root` type."""
        with self._path.open("r", encoding="UTF-8") as file:
            Log.get_pyepggrab_logger().debug("Reading config file %s", self._path)
            conf = json.load(file, cls=self._decoder)
            return self._root.from_dict(conf)

    def write_config(self, config: T) -> None:
        """Write the `root` type config to the config file."""
        configstr = json.dumps(config, cls=self._encoder, indent=2, ensure_ascii=False)

        config_dir = self._path.resolve().parent
        config_dir.mkdir(parents=True, exist_ok=True)

        with self._path.open("w", encoding="UTF-8") as file:
            Log.get_pyepggrab_logger().debug("Writing config file %s", self._path)
            file.write(configstr)

    @staticmethod
    def get_default_config_directory() -> Path:
        """Get the default configuration directory."""
        return Path(Path.home(), ".xmltv")

    @staticmethod
    def get_default_config_name() -> str:
        """Get the default configuration file name."""
        return Path(sys.argv[0]).stem + ".conf"

    @classmethod
    def get_default_config_path(cls) -> Path:
        """Get the default configuration path (dir+name)."""
        return Path(
            cls.get_default_config_directory(),
            cls.get_default_config_name(),
        )
