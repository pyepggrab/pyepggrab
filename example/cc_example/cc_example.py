"""The `cc_example` example grabber."""
import argparse
import logging
from datetime import datetime
from typing import NoReturn, Optional

from pyepggrab.ask import ask_boolean
from pyepggrab.configbase import ConfigRootBase
from pyepggrab.configmanager import ConfigManager
from pyepggrab.log import Log
from pyepggrab.pyepggrab import Pyepggrab
from pyepggrab.xmltv import (
    XmltvChannel,
    XmltvDisplayName,
    XmltvProgramme,
    XmltvTitle,
    XmltvTv,
    to_xmltv_date,
)
from pyepggrab.xmlwriter import writexml

GRABBER_VERSION = "v0"
GRABBER_DESCRIPTION = "Example (example)"
GRABBER_CAPABILITIES = ["baseline", "manualconfig"]


@Pyepggrab.grabber_main
def main(
    args: argparse.Namespace,
    confman: ConfigManager[ConfigRootBase],
) -> Optional[int]:
    """Start grabber in normal operation (not configuring).

    This called by Pyepggrab when the grabber started in any other mode than configuring

    The `args` parameter
    --------------------

    `args` contains all arguments that passed on the command line or
    read from the config file

    Note: to read arguments from the config file the config file must contain an
    'options' dict that contains the arguments.

    Example parameters:

    CLI: `cc_example --days 1 --name Bob`

    Config file:

    ```json
    {
        "options": {
            "days": 1,
            "name": "Bob"
        }
    }
    ```

    The `confman` parameter
    -----------------------

    The ConfigManager provides easy access to read and write the config file.

    The root type represents the whole config file. On reading it returns a root
    type object that contains tho contents of the config file. On writing it
    expects the same type.
    More in configmanager.py
    """
    # The loggers are available everywhere.
    # There is one for pyepggrab itself and one for the grabber.
    # If you want you can create more loggers through `create_logger`.
    # Details in log.py
    log = Log.get_grabber_logger()

    if args.name:
        log.warning("Hello %s", args.name)

    if log.getEffectiveLevel() > logging.INFO:
        log.warning("Set logging level to INFO to see more messages. '--loglevel INFO'")

    log.info("Days: %d", args.days if args.days else -1)
    log.info("Offset: %d", args.offset)

    writexml(
        XmltvTv(
            channels=[
                XmltvChannel(
                    id_="1.example",
                    display_names=[XmltvDisplayName("example channel", "en")],
                ),
            ],
            programmes=[
                XmltvProgramme(
                    start=to_xmltv_date(datetime.fromisoformat("2023-01-01T00:00:00Z")),
                    stop=to_xmltv_date(datetime.fromisoformat("2023-01-01T00:01:00Z")),
                    channel="1.example",
                    titles=[
                        XmltvTitle("example programme", "en"),
                    ],
                ),
            ],
        ),
        args.output,
    )

    # Returning something is optional,
    # but if you return a number, it's used as an exit code.
    return 0


@Pyepggrab.grabber_config
def configure(
    args: argparse.Namespace,
    confman: ConfigManager[ConfigRootBase],
) -> Optional[int]:
    """Start grabber in configuration mode.

    This called by Pyepggrab when the grabber started in configuration mode.

    Parameters are same as in `main`
    """
    try:
        conf = confman.read_config()
    except FileNotFoundError:
        conf = ConfigRootBase(options={})

    # More ask_* functions available in `ask.py`
    if ask_boolean("Save parameters in the config?", default_yes=True):
        conf.options = {}
        for opt in ("loglevel", "quiet", "output", "days", "offset", "name"):
            conf.options[opt] = getattr(args, opt)

    confman.write_config(conf)

    return 0


@Pyepggrab.grabber_extraargs
def extraargs(argp: argparse.ArgumentParser) -> None:
    """Add grabber specific arguments to argparser."""
    argp.add_argument("--name", type=str, help="A name to greet")


def run(**kwargs) -> NoReturn:
    """Entrypoint to start the grabber by calling `Pyepggrab.main()`."""
    Pyepggrab.main(
        version=GRABBER_VERSION,
        description=GRABBER_DESCRIPTION,
        caps=GRABBER_CAPABILITIES,
        **kwargs,
    )


if __name__ == "__main__":
    run()
