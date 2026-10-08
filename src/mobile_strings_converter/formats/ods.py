import io

import ezodf
from ezodf import observer

from ..model import Catalog
from . import table


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    """Reads the first sheet. See `table` for the supported columns."""

    sheet = ezodf.opendoc(io.BytesIO(data)).sheets[0]
    rows = [[cell.value for cell in row] for row in sheet.rows()]

    return table.from_table(rows[0] if rows else None, rows[1:], locale)


def serialize(catalog: Catalog) -> bytes:
    rows = table.to_table(catalog)

    doc = ezodf.newdoc(doctype="ods")
    sheet = ezodf.Sheet("Sheet1", size=(len(rows), len(rows[0])))
    doc.sheets += sheet

    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            sheet[i, j].set_value(value)

    # `doc.save()` does this before writing the file
    observer.broadcast("prepare_saving", root=doc.body.get_xmlroot())
    return doc.tobytes()
