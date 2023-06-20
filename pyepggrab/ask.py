"""Different convenience methods for asking user input.

For ...
    arbitrary input -> ask_input
    whole number -> ask_int
    boolean -> ask_boolean
    boolean with `all` and `none` -> ask_many_boolean
    choices -> ask_choice

For `ask_choice` based inputs, the ABBREVMAP contains some accepted abbreviations
"""

from typing import Optional

from .utils import eprint

ABREVMAP = {"y": "yes", "n": "no"}


def ask_input(prompt: str, default: Optional[str] = None) -> str:
    """Ask for input with and optional default choice if input is empty.

    Input is not validated in any ways.
    """
    if default:
        prompt += f" (default={default})"
    eprint(prompt)
    resp = input()
    if default and not resp:
        return default
    return resp


def ask_int(prompt: str, default: int = 1) -> int:
    """Ask for a whole number as input with a default of 1.

    Input is checked to contain only numbers.
    """
    while True:
        resp = ask_input(prompt, str(default))
        if resp.isnumeric():
            return int(resp)
        eprint("Invalid response! Please use whole numbers")


def ask_choice(prompt: str, *choices: str, default: Optional[str] = None) -> str:
    """Ask for a choice with an optional default.

    The input is checked to contain only one of the "choices".
    Some abbreviations accepted.
    """
    choice_str = ", ".join(choices)
    if default:
        choice_str += f" (default={default})"
    p_prompt = f"{prompt} [{choice_str}]"
    while True:
        resp = ask_input(p_prompt)
        if not resp and default:
            return default
        if resp in choices or resp == default:
            return resp
        if resp in ABREVMAP and ABREVMAP[resp] in choices:
            return ABREVMAP[resp]
        eprint("Invalid response!")


def ask_boolean(prompt: str, default_yes: bool = False) -> bool:
    """Ask for `yes`/`no` answer with a default of no.

    Some abbreviations accepted.
    """
    resp = ask_choice(prompt, "yes", "no", default="yes" if default_yes else "no")
    return resp == "yes"


def ask_many_boolean(prompt: str, default_yes: bool = False) -> str:
    """Ask for any of `yes`/`no`/`all`/`none` with a default of no.

    Some abbreviations accepted.
    """
    return ask_choice(
        prompt,
        "yes",
        "no",
        "all",
        "none",
        default="yes" if default_yes else "no",
    )
