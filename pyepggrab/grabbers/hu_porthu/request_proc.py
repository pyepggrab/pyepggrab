"""retrieving and parsing extended program inforamtion from port.hu."""

from dataclasses import dataclass
from multiprocessing import Queue
from typing import Dict, List, Optional

import requests
from pyrate_limiter import Limiter, RequestRate  # type: ignore[import]
from requests_ratelimiter import LimiterSession  # type: ignore[import]

from pyepggrab.grabbers.hu_porthu.use_ip_adapter import UseIPAdapter
from pyepggrab.grabbers.hu_porthu.utils import to_absolute_porturl
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
    def init_context(cls, rate_limit: int, interval: int, ip_queue: Queue) -> None:
        """Initialize the request session for a process.

        :param rate_limit: amount of requests allowed per `interval`
        :param interval: time windows of the `rate_limit`
        :param ip_queue: queue of ip addresses that used by this process to
        communicate (only 1 used)

        Only executed in other processes not in the main process.
        """
        limiter = Limiter(RequestRate(rate_limit, interval))
        cls.session = LimiterSession(limiter=limiter, per_host=False)

        port_ip = ip_queue.get()
        use_ip_adepter = UseIPAdapter({"port.hu": port_ip})
        cls.session.mount("http://", use_ip_adepter)
        cls.session.mount("https://", use_ip_adepter)

    @classmethod
    def gen_programs(cls, url: str, json: List[Dict]) -> ProcResult:
        """Generate XMLTV programs from the `json` and by querying the `url`.

        Only executed in other processes not in the main process.
        """
        if not cls.session:
            msg = "RequestProcess.session missing"
            raise TypeError(msg)

        rsp = cls.session.get(
            to_absolute_porturl(url),
            timeout=30,
        )
        if rsp.status_code == requests.codes.OK:
            return ProcResult(create_xprogramme(json, rsp))

        err = (
            f"Response code indicating failure: {rsp.status_code}. "
            f"Retrieving program details failed. Url: {rsp.url} "
            "Using basic information."
        )
        return ProcResult(create_xprogramme(json), err)
