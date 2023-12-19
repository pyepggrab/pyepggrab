"""Convenience methods for logging.

Loggers created with `create_logger()` are treated as manged loggers.
The managed loggers are benefit from the delayed logging feature if the loggers
are not finalized to avoid outputting unwanted log messages.
"""

import logging
import sys
from typing import ClassVar, Dict, List, Union

from .utils import grabber_name


class Log:
    """Logger of pyepggrab."""

    _finalized: ClassVar[bool] = False
    _delayedlogs: ClassVar[Dict[str, List[logging.LogRecord]]] = {}
    _managed_loggers: ClassVar[List[logging.Logger]] = []

    @classmethod
    def disable_loggers(cls) -> None:
        """Disable any logging output."""
        logging.disable(logging.CRITICAL)

    @classmethod
    def enable_loggers(cls) -> None:
        """Allow logging output."""
        logging.disable(logging.NOTSET)

    @classmethod
    def get_pyepggrab_logger(cls) -> logging.Logger:
        """Return the pyepggrab logger."""
        return logging.getLogger("pyepggrab")

    @classmethod
    def get_grabber_logger(cls) -> logging.Logger:
        """Return the grabber's logger."""
        return logging.getLogger(grabber_name())

    @classmethod
    def logdelay_filter(cls, logrecord: logging.LogRecord) -> bool:
        """Filter out logs until loggers are finalized so no unwanted output happens.

        Logs are replayed when loggers are finalized.
        """
        if not cls._finalized:
            if logrecord.name in cls._delayedlogs:
                cls._delayedlogs[logrecord.name].append(logrecord)
            else:
                cls._delayedlogs[logrecord.name] = [logrecord]
            return False
        return True

    @classmethod
    def reset_logger(cls, logger: logging.Logger) -> None:
        """Reset logger to a known state."""
        logger.filters.clear()
        logger.handlers.clear()

    @classmethod
    def create_logger(cls, name: str, handler: logging.Handler) -> logging.Logger:
        """Create a managed logger.

        If loggers are not finalized yet a logdelay_filter is added to it.
        """
        logger = logging.getLogger(name)
        cls.reset_logger(logger)

        if logger not in cls._managed_loggers:
            cls._managed_loggers.append(logger)

        logger.addHandler(handler)
        if not cls._finalized:
            logger.addFilter(cls.logdelay_filter)
        return logger

    @classmethod
    def init_loggers(cls) -> None:
        """Initialize pyepggrab and grabber loggers."""
        lformat = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        lhandler = logging.StreamHandler(stream=sys.stderr)
        lhandler.setFormatter(lformat)

        cls.create_logger("pyepggrab", lhandler)

        cls.create_logger(grabber_name(), lhandler)

    @classmethod
    def set_loglevel(cls, level: Union[int, str]) -> None:
        """Set loglevel in managed loggers."""
        for log in cls._managed_loggers:
            log.setLevel(level)

    @classmethod
    def finalize_loggers(cls) -> None:
        """Finalize managed loggers and replay the logs."""
        if not cls._finalized:
            cls._finalized = True
            for logger in cls._managed_loggers:
                logger.removeFilter(cls.logdelay_filter)
                for logrec in cls._delayedlogs.get(logger.name, []):
                    logger.handle(logrec)
                cls._delayedlogs.clear()
