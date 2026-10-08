"""
Checks of the translations of a catalog, which compare each locale with a reference
locale (the default locale, if there is one):

- Missing translations: translatable entries with a reference value but no value in the
  locale.
- Obsolete translations: entries with a value in the locale but no reference value.
- Placeholders that differ from the ones of the reference value. Positions, Android and
  iOS conversions (e.g. `%s` and `%@`) and the order of positional placeholders are
  taken into account (see `placeholders.signature`).
- Values of a different kind (string, plural or array) than the reference value.

Names defined more than once in a file are found by `find_duplicates`.
"""

from collections import Counter
from dataclasses import dataclass

from . import placeholders
from .model import DEFAULT_LOCALE, Catalog, Value


@dataclass(frozen=True)
class Issue:
    """A problem with the value of an entry in a locale."""

    locale: str
    name: str
    message: str

    def __str__(self) -> str:
        return f"[{self.locale}] {self.name}: {self.message}"


def check(catalog: Catalog, reference_locale: str | None = None) -> list[Issue]:
    """
    Compares the values of each locale with the ones of the reference locale.

    :param catalog: Strings to check
    :type catalog: Catalog
    :param reference_locale: Locale to compare the others with. If None, it's the
        default locale, or the first locale if there is no default locale.
    :type reference_locale: str | None
    :return: The issues found, grouped by locale
    :rtype: list[Issue]
    """

    locales = catalog.locales
    if reference_locale is None:
        if not locales:
            return []
        reference_locale = DEFAULT_LOCALE if DEFAULT_LOCALE in locales else locales[0]

    issues = []

    for locale in locales:
        if locale == reference_locale:
            continue

        for entry in catalog.entries:
            reference = entry.values.get(reference_locale)
            value = entry.values.get(locale)

            if reference is None:
                if value is not None:
                    issues.append(
                        Issue(
                            locale,
                            entry.name,
                            f"obsolete translation, as there is no "
                            f"{reference_locale} value",
                        )
                    )
            elif value is None:
                if entry.translatable:
                    issues.append(Issue(locale, entry.name, "missing translation"))
            else:
                message = _compare(reference, value, reference_locale)
                if message:
                    issues.append(Issue(locale, entry.name, message))

    return issues


def find_duplicates(catalog: Catalog) -> list[Issue]:
    """
    Returns an issue for each name defined more than once, such as a `<string>` written
    twice in a `strings.xml` file. Only the last definition is kept when converting
    several files at once.

    :param catalog: Strings of a file, as read by `parse` or `load`
    :type catalog: Catalog
    :return: The issues found
    :rtype: list[Issue]
    """

    counts = Counter(entry.name for entry in catalog.entries)
    issues = []

    for entry in catalog.entries:
        if counts[entry.name] > 1:
            locale = next(iter(entry.values), DEFAULT_LOCALE)
            issues.append(
                Issue(locale, entry.name, f"defined {counts[entry.name]} times")
            )
            # Report each name once
            counts[entry.name] = 0

    return issues


def _compare(reference: Value, value: Value, reference_locale: str) -> str | None:
    """Returns the problem of the value compared to the reference, if any."""

    reference_kind, kind = _kind(reference), _kind(value)
    if reference_kind != kind:
        return f"is a {kind}, but the {reference_locale} value is a {reference_kind}"

    if isinstance(reference, list) and isinstance(value, list):
        if len(reference) != len(value):
            return (
                f"has {len(value)} items, but the {reference_locale} value has "
                f"{len(reference)}"
            )
        for i, (reference_item, item) in enumerate(zip(reference, value, strict=True)):
            message = _compare_placeholders([reference_item], [item], reference_locale)
            if message:
                return f"item {i} {message}"
        return None

    if isinstance(reference, dict) and isinstance(value, dict):
        # Languages can leave the number out of some quantities (e.g. "One song"), so
        # the placeholders of every quantity are compared together
        return _compare_placeholders(
            list(reference.values()), list(value.values()), reference_locale
        )

    assert isinstance(reference, str) and isinstance(value, str)
    return _compare_placeholders([reference], [value], reference_locale)


def _compare_placeholders(
    references: list[str], values: list[str], reference_locale: str
) -> str | None:
    expected = _signature(references)
    actual = _signature(values)
    if expected == actual:
        return None

    return (
        f"has the placeholders {_format(actual)}, but the {reference_locale} value has "
        f"{_format(expected)}"
    )


def _signature(values: list[str]) -> list[tuple[int, str]]:
    return sorted({item for value in values for item in placeholders.signature(value)})


def _format(signature: list[tuple[int, str]]) -> str:
    if not signature:
        return "none"
    return " ".join(f"%{position}${conversion}" for position, conversion in signature)


def _kind(value: Value) -> str:
    if isinstance(value, dict):
        return "plural"
    if isinstance(value, list):
        return "array"
    return "string"
