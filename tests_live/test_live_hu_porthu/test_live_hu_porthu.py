import pathlib
import subprocess
import sys
import tempfile
import unittest

from lxml import etree

TESTDATADIR = pathlib.Path(__file__).parent.joinpath("testdata")
MODULE = "pyepggrab.grabbers.hu_porthu.hu_porthu"


class TestLiveHuPorthu(unittest.TestCase):
    def test_simple(self) -> None:
        with tempfile.NamedTemporaryFile() as tmpfile:
            sp = subprocess.run(
                args=[
                    sys.executable,
                    "-m",
                    MODULE,
                    "--debug",
                    "--config-file",
                    str(TESTDATADIR.joinpath("testconfig.conf")),
                    "--days",
                    "1",
                    "--output",
                    tmpfile.name,
                ],
                capture_output=True,
                check=False,
            )
            print(sp.stderr.decode())

            self.assertEqual(0, sp.returncode)

            xml = etree.parse(tmpfile)
            root = xml.getroot()
            channels = len([c for c in root if c.tag == "channel"])
            programs = len([c for c in root if c.tag == "programme"])

            self.assertEqual(1, channels)
            self.assertGreater(programs, 0)

    def test_simple_noprog(self) -> None:
        with tempfile.NamedTemporaryFile() as tmpfile:
            sp = subprocess.run(
                args=[
                    sys.executable,
                    "-m",
                    MODULE,
                    "--debug",
                    "--config-file",
                    str(TESTDATADIR.joinpath("testconfig.conf")),
                    "--days",
                    "1",
                    "--offset",
                    "30",  # only 15 days of programs available
                    "--output",
                    tmpfile.name,
                ],
                capture_output=True,
                check=False,
            )
            print(sp.stderr.decode())

            self.assertEqual(0, sp.returncode)

            xml = etree.parse(tmpfile)
            root = xml.getroot()
            channels = len([c for c in root if c.tag == "channel"])
            programs = len([c for c in root if c.tag == "programme"])

            self.assertEqual(0, channels)
            self.assertEqual(0, programs)

    def test_slow(self) -> None:
        with tempfile.NamedTemporaryFile() as tmpfile:
            sp = subprocess.run(
                args=[
                    sys.executable,
                    "-m",
                    MODULE,
                    "--debug",
                    "--config-file",
                    str(TESTDATADIR.joinpath("testconfig.conf")),
                    "--days",
                    "1",
                    "--slow",
                    "--jobs",
                    "1",
                    "--output",
                    tmpfile.name,
                ],
                capture_output=True,
                check=False,
            )
            print(sp.stderr.decode())

            self.assertEqual(0, sp.returncode)

            xml = etree.parse(tmpfile)
            root = xml.getroot()
            channels = len([c for c in root if c.tag == "channel"])
            programs = len([c for c in root if c.tag == "programme"])

            self.assertEqual(1, channels)
            self.assertGreater(programs, 0)
