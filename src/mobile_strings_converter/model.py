"""
Data model shared by every file type.

A `Catalog` holds the entries of one or more locales. Each `Entry` maps a locale to
its value.
"""

from dataclasses import dataclass, field, replace
from typing import Dict, Iterable, List, Optional, Tuple

# Locale of the strings that are not tied to any language, such as the ones in
# Android's `values` directory or iOS' `Base.lproj` directory
DEFAULT_LOCALE = "default"

Value = str


@dataclass
class Entry:
    """A named string with its value in each locale."""

    name: str
    values: Dict[str, Value] = field(default_factory=dict)
    # Note for translators, e.g. `/* Title of the main screen */`
    comment: Optional[str] = None
    # Android's `translatable="false"`
    translatable: bool = True


@dataclass
class Row:
    """An entry as written in a table."""

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
        """Creates a catalog from (name, value) pairs."""

        return cls.from_rows(Row(name, {locale: value}) for name, value in pairs)

    @classmethod
    def from_rows(cls, rows: Iterable[Row]) -> "Catalog":
        """Creates a catalog from table rows."""

        entries: Dict[str, Entry] = {}

        for row in rows:
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

    def to_rows(self) -> List[Row]:
        """Returns a row for each entry."""

        return [
            Row(entry.name, dict(entry.values), entry.comment) for entry in self.entries
        ]

    def to_pairs(self, locale: Optional[str] = None) -> List[Tuple[str, str]]:
        """
        Returns the (name, value) pairs of the locale, or of the first locale if none
        is given. Entries without a value in the locale have an empty value.
        """

        if locale is None:
            locale = next(iter(self.locales), DEFAULT_LOCALE)

        return [(row.name, row.values.get(locale, "")) for row in self.to_rows()]


def to_value(raw) -> Optional[Value]:
    """
    Converts a value read from a JSON or YAML file into a `Value`. Returns None for
    missing values.
    """

    if raw is None:
        return None
    return str(raw)
