"""Collection of utilities used in many parts of hu_porthu."""

from typing import Optional

from pyepggrab.utils import remove_prefix, remove_suffix

ID_BASE = ".port.hu"
ID_RADIO = ".radio" + ID_BASE

PORT_TV = "tvchannel-"
PORT_RADIO = "radiochannel-"

HOST = "port.hu"
BASE_URL = f"https://{HOST}/"
INIT_URL = BASE_URL + "tvapi/init"
RADIO_INIT_URL = BASE_URL + "radioapi/init"
PROGLIST_URL = BASE_URL + "tvapi"
RADIO_PROGLIST_URL = BASE_URL + "radioapi"


def portid_to_xmlid(portid: str) -> str:
    """Convert a port.hu id to an xmltv id.

    Port ids are used in the channel ids.

    `tvchannel-123` to `123.port.hu` and
    `radiochannel-123` to `123.radio.port.hu`

    Similar to: `eventid_to_xmlid()`
    """
    if portid.startswith(PORT_RADIO):
        return remove_prefix(portid, PORT_RADIO) + ID_RADIO

    return remove_prefix(portid, PORT_TV) + ID_BASE


def xmlid_to_portid(xmlid: str) -> str:
    """Convert an xmltv id to a port.hu id.

    `123.port.hu` to `tvchannel-123` and
    `123.radio.port.hu` to `radiochannel-123`
    """
    if xmlid.endswith(ID_RADIO):
        return PORT_RADIO + remove_suffix(xmlid, ID_RADIO)

    return PORT_TV + remove_suffix(xmlid, ID_BASE)


def eventid_to_xmlid(eventid: str) -> str:
    """Convert an event-tv id to an xmltv channel id.

    Event ids are used in the program ids.
    This is not compatible with radio event ids.

    `event-tv-1111111111-234` to `234.port.hu`.

    Similar to: `portid_to_xmlid()
    """
    return eventid[eventid.rfind("-") + 1 :] + ID_BASE


def to_friendlyimage(icon: str) -> str:
    """Convert an url to an svg image to a png image.

    pngs are served under the `raster` directory
    """
    if icon.endswith(".svg"):
        return icon.replace("vector", "raster").replace(".svg", ".png")
    return icon


def to_absolute_porturl(url: str) -> str:
    """Append the base url to a relative url."""
    if url.startswith("/"):
        return BASE_URL + url[1:]
    return url


def append_if_not_empty(base: Optional[str], sep: str, *strs: Optional[str]) -> str:
    """Append `strs` to `base` separated by `sep` if `strs` is not empty.

    If `base` or `strs` is empty `sep` is omitted from the result.
    """
    if None in strs or "" in strs:
        if base:
            return base
        return ""

    if base is None or len(base) == 0:
        return "".join([str(v) for v in strs])

    return base + sep + "".join([str(v) for v in strs if v])
