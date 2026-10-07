"""
JSON files hold a list of records, one per entry:

- Single-locale catalogs: `{"name": ..., "value": ...}`
- Multi-locale catalogs: `{"name": ..., "value": ..., "es": ..., "fr": ...}`, where
  `value` holds the default locale.

Entries with a comment have a `comment` field. A single object mapping names to values
can be read as well.
"""

import json

from ..model import DEFAULT_LOCALE, Catalog, Entry, to_value
from .text import decode

NAME_KEY = "name"
VALUE_KEY = "value"
COMMENT_KEY = "comment"


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    json_data = json.loads(decode(data))

    if isinstance(json_data, dict):
        return Catalog(
            [
                Entry(str(name), _values({locale: to_value(value)}))
                for name, value in json_data.items()
            ]
        )

    if not isinstance(json_data, list):
        raise ValueError("The file provided is not a valid .json file.")

    entries = []
    for record in json_data:
        if not isinstance(record, dict) or record.get(NAME_KEY) is None:
            continue

        values = {}
        for key, value in record.items():
            if key == VALUE_KEY:
                values[locale] = to_value(value)
            elif key not in (NAME_KEY, COMMENT_KEY):
                values[key] = to_value(value)

        comment = record.get(COMMENT_KEY)
        entries.append(
            Entry(str(record[NAME_KEY]), _values(values), comment and str(comment))
        )

    return Catalog(entries)


def serialize(catalog: Catalog) -> bytes:
    return (dumps(catalog, indent=2) + "\n").encode("utf-8")


def dumps(catalog: Catalog, indent=None) -> str:
    locales = catalog.locales or [DEFAULT_LOCALE]
    is_single_locale = len(locales) == 1

    records = []
    for entry in catalog.entries:
        record = {NAME_KEY: entry.name}

        if is_single_locale:
            record[VALUE_KEY] = entry.values.get(locales[0], "")
        else:
            for locale, value in entry.values.items():
                record[VALUE_KEY if locale == DEFAULT_LOCALE else locale] = value

        if entry.comment:
            record[COMMENT_KEY] = entry.comment

        records.append(record)

    return json.dumps(records, ensure_ascii=False, indent=indent)


def _values(values):
    """Removes the missing values."""
    return {locale: value for locale, value in values.items() if value is not None}
