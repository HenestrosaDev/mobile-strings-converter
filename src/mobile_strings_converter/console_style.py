"""
Colors of the messages printed by the command. Colors are only used in terminals, so
redirected or piped output has no escape codes. Set `NO_COLOR` to disable them, or
`FORCE_COLOR` to use them anyway (see https://no-color.org and https://force-color.org).
"""

import os
from typing import TextIO


class ConsoleStyle:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


def colorize(text: str, color: str, stream: TextIO) -> str:
    """
    Returns the text in the color if the stream supports colors, or the text as is
    otherwise.

    :param text: Text to print
    :type text: str
    :param color: One of the colors of `ConsoleStyle`
    :type color: str
    :param stream: Stream the text is printed to
    :type stream: TextIO
    :return: The text, in the color if supported
    :rtype: str
    """

    return f"{color}{text}{ConsoleStyle.END}" if supports_color(stream) else text


def supports_color(stream: TextIO) -> bool:
    """Returns True if the text printed to the stream can have colors."""

    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if os.environ.get("TERM") == "dumb":
        return False

    isatty = getattr(stream, "isatty", None)
    return bool(isatty and isatty())
