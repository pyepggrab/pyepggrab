import tempfile
import unittest

from pyepggrab.configmanager import ConfigManager
from pyepggrab.grabbers.hu_porthu.config import (
    Channel,
    GrabberConfig,
    GrabberConfigEncoder,
)
from pyepggrab.log import Log


class TestConfigfile(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpfile = tempfile.NamedTemporaryFile()
        self.confmgr = ConfigManager(
            self.tmpfile.name,
            GrabberConfig,
            GrabberConfigEncoder,
        )

        Log.init_loggers()
        Log.set_loglevel("DEBUG")
        Log.finalize_loggers()

    def tearDown(self) -> None:
        self.tmpfile.close()

    def test_read_config(self) -> None:
        self.tmpfile.write(config_json.encode())
        self.tmpfile.flush()

        cfg = self.confmgr.read_config()

        self.assertEqual(cfg, config_object)

    def test_write_config(self) -> None:
        self.confmgr.write_config(config_object)

        jsoncfg = self.tmpfile.read().decode()

        self.assertEqual(jsoncfg, config_json)


config_json = """{
  "options": {
    "loglevel": 10,
    "slow": true
  },
  "channels": [
    {
      "id": "5.port.hu",
      "name": "RTL",
      "enabled": false
    },
    {
      "id": "3.port.hu",
      "name": "TV2",
      "enabled": true
    }
  ]
}"""

config_object = GrabberConfig(
    options={
        "loglevel": 10,
        "slow": True,
    },
    channels=[
        Channel(
            id_="5.port.hu",
            name="RTL",
            enabled=False,
        ),
        Channel(
            id_="3.port.hu",
            name="TV2",
            enabled=True,
        ),
    ],
)
