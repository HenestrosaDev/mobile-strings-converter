import html
from html.parser import HTMLParser

from ..model import Catalog
from . import table
from .text import decode


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    """
    Reads the rows of the HTML tables. The first row of `<th>` cells is the header. If
    there is none, the table is assumed to have a name and a value column.
    """

    parser = _HTMLTableParser()
    parser.feed(decode(data))
    parser.close()

    return table.from_table(parser.header, parser.rows, locale)


def serialize(catalog: Catalog) -> bytes:
    header, *rows = table.to_table(catalog)

    lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '\t<meta charset="UTF-8">',
        "</head>",
        "<body>",
        "<table>",
        "\t<thead>",
        "\t\t<tr>",
        *[f"\t\t\t<th>{_escape(cell)}</th>" for cell in header],
        "\t\t</tr>",
        "\t</thead>",
        "\t<tbody>",
    ]
    for row in rows:
        lines.append("\t\t<tr>")
        lines += [f"\t\t\t<td>{_escape(cell)}</td>" for cell in row]
        lines.append("\t\t</tr>")
    lines += ["\t</tbody>", "</table>", "</body>", "</html>"]

    return "".join(f"{line}\n" for line in lines).encode("utf-8")


def _escape(value: str) -> str:
    return html.escape(value, quote=False)


class _HTMLTableParser(HTMLParser):
    """Collects the text of the `<th>` header cells and `<td>` cells of every row."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.header: list[str] | None = None
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._row_is_header = False
        self._cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
            self._row_is_header = False
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []
            self._row_is_header = self._row_is_header or tag == "th"

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._row is not None and self._cell is not None:
            self._row.append("".join(self._cell))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if not self._row_is_header:
                self.rows.append(self._row)
            elif self.header is None:
                self.header = self._row
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)
