"""The hu_porthu grabber."""
import argparse
import logging
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from math import floor
from typing import Dict, List, NoReturn, Optional, Tuple

import requests
from fake_useragent import UserAgent  # type: ignore[import]

from pyepggrab.ask import ask_boolean, ask_many_boolean
from pyepggrab.configmanager import ConfigManager
from pyepggrab.grabbers.hu_porthu.config import (
    Channel,
    GrabberConfig,
    GrabberConfigEncoder,
)
from pyepggrab.grabbers.hu_porthu.request_proc import ProcessCtx
from pyepggrab.grabbers.hu_porthu.utils import (
    INIT_URL,
    PROGLIST_URL,
    portid_to_xmlid,
    xmlid_to_portid,
)
from pyepggrab.grabbers.hu_porthu.xml_utils import (
    create_xmltvchannel,
    create_xprogramme,
)
from pyepggrab.log import Log
from pyepggrab.pyepggrab import Pyepggrab
from pyepggrab.xmltv import XmltvChannel, XmltvProgramme, XmltvTv
from pyepggrab.xmlwriter import writexml

try:
    from zoneinfo import ZoneInfo  # type: ignore # noqa: F401, RUF100
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore # noqa: F401, RUF100

GRABBER_VERSION = "v1"
GRABBER_DESCRIPTION = "Hungary (port.hu)"
GRABBER_CAPABILITIES = ["baseline", "manualconfig"]


@dataclass
class ApiLimits:
    """Limits of the port.hu API."""

    valid: bool
    days: int
    channels: List[Channel]


def get_simple_channel_list() -> List[dict]:
    """Return the list of channels that currently supported."""
    sess = requests.session()
    sess.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Encoding": "gzip, deflate, br",
        },
    )
    sess.headers["User-Agent"] = UserAgent().random

    rsp = sess.get(INIT_URL)
    if rsp.status_code == requests.codes.OK:
        chlist = rsp.json()
        return chlist["channels"]
    return []


def build_url_map(progjsons: List[Dict]) -> Dict[Optional[str], List[Dict]]:
    """Group programs by url to save network traffic later."""
    progmap: Dict[Optional[str], List[Dict]] = {}
    for progjson in progjsons:
        key = progjson.get("film_url")

        if key not in progmap:
            progmap[key] = []

        progmap[key].append(progjson)
    return progmap


def fetch_prog_info(jsons: List[Dict], slow: bool, jobs: int) -> List[XmltvProgramme]:
    """Fetch program informations and create XMLTV Programme from them.

    :param jsons: programs returned by port.hu api in json format
    :param slow: query the program page to obtain extended information
    :param jobs: number of parallel processes to run if `slow` is `true`
    """
    progs: List[XmltvProgramme] = []
    log = Log.get_grabber_logger()

    if slow:
        progmap = build_url_map(jsons)

        log.debug("Using slow mode")
        log.debug(
            "URL statistics: %d total, %d unique, %d none",
            len(jsons),
            len(progmap),
            len(progmap.get(None, [])),
        )

        total = len(jsons) - len(progmap.get(None, []))
        onepercent = total / 100
        nextpercent = onepercent
        current = 0

        log.debug("Downloading details and generating programs")
        url, progjsons = zip(*[(k, v) for k, v in progmap.items() if k])
        with ProcessPoolExecutor(
            max_workers=jobs,
            initializer=ProcessCtx.init_context,
        ) as ppe:
            for result in ppe.map(ProcessCtx.gen_programs, url, progjsons):
                if result.error:
                    log.warning(result.error)

                progs += result.result
                current += len(result.result)
                if current >= nextpercent:
                    log.info(
                        "%d%% completed (%d/%d)",
                        int(current / onepercent),
                        current,
                        total,
                    )
                    nextpercent = (floor(current / onepercent) + 1) * onepercent
        log.debug("Downloading details and generating programs done")
    else:
        progmap = {None: jsons}

    noneurls = progmap.get(None, [])
    if len(noneurls) > 0:
        log.debug("Generating urlless programs")

        progs += create_xprogramme(noneurls)

        log.debug("Generating urlless programs done")

    log.debug("Generated %d programs", len(progs))
    return progs


def check_expected_channels(
    expected_ids: List[str],
    retrieved_ids: List[str],
    day: date,
) -> None:
    """Check if the number of retrieved channels are same as requested.

    If they are different may indicate an error on our or on port.hu side.
    Either way the programs for these channels are going to be missing so warn about it
    """
    log = Log.get_grabber_logger()

    if len(expected_ids) == len(retrieved_ids):
        return

    if len(retrieved_ids) == 0:
        log.debug("No programs received on %s", str(day))
    else:
        log.warning(
            "Requested and received channel count does not match (%d != %d) "
            "for day %s",
            len(expected_ids),
            len(retrieved_ids),
            str(day),
        )
    if log.getEffectiveLevel() <= logging.DEBUG:
        for exp in expected_ids:
            # exp is port style
            xmlexp = portid_to_xmlid(exp)
            if xmlexp not in retrieved_ids:
                log.debug("Missing channel: %s", xmlexp)

        for recv in retrieved_ids:
            # recv is xmlid style
            portrecv = xmlid_to_portid(recv)
            if portrecv not in expected_ids:
                log.debug("Extra channel: %s", recv)


