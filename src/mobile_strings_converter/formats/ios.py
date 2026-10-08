"""
iOS strings files (`Localizable.strings`).

A comment right before an entry is read as its comment for translators, unless the
comment holds commented out entries, which are read as entries if `with_comments` is
True. Plurals and arrays can't be written to `.strings` files, so they are skipped
(see `stringsdict` for plurals). Android placeholders (e.g. `%s`) are converted to iOS
ones (e.g. `%@`) when writing.
"""

import re
import warnings

from .. import placeholders
from ..exceptions import ConversionWarning
from ..model import Catalog, Entry
from .text import decode

MULTI_LOCALE = False

# Names and values can be written without quotes if they only have these characters,
# e.g. `hello_world = "Hello, World!";`
_IOS_UNQUOTED = r"[A-Za-z0-9_$+/:.-]+"


def _token_pattern(unquoted: bool) -> re.Pattern[str]:
    """
    Matches, in order of appearance, block comments, line comments and
    `"name" = "value";` entries, optionally with unquoted names and values.
    """

    def string(group: str) -> str:
        quoted = rf'"(?P<{group}>(?:[^"\\]|\\.)*)"'
        return (
            f"(?:{quoted}|(?P<{group}_unquoted>{_IOS_UNQUOTED}))"
            if unquoted
            else quoted
        )

    return re.compile(
        r"/\*(?P<block>.*?)\*/"
        r"|//(?P<line>[^\n]*)"
        rf"|{string('name')}\s*=\s*{string('value')}\s*;",
        re.DOTALL,
    )


_IOS_TOKEN_PATTERN = _token_pattern(unquoted=True)

# Comments only count as commented out entries if their names and values are quoted,
# so that comments for translators such as `/* Shown when count = 0; */` are not
# mistaken for entries
_IOS_COMMENTED_TOKEN_PATTERN = _token_pattern(unquoted=False)

_IOS_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "0": "\0"}


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    entries = _parse_entries(decode(data), locale, with_comments)

    if not entries:
        raise ValueError("The file provided is not a valid .strings file.")

    return Catalog(entries)


def serialize(catalog: Catalog) -> bytes:
    if catalog.is_multi_locale:
        raise ValueError(
            "An iOS .strings file can only hold one locale, but the strings have "
            f"{len(catalog.locales)}: {', '.join(catalog.locales)}."
        )

    lines = []
    skipped = []

    for entry in catalog.entries:
        value = next(iter(entry.values.values()), "")
        if not isinstance(value, str):
            skipped.append(entry.name)
            continue

        if entry.comment:
            lines.append(f"/* {entry.comment.replace('*/', '* /')} */")
        value = placeholders.to_ios(value)
        lines.append(f'"{_escape_ios(entry.name)}" = "{_escape_ios(value)}";')

    if skipped:
        warnings.warn(
            f"Skipped {len(skipped)} plural(s)/array(s) because .strings files can't "
            f"hold them: {', '.join(skipped)}. Plurals can be written to .stringsdict "
            f"or .xcstrings files.",
            ConversionWarning,
            stacklevel=2,
        )

    return "".join(f"{line}\n" for line in lines).encode("utf-8")


def _parse_entries(
    data: str,
    locale: str,
    with_comments: bool,
    pattern: re.Pattern[str] = _IOS_TOKEN_PATTERN,
) -> list[Entry]:
    entries = []
    comment = None
    previous_end = None

    for match in pattern.finditer(data):
        groups = match.groupdict()
        name = _string(groups, "name")
        if name is not None:
            entries.append(
                Entry(name, {locale: _string(groups, "value") or ""}, comment)
            )
            comment = None
            previous_end = match.end()
            continue

        text = match.group("block") or match.group("line") or ""
        commented_entries = _parse_entries(
            text, locale, with_comments=False, pattern=_IOS_COMMENTED_TOKEN_PATTERN
        )

        if commented_entries:
            if with_comments:
                entries.extend(commented_entries)
            # A comment before commented out entries is about them
            comment = None
        elif previous_end is None or "\n" in data[previous_end : match.start()]:
            # Comments on the same line as the previous entry are not for the next one
            comment = text.strip() or None

    return entries


def _string(groups: dict[str, str | None], group: str) -> str | None:
    """Returns the unescaped string of a quoted or unquoted group of a match."""

    quoted = groups[group]
    if quoted is not None:
        return _unescape_ios(quoted)
    return groups.get(f"{group}_unquoted")


def _unescape_ios(value: str) -> str:
    def replace(match):
        escaped = match.group(1)
        if escaped[0] in "uU" and len(escaped) > 1:
            return chr(int(escaped[1:], 16))
        return _IOS_ESCAPES.get(escaped, escaped)

    return re.sub(r"\\([uU][0-9a-fA-F]{4}|.)", replace, value, flags=re.DOTALL)


def _escape_ios(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )
