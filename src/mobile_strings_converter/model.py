"""
Data model shared by every file type.

A `Catalog` holds the entries of one or more locales. Each `Entry` maps a locale to
its value, which is either a string, a plural (a dict of quantity -> string) or an
array (a list of strings).
"""

import re
from dataclasses import dataclass, field, replace
from typing import Dict, Iterable, List, Optional, Tuple, Union

# Locale of the strings that are not tied to any language, such as the ones in
# Android's `values` directory or iOS' `Base.lproj` directory
DEFAULT_LOCALE = "default"

# CLDR plural categories, in the order they are written
PLURAL_QUANTITIES = ("zero", "one", "two", "few", "many", "other")

Value = Union[str, Dict[str, str], List[str]]

# Matches the names of flattened plurals and arrays, e.g. `songs[one]` or `planets[0]`
_FLAT_NAME_PATTERN = re.compile(
    r"^(?P<name>.*\S)\[(?P<key>" + "|".join(PLURAL_QUANTITIES) + r"|\d+)\]$"
)


@dataclass
class Entry:
    """A named string, plural or array with its value in each locale."""

    name: str
    values: Dict[str, Value] = field(default_factory=dict)
    # Note for translators, e.g. `/* Title of the main screen */`
    comment: Optional[str] = None
    # Android's `translatable="false"`
    translatable: bool = True


@dataclass
class Row:
    """An entry flattened into strings, as written in a table."""

    name: str
    values: Dict[str, str] = field(default_factory=dict)
    comment: Optional[str] = None


@dataclass
class Catalog:
    """The strings of one or more locales."""

    entries: List[Entry] = field(default_factory=list)

    @property
    def locales(self) -> List[str]:
        """Locales with at least one value, in order of appearance."""

        locales = {}
        for entry in self.entries:
            locales.update(dict.fromkeys(entry.values))
        return list(locales)

    @property
    def is_multi_locale(self) -> bool:
        return len(self.locales) > 1

    @classmethod
    def from_pairs(
        cls, pairs: Iterable[Tuple[str, str]], locale: str = DEFAULT_LOCALE
    ) -> "Catalog":
        """
        Creates a catalog from (name, value) pairs. Flattened plurals and arrays (e.g.
        `songs[one]` or `planets[0]`) are grouped back into a single entry.
        """

        return cls.from_rows(Row(name, {locale: value}) for name, value in pairs)

    @classmethod
    def from_rows(cls, rows: Iterable[Row]) -> "Catalog":
        """
        Creates a catalog from table rows. Flattened plurals and arrays (e.g.
        `songs[one]` or `planets[0]`) are grouped back into a single entry.
        """

        entries: Dict[str, Entry] = {}

        for row in rows:
            match = _FLAT_NAME_PATTERN.match(row.name)
            entry = match and entries.get(match.group("name"))

            if match and (entry is None or _is_container(entry, match.group("key"))):
                name, key = match.groups()
                if entry is None:
                    entry = entries[name] = Entry(name)

                for locale, value in row.values.items():
                    if key.isdigit():
                        array = entry.values.setdefault(locale, [])
                        array.extend([""] * (int(key) + 1 - len(array)))
                        array[int(key)] = value
                    else:
                        entry.values.setdefault(locale, {})[key] = value
            else:
                # Later rows with the same name override the previous ones
                entry = entries.setdefault(row.name, Entry(row.name))
                entry.values.update(row.values)

            entry.comment = entry.comment or row.comment

        return cls(list(entries.values()))

    @classmethod
    def merge(cls, catalogs: Iterable["Catalog"]) -> "Catalog":
        """
        Combines the catalogs of different locales into one. Entries are matched by
        name, and values of later catalogs override the ones of earlier catalogs.
        """

        entries: Dict[str, Entry] = {}

        for catalog in catalogs:
            for entry in catalog.entries:
                merged = entries.setdefault(entry.name, Entry(entry.name))
                merged.values.update(entry.values)
                merged.comment = merged.comment or entry.comment
                merged.translatable = merged.translatable and entry.translatable

        return cls(list(entries.values()))

    def for_locale(self, locale: str) -> "Catalog":
        """Returns a catalog with the entries that have a value in the locale."""

        return Catalog(
            [
                replace(entry, values={locale: entry.values[locale]})
                for entry in self.entries
                if locale in entry.values
            ]
        )

    def split(self) -> Dict[str, "Catalog"]:
        """Returns a single-locale catalog for each locale."""

        return {locale: self.for_locale(locale) for locale in self.locales}

    def to_rows(self) -> List[Row]:
        """
        Flattens the entries into rows of strings. Plurals and arrays are written as one
        row per item, named `name[quantity]` or `name[index]` respectively.
        """

        rows = []

        for entry in self.entries:
            values = list(entry.values.values())

            if values and isinstance(values[0], dict):
                keys = _ordered_keys(v for v in values if isinstance(v, dict))
                entry_rows = [
                    Row(
                        f"{entry.name}[{key}]",
                        {
                            locale: value[key]
                            for locale, value in entry.values.items()
                            if isinstance(value, dict) and key in value
                        },
                    )
                    for key in keys
                ]
            elif values and isinstance(values[0], list):
                size = max(len(v) for v in values if isinstance(v, list))
                entry_rows = [
                    Row(
                        f"{entry.name}[{i}]",
                        {
                            locale: value[i]
                            for locale, value in entry.values.items()
                            if isinstance(value, list) and i < len(value)
                        },
                    )
                    for i in range(size)
                ]
            else:
                entry_rows = [
                    Row(
                        entry.name,
                        {
                            locale: value
                            for locale, value in entry.values.items()
                            if isinstance(value, str)
                        },
                    )
                ]

            if entry_rows:
                entry_rows[0].comment = entry.comment
            rows.extend(entry_rows)

        return rows

    def to_pairs(self, locale: Optional[str] = None) -> List[Tuple[str, str]]:
        """
        Returns the (name, value) pairs of the locale, or of the first locale if none
        is given. Plurals and arrays are flattened (see `to_rows`), and entries without
        a value in the locale have an empty value.
        """

        if locale is None:
            locale = next(iter(self.locales), DEFAULT_LOCALE)

        return [(row.name, row.values.get(locale, "")) for row in self.to_rows()]


def to_value(raw) -> Optional[Value]:
    """
    Converts a value read from a JSON or YAML file into a `Value`. Dicts are plurals,
    lists are arrays and any other value is converted into a string. Returns None for
    missing values.
    """

    if raw is None:
        return None
    if isinstance(raw, dict):
        return {str(key): _to_str(value) for key, value in raw.items()}
    if isinstance(raw, list):
        return [_to_str(value) for value in raw]
    return str(raw)


def _to_str(raw) -> str:
    return "" if raw is None else str(raw)


def _is_container(entry: Entry, key: str) -> bool:
    """Returns True if the entry is a plural or array that can hold the key."""

    container_type = list if key.isdigit() else dict
    return all(isinstance(value, container_type) for value in entry.values.values())


def _ordered_keys(plurals: Iterable[Dict[str, str]]) -> List[str]:
    keys = {}
    for plural in plurals:
        keys.update(dict.fromkeys(plural))

    known = [quantity for quantity in PLURAL_QUANTITIES if quantity in keys]
    return known + [key for key in keys if key not in PLURAL_QUANTITIES]