def extract_channel_prog(ch: Dict) -> List[Dict]:
    """Extract the list of programs on a chennel from the port.hu api json."""
    ret_json: List[Dict] = []
    prog: dict
    for prog in ch["programs"]:
        ret_json.append(prog)
    return ret_json


def add_new_progs(progjsons: List[dict], exceptedday: date, ch: dict) -> None:
    """Add new programs on `ch` to `progjsons` if they are on the `expectedday`."""
    log = Log.get_grabber_logger()

    for progjson in extract_channel_prog(ch):
        if "start_datetime" in progjson:
            start_date = datetime.fromisoformat(progjson["start_datetime"]).date()
            if start_date == exceptedday:
                progjsons.append(progjson)
            else:
                log.debug(
                    "Program start time is outside of the day. "
                    "Skipped. day: %s, program: %s (%s) - %s",
                    str(exceptedday),
                    str(progjson["title"]),
                    str(progjson["id"]),
                    str(progjson["start_datetime"]),
                )
        else:
            log.warning("Invalid program. Skipped. program: %s", str(progjson))


def add_new_channel(channels: Dict[str, XmltvChannel], ch: dict) -> None:
    """Add new channel (`ch`) to `channels` if not already exists."""
    xch = create_xmltvchannel(ch)
    if xch.id_ not in channels:
        channels[xch.id_] = xch


def extract_channel_data(
    jsonrsp: dict,
    expected_chan_ids: List[str],
    start_day: date,
) -> Tuple[Dict[str, XmltvChannel], List[Dict]]:
    """Extract channels and programs from port.hu api response.

    Take day boundaries into account to conform with XMLTV requirements
    (port.hu not keeping exact boundaries)
    """
    channels: Dict[str, XmltvChannel] = {}
    progjsons: List[Dict] = []
    day = start_day
    for dayprog in jsonrsp.values():
        day_channels: Dict[str, XmltvChannel] = {}
        for ch in dayprog["channels"]:
            add_new_channel(day_channels, ch)
            add_new_progs(progjsons, day, ch)
        check_expected_channels(expected_chan_ids, list(day_channels), day)
        channels = {**day_channels, **channels}
        day += timedelta(days=1)
    return channels, progjsons


def get_api_limits() -> ApiLimits:
    """Retrieve the current state of the API."""
    valid = True
    days = 0
    channels: List[Channel] = []

    sess = requests.session()
    sess.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Encoding": "gzip, deflate, br",
        },
    )
    sess.headers["User-Agent"] = UserAgent().random
    response = sess.get(INIT_URL)
    if response.status_code == requests.codes.OK:
        resp_json: dict = response.json()

        j_days = resp_json.get("days")
        if j_days:
            days = len(j_days)
        else:
            valid = False

        j_channels = resp_json.get("channels")
        if j_channels:
            channels = []
            for ch in j_channels:
                conf_ch = ch_to_configchannel(ch)
                if conf_ch.id_ in [None, ""]:
                    valid = False
                channels.append(conf_ch)

    return ApiLimits(valid, days, channels)


def retrieve_guide(
    chan_ids: List[str],
    days: int = 0,
    offset: int = 0,
    slow: bool = False,
    jobs: int = 1,
) -> XmltvTv:
    """Retrieve guide from port.hu api.

    :param chan_ids: channel ids to be retrieved (port.hu id format (tvchannel-*))
    :param days: how many days to retrieve
    :param offset: start `offset` days after today
    :param slow: retrieve webpages to extract extended information
    :param jobs: number of parallel  jobs to run if `slow` is `true`
    """
    log = Log.get_grabber_logger()

    sess = requests.session()
    sess.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Encoding": "gzip, deflate, br",
        },
    )
    sess.headers["User-Agent"] = UserAgent().random
    dateformat = "%Y-%m-%d"
    date_from = datetime.now(ZoneInfo("Europe/Budapest")).date() + timedelta(
        days=offset,
    )
    # date_from = date.today() + timedelta(days=offset)
    date_to = date_from + timedelta(days=days)

    log.info(
        "retrieving programs from %s to %s for %d channel(s)",
        date_from.strftime(dateformat),
        date_to.strftime(dateformat),
        len(chan_ids),
    )

    response = sess.get(
        PROGLIST_URL,
        params={
            "channel_id[]": chan_ids,
            "i_datetime_from": date_from.strftime(dateformat),
            "i_datetime_to": date_to.strftime(dateformat),
        },
    )

    channels: Dict[str, XmltvChannel] = {}
    progjsons: List[Dict] = []
    if response.status_code == requests.codes.OK:
        channels, progjsons = extract_channel_data(response.json(), chan_ids, date_from)

    log.debug("Retrieved %d programs on %d channel(s)", len(progjsons), len(channels))

    tv = XmltvTv()
    if len(progjsons) > 0:
        try:
            progs = fetch_prog_info(progjsons, slow, jobs)
            tv.channels = list(channels.values())
            tv.programmes = progs
        except Exception:
            log.exception("Exception occurred while fetching programs")
    else:
        log.warning("No programs found")
        return tv

    return tv


