"""retrieving and parsing extended program inforamtion from port.hu."""
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests
from fake_useragent import UserAgent  # type: ignore[import]
from requests.adapters import HTTPAdapter
from urllib3 import Retry

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
    def init_context(cls) -> None:
        """Initialize the request session for a process.

        Only executed in other processes not in the main process.
        """
        cls.session = requests.Session()
        cls.session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml",
                "Accept-Encoding": "gzip, deflate, br",
            },
        )
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        cls.session.mount("http://", adapter)
        cls.session.mount("https://", adapter)

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
            headers={"User-Agent": UserAgent().random},
        )
        if rsp.status_code == requests.codes.OK:
            return ProcResult(create_xprogramme(json, rsp))

        err = (
            f"Response code indicating failure: {rsp.status_code}. "
            f"Retrieving program details failed. Url: {rsp.url} "
            "Using basic information."
        )
        return ProcResult(create_xprogramme(json), err)
