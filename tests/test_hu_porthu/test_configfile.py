import os
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
        fd, self.tmpfile = tempfile.mkstemp(prefix="test_")
        os.close(fd)

        self.confmgr = ConfigManager(
            self.tmpfile,
            GrabberConfig,
            GrabberConfigEncoder,
        )

        Log.init_loggers()
        Log.set_loglevel("DEBUG")
        Log.finalize_loggers()

    def tearDown(self) -> None:
        os.remove(self.tmpfile)

    def test_read_config(self) -> None:
        with open(self.tmpfile, "w") as f:
            f.write(config_json)

        cfg = self.confmgr.read_config()

        self.assertEqual(cfg, config_object)

    def test_write_config(self) -> None:
        self.confmgr.write_config(config_object)

        jsoncfg = ""
        with open(self.tmpfile) as f:
            jsoncfg = f.read()

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
