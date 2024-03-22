"""Convenience methods for writing and validating xml."""

from pathlib import Path
from typing import Optional

from lxml import etree

from .log import Log
from .xmltv import XmltvTv


def writexml(xml: XmltvTv, path: Optional[str] = None, validate: bool = True) -> bool:
    """Write the contents of `xml` to a file or to the stdout.

    :param xml: xml contents
    :param path: path to the file where the xml should be saved,
    if `None`, printed to the stdout
    :param validate: Validate the xml contents against the XMLTV DTD
    """
    log = Log.get_pyepggrab_logger()

    if validate:
        # use str path because lxml < 4.8.0 does not support path-like objects
        dtd = etree.DTD(str(Path(Path(__file__).parent, "resources/xmltv.dtd")))
        if not dtd.validate(xml.to_xmltree()):
            log.error("XML not valid")
            # _ErrorLog is iterable: https://lxml.de/api/lxml.etree._ErrorLog-class.html
            for err in dtd.error_log:  # type: ignore[attr-defined]
                log.error(err)
            return False
        log.debug("XML valid")

    if path:
        log.debug("Writing to file %s", path)
        with open(path, "w", encoding="UTF-8") as file:
            file.write(xml.to_str())
    else:
        log.debug("Writing to stdout")
        print(xml.to_str())

    return True
