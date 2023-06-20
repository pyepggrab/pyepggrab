"""Utilities that useful globally in many places.

Also includes functions that have been back ported to maintain compatibility
with older python versions (this should be noted in the function)
"""

import sys
from pathlib import Path


def script_path() -> str:
    """Return the path of the script that started it."""
    return sys.argv[0]


def script_name() -> str:
    """Return the name of the script that started it."""
    return Path(script_path()).stem


def remove_prefix(base: str, pfx: str) -> str:
    """Remove `pfx` from `s` if it starts with it."""
    # `str.removeprefix()` available in >= 3.9"
    # Remove if < 3.9 unsupported
    if base.startswith(pfx):
        return base[len(pfx) :]
    return base


def remove_suffix(base: str, sfx: str) -> str:
    """Remove `sfx` from `s` if it ends with it."""
    # `str.removesuffix()` available in >= 3.9"
    # Remove if < 3.9 unsupported
    if base.endswith(sfx):
        return base[: len(base) - len(sfx)]
    return base


def grabber_name() -> str:
    """Return the name of the grabber (or the script that used to start it)."""
    return script_name()


def eprint(*args, **kwargs) -> None:
    """Print to the stderr (standard error output)."""
    print(*args, file=sys.stderr, **kwargs)
