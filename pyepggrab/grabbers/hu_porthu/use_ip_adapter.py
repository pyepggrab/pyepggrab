"""Adapter for the requests module to avoid DNS queries."""

from typing import Dict, Mapping, Optional, Union
from urllib.parse import urlparse

from requests import PreparedRequest, Response
from requests.adapters import HTTPAdapter
from urllib3 import HTTPConnectionPool


class UseIPAdapter(HTTPAdapter):
    """Replaces the hostname with an IP address to avoid DNS queries.

    TLS SNI, certificate validation and HTTP Host header is handled.
    """

    def __init__(self, host_ip_map: Dict[str, str]) -> None:
        """:param host_ip_map: hostnames mapped to ip addresses"""
        self.host_ip_map = host_ip_map
        super().__init__()

    def _replace_hostname(self, url: str) -> str:
        """Replace hostname in `url` if a mapping exists for it."""
        parurl = urlparse(url)
        for host, ip in self.host_ip_map.items():
            if host == parurl.hostname:
                # NOTE: userinfo maybe replaced
                new_nethost = parurl.netloc.replace(parurl.hostname, ip)
                new_parurl = parurl._replace(netloc=new_nethost)
                return new_parurl.geturl()
        return url

    def _mod_host_header(self, request: PreparedRequest) -> None:
        """Add a Host header to the `request` if required, cleared otherwise."""
        hostname = str(urlparse(request.url).hostname)
        if hostname in self.host_ip_map:
            request.headers.update({"Host": hostname})
            return

        if "host" in request.headers:
            del request.headers["host"]

    def _mod_poolmanager(self, request: PreparedRequest) -> None:
        """Add hostnames to the poolmanager.

        Hostnames are required for successful connection and
        certificate verification.
        """
        pool_kw = self.poolmanager.connection_pool_kw

        parurl = urlparse(request.url)
        if parurl.scheme == "https":
            hostname = parurl.hostname
            if hostname in self.host_ip_map:
                # CN/SAN
                pool_kw["assert_hostname"] = hostname
                # SNI
                pool_kw["server_hostname"] = hostname
                return

        if "assert_hostname" in pool_kw:
            del pool_kw["assert_hostname"]
        if "server_hostname" in pool_kw:
            del pool_kw["server_hostname"]

    def get_connection(
        self,
        url: Union[str, bytes],
        proxies: Optional[Mapping[str, str]] = None,
    ) -> HTTPConnectionPool:
        """Replace hostname and returns a urllib3 connection for `url`."""
        url = self._replace_hostname(str(url))
        return super().get_connection(url, proxies)  # type: ignore[return-value]

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        """Set up poolmanager and send the `request` object."""
        self._mod_host_header(request)
        self._mod_poolmanager(request)
        return super().send(request, *args, **kwargs)
