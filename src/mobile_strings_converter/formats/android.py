"""
Android string resources (`strings.xml`): `<string>`, `<plurals>` and `<string-array>`.

A comment right before a resource is read as its comment for translators, unless the
comment holds commented out resources, which are read as entries if `with_comments`
is True. iOS placeholders (e.g. `%@`) are converted to Android ones (e.g. `%s`) when
writing.
"""

import html
import re
import warnings

from lxml import etree

from .. import placeholders
from ..exceptions import ConversionWarning
from ..model import Catalog, Entry, Value

MULTI_LOCALE = False

_ANDROID_ESCAPES = {"n": "\n", "t": "\t"}

# Matches, in order of appearance, escape sequences, double quotes, whitespace and any
# other text
_ANDROID_TOKEN_PATTERN = re.compile(
    r'\\(?P<escaped>u[0-9a-fA-F]{4}|.)|(?P<quote>")|(?P<space>\s+)|[^\\"\s]+|\\',
    re.DOTALL,
)


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    try:
        root = etree.fromstring(data.strip())
    except etree.XMLSyntaxError:
        raise ValueError("The file provided is not a valid .xml file.") from None

    entries = []

    if root.tag == "resources":
        comment = None

        for node in root:
            if node.tag is etree.Comment:
                commented_entries = _parse_commented_resources(node.text or "", locale)
                if commented_entries:
                    if with_comments:
                        entries.extend(commented_entries)
                    # A comment before commented out resources is about them
                    comment = None
                elif not _is_trailing(node):
                    comment = (node.text or "").strip() or None
                continue

            entry = _parse_resource(node, locale)
            if entry is not None:
                entry.comment = comment
                entries.append(entry)
            comment = None

    if not entries:
        raise ValueError("The file provided is not a valid .xml file.")

    return Catalog(entries)


def serialize(catalog: Catalog) -> bytes:
    if catalog.is_multi_locale:
        raise ValueError(
            "An Android .xml file can only hold one locale, but the strings have "
            f"{len(catalog.locales)}: {', '.join(catalog.locales)}."
        )

    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]

    for entry in catalog.entries:
        value = next(iter(entry.values.values()), "")
        name = html.escape(entry.name)
        attributes = f'name="{name}"'
        if not entry.translatable:
            attributes += ' translatable="false"'

        if entry.comment:
            # `--` is not allowed inside XML comments
            comment = re.sub(r"-(?=-)", "- ", entry.comment)
            lines.append(f"\t<!-- {comment} -->")

        if isinstance(value, dict):
            lines.append(f"\t<plurals {attributes}>")
            for quantity, item in value.items():
                lines.append(
                    f'\t\t<item quantity="{html.escape(quantity)}">'
                    f"{_to_android_value(item)}</item>"
                )
            lines.append("\t</plurals>")
        elif isinstance(value, list):
            lines.append(f"\t<string-array {attributes}>")
            for item in value:
                lines.append(f"\t\t<item>{_to_android_value(item)}</item>")
            lines.append("\t</string-array>")
        else:
            lines.append(f"\t<string {attributes}>{_to_android_value(value)}</string>")

    lines.append("</resources>")

    return "".join(f"{line}\n" for line in lines).encode("utf-8")


def _parse_resource(node: etree._Element, locale: str) -> Entry | None:
    name = node.get("name")
    if name is None:
        return None

    value: Value
    if node.tag == "string":
        value = _get_android_value(node)
    elif node.tag == "plurals":
        value = {
            quantity: _get_android_value(item)
            for item in node
            if item.tag == "item" and (quantity := item.get("quantity")) is not None
        }
    elif node.tag == "string-array":
        value = [_get_android_value(item) for item in node if item.tag == "item"]
    else:
        if node.tag in ("integer-array", "array"):
            warnings.warn(
                f'Skipped the <{node.tag} name="{name}"> resource because it is not '
                f"supported.",
                ConversionWarning,
                stacklevel=2,
            )
        return None

    return Entry(
        name,
        {locale: value},
        translatable=node.get("translatable", "true").lower() != "false",
    )


def _parse_commented_resources(comment: str, locale: str) -> list[Entry]:
    try:
        root = etree.fromstring(f"<resources>{comment}</resources>")
    except etree.XMLSyntaxError:
        # The comment is not a commented out resource
        return []

    entries = [
        _parse_resource(node, locale) for node in root if isinstance(node.tag, str)
    ]
    return [entry for entry in entries if entry is not None]


def _is_trailing(comment: etree._Element) -> bool:
    """Returns True if the comment is on the same line as the previous resource."""

    previous = comment.getprevious()
    if previous is None:
        return False

    return "\n" not in (previous.tail or "")


def _get_android_value(element: etree._Element) -> str:
    """
    Returns the value of a `<string>` or `<item>` element. Values with inline markup
    (e.g. `<b>bold</b>`) are returned verbatim, as they appear in the file. Otherwise,
    the XML entities and Android escape sequences are decoded.
    """

    if len(element):
        inner_xml = element.text and html.escape(element.text, quote=False) or ""
        for child in element:
            inner_xml += etree.tostring(child, encoding="unicode", with_tail=True)
        return inner_xml

    return _unescape_android(element.text or "")


def _unescape_android(value: str) -> str:
    """
    Decodes a value as Android does: whitespace outside double quotes is collapsed into
    a single space and trimmed, unescaped double quotes are removed, and escape
    sequences (e.g. `\\n` or `\\'`) are decoded.
    """

    # Text and whether it's whitespace that can be collapsed and trimmed
    parts: list[tuple[str, bool]] = []
    quoted = False

    for match in _ANDROID_TOKEN_PATTERN.finditer(value):
        if match.group("escaped") is not None:
            escaped = match.group("escaped")
            if escaped[0] == "u" and len(escaped) > 1:
                text = chr(int(escaped[1:], 16))
            else:
                text = _ANDROID_ESCAPES.get(escaped, escaped)
            parts.append((text, False))
        elif match.group("quote") is not None:
            quoted = not quoted
        elif match.group("space") is not None and not quoted:
            # Whitespace split by quotes (e.g. `a "" b`) is collapsed as well
            if not (parts and parts[-1][1]):
                parts.append((" ", True))
        else:
            parts.append((match.group(0), False))

    while parts and parts[0][1]:
        parts.pop(0)
    while parts and parts[-1][1]:
        parts.pop()

    return "".join(text for text, _ in parts)


def _escape_android(value: str) -> str:
    value = (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )

    # `@` and `?` at the start of a value are resource references
    if value.startswith(("@", "?")):
        value = "\\" + value

    # Android collapses and trims whitespace outside double quotes
    if value != value.strip(" ") or "  " in value:
        value = f'"{value}"'

    return html.escape(value, quote=False)


def _to_android_value(value: str) -> str:
    """
    Returns the value ready to be written inside a `<string>` element, with iOS
    placeholders converted to Android ones. Values with well-formed inline markup (as
    returned by `_get_android_value`) are written verbatim.
    """

    value = placeholders.to_android(value)

    if "<" in value:
        try:
            if len(etree.fromstring(f"<string>{value}</string>")):
                return value
        except etree.XMLSyntaxError:
            pass

    return _escape_android(value)
