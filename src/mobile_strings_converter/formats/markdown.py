import re

from ..model import Catalog
from . import table
from .text import decode

DELIMITER = "|"

# Splits a row on delimiters that are not escaped with a backslash
_SPLIT_PATTERN = re.compile(rf"(?<!\\){re.escape(DELIMITER)}")


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    """
    Reads the first table of a Markdown file. The first line of the table is the
    header, and the second one is the separator between the header and the rows.
    """

    lines = [line.strip() for line in decode(data).splitlines()]
    table_lines = [line for line in lines if line.startswith(DELIMITER)]
    if not table_lines:
        return Catalog()

    header, rows = _split_row(table_lines[0]), table_lines[2:]
    return table.from_table(header, [_split_row(row) for row in rows], locale)


def serialize(catalog: Catalog) -> bytes:
    header, *rows = table.to_table(catalog)

    lines = [_join_row(header), _join_row(["-----------"] * len(header))]
    lines += [_join_row([_escape(cell) for cell in row]) for row in rows]

    return "".join(f"{line}\n" for line in lines).encode("utf-8")


def _split_row(row: str) -> list[str]:
    return [_unescape(cell.strip()) for cell in _SPLIT_PATTERN.split(row)[1:-1]]


def _join_row(cells: list[str]) -> str:
    return f"{DELIMITER} {f' {DELIMITER} '.join(cells)} {DELIMITER}"


def _escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r\n", "<br>")
        .replace("\n", "<br>")
    )


def _unescape(value: str) -> str:
    return re.sub(r"\\(.)|<br>", lambda m: m.group(1) or "\n", value, flags=re.DOTALL)
