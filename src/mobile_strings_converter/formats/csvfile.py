import csv
import io

from ..model import Catalog
from . import table
from .text import decode


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    """
    Reads a CSV file with a header row. See `table` for the supported columns.
    """

    reader = csv.reader(io.StringIO(decode(data), newline=""))
    header = next(reader, None)
    return table.from_table(header, list(reader), locale)


def serialize(catalog: Catalog) -> bytes:
    output = io.StringIO(newline="")
    csv.writer(output).writerows(table.to_table(catalog, lowercase_headers=True))
    return output.getvalue().encode("utf-8")
