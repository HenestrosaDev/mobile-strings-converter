"""
Conversion between catalogs and tables, shared by every tabular file type.

The first column holds the names. A single-locale catalog has a `VALUE` column, and a
multi-locale catalog has one column per locale, named after it (`VALUE` for the
default locale). A `COMMENT` column is added if any entry has a comment.
"""

from collections.abc import Sequence

from ..model import DEFAULT_LOCALE, Catalog, Row

NAME_HEADER = "NAME"
VALUE_HEADER = "VALUE"
COMMENT_HEADER = "COMMENT"


def to_table(catalog: Catalog, lowercase_headers: bool = False) -> list[list[str]]:
    """
    Returns the header followed by a row of strings for each flattened entry.

    :param catalog: Strings to write
    :type catalog: Catalog
    :param lowercase_headers: True to write `name`, `value` and `comment` in lowercase
    :type lowercase_headers: bool
    :return: The header and the rows of the table
    :rtype: list[list[str]]
    """

    locales = catalog.locales or [DEFAULT_LOCALE]
    rows = catalog.to_rows()
    with_comments = any(row.comment for row in rows)

    def label(header: str) -> str:
        return header.lower() if lowercase_headers else header

    header = [label(NAME_HEADER)]
    for locale in locales:
        is_value_column = len(locales) == 1 or locale == DEFAULT_LOCALE
        header.append(label(VALUE_HEADER) if is_value_column else locale)
    if with_comments:
        header.append(label(COMMENT_HEADER))

    table = [header]
    for row in rows:
        cells = [row.name] + [row.values.get(locale, "") for locale in locales]
        if with_comments:
            cells.append(row.comment or "")
        table.append(cells)

    return table


def from_table(
    header: Sequence | None, rows: Sequence[Sequence], locale: str
) -> Catalog:
    """
    Creates a catalog from a table. Rows without a name are skipped, as well as columns
    without a header. Empty cells mean that the entry has no value in that locale.

    :param header: Cells of the header row. If None, the table is assumed to have a
        name and a value column.
    :type header: Sequence | None
    :param rows: Cells of each row, without the header
    :type rows: Sequence[Sequence]
    :param locale: Locale of the `VALUE` column
    :type locale: str
    :return: The strings of the table
    :rtype: Catalog
    """

    if header is None:
        header = [NAME_HEADER, VALUE_HEADER]

    # Index of the column of each locale and of the comments
    columns = {}
    comment_column = None
    for i, cell in enumerate(header[1:], start=1):
        label = _to_str(cell).strip()
        if label.upper() == VALUE_HEADER:
            columns[locale] = i
        elif label.upper() == COMMENT_HEADER:
            comment_column = i
        elif label:
            columns[label] = i

    def cell_at(row: Sequence, i: int | None) -> str:
        return _to_str(row[i]) if i is not None and i < len(row) else ""

    catalog_rows = []
    for row in rows:
        name = cell_at(row, 0)
        if name.strip() == "":
            continue

        values = {
            column_locale: cell_at(row, i)
            for column_locale, i in columns.items()
            if cell_at(row, i) != ""
        }
        catalog_rows.append(Row(name, values, cell_at(row, comment_column) or None))

    return Catalog.from_rows(catalog_rows)


def _to_str(cell: object) -> str:
    return "" if cell is None else str(cell)
