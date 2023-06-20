"""Argument parser for the common XMLTV parameters.

Handles the execution of common arguments like --version or --capabilities

capabilities are same as described in the original XMLTV docs:
http://wiki.xmltv.org/index.php/XmltvCapabilities
"""
import argparse
import logging
import sys
from typing import Callable, List, Optional, Sequence

from pyepggrab import __about__
from pyepggrab.log import Log

ExtraargsType = Callable[[argparse.ArgumentParser], None]


class ArgParser:
    """Handle argument parsing and executing of common arguments."""

    def __init__(
        self,
        version: str,
        description: str,
        caps: List[str],
        extraargs_cb: Optional[ExtraargsType] = None,
    ) -> None:
        """Initialize `Argparser`.

        :param version: version of the grabber
        :param description: description of the grabber
        :param caps: capabilities of the grabber
        :param extraargs_cb: Callback to the grabber to add extra arguments
        """
        self._version = version
        self._description = description
        self._caps = caps
        self._args: Optional[argparse.Namespace] = None

        self.parser = argparse.ArgumentParser()
        prs = self.parser
        prs.add_argument("--pyepggrabver", action="store_true")

        prs.add_argument("-l", "--loglevel", dest="loglevel", default=logging.WARNING)
        prs.add_argument(
            "-d",
            "--debug",
            action="store_const",
            dest="loglevel",
            const=logging.DEBUG,
        )
        prs.add_argument(
            "-v",
            "--verbose",
            action="store_const",
            dest="loglevel",
            const=logging.INFO,
        )

        # XMLTV
        prs.add_argument("-q", "--quiet", action="store_true")
        prs.add_argument("--version", action="store_true")
        prs.add_argument("--description", dest="desc", action="store_true")
        prs.add_argument("--capabilities", action="store_true")

        if "baseline" in caps:
            # --quiet should be here but it's provided by default
            prs.add_argument("--output")
            prs.add_argument("--days", type=int)
            prs.add_argument("--offset", type=int, default=0)
            prs.add_argument("--config-file")

        if "manualconfig" in caps:
            prs.add_argument("--configure", action="store_true")

        if extraargs_cb:
            extraargs_cb(prs)

    def parse_args(self, args: Optional[Sequence[str]] = None) -> argparse.Namespace:
        """Parse arguments. Optionally override them with `args`."""
        self._args = self.parser.parse_args(args=args)
        return self._args

    def exec_common(self) -> None:
        """Execute functionality that every grabber should do.

        Arguments must be parsed before
        """
        if not self._args:
            msg = "No arguemnts. Use 'parse_args()' before calling"
            raise ValueError(msg)

        args = self._args

        if args.quiet:
            Log.disable_loggers()
        else:
            Log.set_loglevel(args.loglevel)

        if args.version:
            print(self._version)
            sys.exit(0)

        if args.pyepggrabver:
            print(__about__.__version__)
            sys.exit(0)

        if args.desc:
            print(self._description)
            sys.exit(0)

        if args.capabilities:
            print("\n".join(self._caps))
            sys.exit(0)
