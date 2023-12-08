"""retrieving and parsing extended program inforamtion from port.hu."""
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests
from pyrate_limiter import Limiter, RequestRate  # type: ignore[import]
from requests_ratelimiter import LimiterSession  # type: ignore[import]

from pyepggrab.grabbers.hu_porthu.utils import BASE_URL, to_absolute_porturl
from pyepggrab.grabbers.hu_porthu.xml_utils import create_xprogramme
from pyepggrab.xmltv import XmltvProgramme


@dataclass
class ProcResult:
    """Result of a program retrieving process."""

    result: List[XmltvProgramme]
    error: Optional[str] = None


class ProcessCtx:
    """Every subprocess has its own context and reuses it."""

    session: requests.Session

    @classmethod
    def init_context(cls, rate_limit: int, interval: int) -> None:
        """Initialize the request session for a process.

        Only executed in other processes not in the main process.
        """
        limiter = Limiter(RequestRate(rate_limit, interval))
        cls.session = LimiterSession(limiter=limiter, per_host=False)
        cls.session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml",
                "Accept-Encoding": "gzip, deflate, br",
            },
        )

        cls.init_cookies()

    @classmethod
    def init_cookies(cls) -> None:
        """Initialize cookies to be able to query the tvapi.

        By querying this url the following cookies are retrieved:
        `advanced`, `INX_CHECKER2`, `psid`, `legacy-psid`.

        Only executed in other processes not in the main process.
        """
        cls.session.get(BASE_URL + "tv")
        assert len(cls.session.cookies.get_dict()) > 0

    @classmethod
    def gen_programs(cls, url: str, json: List[Dict]) -> ProcResult:
        """Generate XMLTV programs from the `json`and by querying the `url`.

        Only executed in other processes not in the main process.
        """
        if not cls.session:
            msg = "RequestProcess.session missing"
            raise TypeError(msg)

        rsp = cls.session.get(
            to_absolute_porturl(url),
        )
        if rsp.status_code == requests.codes.OK:
            return ProcResult(create_xprogramme(json, rsp))

        err = (
            f"Response code indicating failure: {rsp.status_code}. "
            f"Retrieving program details failed. Url: {rsp.url} "
            "Using basic information."
        )
        return ProcResult(create_xprogramme(json), err)
