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
from typing import List

from .. import placeholders
from ..exceptions import ConversionWarning
from ..model import Catalog, Entry
from .text import decode

MULTI_LOCALE = False

# Matches, in order of appearance, block comments, line comments and
# `"name" = "value";` entries.
_IOS_TOKEN_PATTERN = re.compile(
    r"/\*(?P<block>.*?)\*/"
    r"|//(?P<line>[^\n]*)"
    r'|"(?P<name>(?:[^"\\]|\\.)*)"\s*=\s*"(?P<value>(?:[^"\\]|\\.)*)"\s*;',
    re.DOTALL,
)

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
        )

    return "".join(f"{line}\n" for line in lines).encode("utf-8")


def _parse_entries(data: str, locale: str, with_comments: bool) -> List[Entry]:
    entries = []
    comment = None
    previous_end = None

    for match in _IOS_TOKEN_PATTERN.finditer(data):
        if match.group("name") is not None:
            entries.append(
                Entry(
                    _unescape_ios(match.group("name")),
                    {locale: _unescape_ios(match.group("value"))},
                    comment,
                )
            )
            comment = None
            previous_end = match.end()
            continue

        text = match.group("block") or match.group("line") or ""
        commented_entries = _parse_entries(text, locale, with_comments=False)

        if commented_entries:
            if with_comments:
                entries.extend(commented_entries)
            # A comment before commented out entries is about them
            comment = None
        elif previous_end is None or "\n" in data[previous_end : match.start()]:
            # Comments on the same line as the previous entry are not for the next one
            comment = text.strip() or None

    return entries


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