def ch_to_configchannel(chlistentry: Dict) -> Channel:
    """Convert a json channel to `Channel`."""
    chid = portid_to_xmlid(chlistentry["id"])
    return Channel(id_=chid, name=chlistentry["name"], enabled=False)


@Pyepggrab.grabber_config
def configure(
    args: argparse.Namespace,
    confman: ConfigManager[GrabberConfig],
) -> Optional[int]:
    """Grabber configuration function.

    Creates or modifies existing configuration.
    Called by pyepggrab if `--configure` supplied
    """
    try:
        conf = confman.read_config()
    except FileNotFoundError:
        conf = GrabberConfig(options={}, channels=[])

    add_options = ask_boolean(
        "Add the current parameters to the config file?\n"
        "This causes the values in the file to be used, "
        "but can be overridden with command line parameters",
    )
    if add_options:
        conf.options = {}
        for opt in ("loglevel", "quiet", "output", "days", "offset", "slow", "jobs"):
            conf.options[opt] = getattr(args, opt)

    emptyconf = len(conf.channels) == 0
    if not emptyconf:
        reconf = ask_boolean("Reconfigure channels?\nDefaults are the current settings")

    if emptyconf or reconf:
        channels = [ch_to_configchannel(ch) for ch in get_simple_channel_list()]

        channum = len(channels)
        allyes = None
        for i, ch in zip(range(1, channum + 1), channels):
            if allyes is None:
                default = next(
                    (confc.enabled for confc in conf.channels if confc.id_ == ch.id_),
                    True,
                )
                resp = ask_many_boolean(
                    f"Include '{ch.name}' ({ch.id_}) in the guide? ({i}/{channum})",
                    default_yes=default,
                )
                ch.enabled = resp in ["yes", "all"]
                if resp == "all":
                    allyes = True
                elif resp == "none":
                    allyes = False
            else:
                ch.enabled = allyes
        conf.channels = channels

    confman.write_config(conf)
    return 0


@Pyepggrab.grabber_extraargs
def extraargs(argp: argparse.ArgumentParser) -> None:
    """Add grabber specific arguments to argparser.

    Called by pyepggrab
    """
    argp.add_argument(
        "--slow",
        action="store_true",
        help=(
            "Use a significantly slower, but more detailed mode to download the guide. "
            "This adds information like description, actors, etc"
        ),
    )
    argp.add_argument(
        "--jobs",
        type=int,
        default=1,
        help=(
            "Number of parallel processes used to download the guide. "
            "Only used in --slow mode. Setting this value too high may result in "
            "high resource usage and/or getting banned from port.hu"
        ),
    )


@Pyepggrab.grabber_main
def main(
    args: argparse.Namespace,
    confman: ConfigManager[GrabberConfig],
) -> Optional[int]:
    """Start graber in normal operation (not configuring).

    Called by pyepggrab
    """
    log = Log.get_grabber_logger()

    if not confman.is_config_exists():
        log.error(
            "Config file not found. "
            "Please run the script with the --configure parameter",
        )
        return 1

    conf = confman.read_config()
    enabled_ch_list = [ch for ch in conf.channels if ch.enabled]

    if log.getEffectiveLevel() <= logging.DEBUG:
        log.debug("Enabled channels:")
        for ch in conf.channels:
            if ch.enabled:
                log.debug("%s - %s", ch.id_, ch.name)

    limits = get_api_limits()

    if not limits.valid:
        log.warning(
            "Failed to retrieve the API limits. "
            "This may indicate changed API or error in communication",
        )
    else:
        chlimit_ids = [ch.id_ for ch in limits.channels]
        for en_ch in enabled_ch_list:
            if en_ch.id_ not in chlimit_ids:
                log.warning(
                    "Channel '%s'(%s) not available on the API. (Maybe temporarly)",
                    en_ch.name,
                    en_ch.id_,
                )

    days = args.days
    if days is None:
        if limits.valid:
            log.info(
                "No days specified, retrieving all currently available (%d)",
                limits.days,
            )
            days = limits.days
        else:
            log.info("No days specified, retrieving maximum of 30 days")
            days = 30

    if limits.valid and days > limits.days:
        log.warning(
            "Specified number of days (%d) is larger than available, "
            "expect no programs after %d day(s)",
            days,
            limits.days,
        )

    enabled_ch_portids = [xmlid_to_portid(ch.id_) for ch in enabled_ch_list]

    guide = retrieve_guide(enabled_ch_portids, days, args.offset, args.slow, args.jobs)
    writexml(guide, args.output)
    return 0


def run(**kwargs) -> NoReturn:
    """Entrypoint to start the grabber by calling `pyepggrab_main()`."""
    Pyepggrab.main(
        version=GRABBER_VERSION,
        description=GRABBER_DESCRIPTION,
        caps=GRABBER_CAPABILITIES,
        config_root=GrabberConfig,
        config_encoder=GrabberConfigEncoder,
        **kwargs,
    )


if __name__ == "__main__":
    run()
