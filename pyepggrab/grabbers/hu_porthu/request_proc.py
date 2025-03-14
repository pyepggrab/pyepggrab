"""retrieving and parsing extended program inforamtion from port.hu."""

import time
from dataclasses import dataclass, field
from logging import INFO, WARNING
from multiprocessing import Queue
from typing import Dict, List, Tuple

import requests

from pyepggrab.grabbers.hu_porthu.use_ip_adapter import UseIPAdapter
from pyepggrab.grabbers.hu_porthu.utils import to_absolute_porturl
from pyepggrab.grabbers.hu_porthu.xml_utils import create_xprogramme
from pyepggrab.xmltv import XmltvProgramme


@dataclass
class ProcResult:
    """Result of a program retrieving process."""

    result: List[XmltvProgramme]
    failed: bool
    retry: bool = False
    logs: List[Tuple[int, str]] = field(default_factory=list)


class ProcessCtx:
    """Every subprocess has its own context and reuses it."""

    session: requests.Session
    target_interval_ns: float
    last: int
    tag: str

    @classmethod
    def init_context(
        cls,
        rate_limit: int,
        interval: int,
        ip_queue: "Queue[str]",
    ) -> None:
        """Initialize the request session for a process.

        :param rate_limit: amount of requests allowed per `interval`
        :param interval: time windows of the `rate_limit`
        :param ip_queue: queue of ip addresses that used by this process to
        communicate (only 1 used)

        Only executed in other processes not in the main process.
        """
        cls.session = requests.Session()

        port_ip = ip_queue.get()
        use_ip_adepter = UseIPAdapter({"port.hu": port_ip})
        cls.session.mount("http://", use_ip_adepter)
        cls.session.mount("https://", use_ip_adepter)

        cls.target_interval_ns = interval / rate_limit * 1_000_000_000
        cls.last = time.monotonic_ns()
        cls.tag = cls._ipv4_to_tag(port_ip)

    @classmethod
    def gen_programs(cls, url: str, json: List[Dict]) -> ProcResult:
        """Generate XMLTV programs from the `json` and by querying the `url`.

        Only executed in other processes not in the main process.
        """
        cls._do_rate_limit()

        if not cls.session:
            msg = "RequestProcess.session missing"
            raise TypeError(msg)

        logs = []

        try:
            rsp = cls.session.get(
                to_absolute_porturl(url),
                timeout=30,
            )
        except requests.Timeout:
            logs = [
                (
                    WARNING,
                    f"{cls.tag} Request timeout. Url: {rsp.url}. ",
                ),
            ]
            return ProcResult(
                create_xprogramme(json),
                failed=True,
                retry=True,
                logs=logs,
            )

        if rsp.status_code == requests.codes.OK:
            return ProcResult(create_xprogramme(json, rsp), failed=False)

        if rsp.status_code == requests.codes.TOO_MANY_REQUESTS:
            old_target = cls.target_interval_ns / 1_000_000_000
            cls.target_interval_ns *= 2
            new_target = cls.target_interval_ns / 1_000_000_000
            logs.extend(
                [
                    (
                        WARNING,
                        f"{cls.tag} Rate limit exceeded. "
                        "You may consider adjusting the rate limit. "
                        "Increasing the time between requests",
                    ),
                    (
                        INFO,
                        f"from {old_target}s to {new_target}s",
                    ),
                ],
            )
            return ProcResult(
                create_xprogramme(json),
                failed=True,
                logs=logs,
                retry=True,
            )

        logs = [
            (
                WARNING,
                f"{cls.tag} Response code indicating failure: {rsp.status_code}. "
                f"Retrieving program details failed. Url: {rsp.url} "
                "Using basic information.",
            ),
        ]
        return ProcResult(create_xprogramme(json), failed=True, logs=logs)

    @classmethod
    def _ipv4_to_tag(cls, ip: str) -> str:
        """Convert an IPv4 address to a log tag."""
        return "[" + ".".join(ip.split(".")[2:]) + "]"

    @classmethod
    def _do_rate_limit(cls) -> None:
        """Sleep to reach the target request rate."""
        now = time.monotonic_ns()
        diff = now - cls.last
        if diff < cls.target_interval_ns:
            time.sleep((cls.target_interval_ns - diff) / 1_000_000_000)

        cls.last = time.monotonic_ns()
