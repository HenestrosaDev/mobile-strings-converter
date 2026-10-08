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
- Empty translations of values that are not empty.
- Untranslated values, which are the same as the reference value. As some values are
  the same in several languages (e.g. `OK`), this check is optional.

Names defined more than once in a file are found by `find_duplicates`.

Each issue has a code (e.g. `missing`), listed in `ISSUE_CODES`.
"""

import re
from collections import Counter
from dataclasses import dataclass

from . import placeholders
from .model import DEFAULT_LOCALE, Catalog, Value

# Codes of the issues, with what they mean
ISSUE_CODES = {
    "missing": "a translatable string has no value in the locale",
    "obsolete": "a string has a value in the locale, but no reference value",
    "placeholders": "the placeholders differ from the ones of the reference value",
    "kind": "the value is a different kind (string, plural or array) or size than "
    "the reference value",
    "empty": "the value is empty, but the reference value is not",
    "untranslated": "the value is the same as the reference value",
    "duplicate": "the name is defined more than once in a file",
}

# Values without letters other than placeholders (e.g. `%d` or `—`) are the same in
# every language
_LETTER_PATTERN = re.compile(r"[^\W\d_]")


@dataclass(frozen=True)
class Issue:
    """A problem with the value of an entry in a locale."""

    locale: str
    name: str
    message: str
    # One of `ISSUE_CODES`
    code: str

    def __str__(self) -> str:
        return f"[{self.locale}] {self.name}: {self.message}"


def check(
    catalog: Catalog,
    reference_locale: str | None = None,
    untranslated: bool = False,
) -> list[Issue]:
    """
    Compares the values of each locale with the ones of the reference locale.

    :param catalog: Strings to check
    :type catalog: Catalog
    :param reference_locale: Locale to compare the others with. If None, it's the
        default locale, or the first locale if there is no default locale.
    :type reference_locale: str | None
    :param untranslated: True to report the values that are the same as the reference
        value, as long as they have letters
    :type untranslated: bool
    :return: The issues found, grouped by locale
    :rtype: list[Issue]
    """

    locales = catalog.locales
    if reference_locale is None:
        if not locales:
            return []
        reference_locale = DEFAULT_LOCALE if DEFAULT_LOCALE in locales else locales[0]
    elif reference_locale not in locales:
        raise ValueError(
            f"The reference locale {reference_locale} has no strings. The locales are: "
            f"{', '.join(locales) or 'none'}."
        )

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
                            "obsolete",
                        )
                    )
            elif value is None:
                if entry.translatable:
                    issues.append(
                        Issue(locale, entry.name, "missing translation", "missing")
                    )
            else:
                problem = _compare(
                    reference,
                    value,
                    reference_locale,
                    # Values that are not translated can be empty or the same
                    check_text=entry.translatable,
                    untranslated=untranslated,
                )
                if problem:
                    code, message = problem
                    issues.append(Issue(locale, entry.name, message, code))

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
                Issue(
                    locale,
                    entry.name,
                    f"defined {counts[entry.name]} times",
                    "duplicate",
                )
            )
            # Report each name once
            counts[entry.name] = 0

    return issues


def _compare(
    reference: Value,
    value: Value,
    reference_locale: str,
    check_text: bool,
    untranslated: bool,
) -> tuple[str, str] | None:
    """
    Returns the code and message of the problem of the value, if any. Empty and
    untranslated values are only checked if `check_text` is True.
    """

    reference_kind, kind = _kind(reference), _kind(value)
    if reference_kind != kind:
        return (
            "kind",
            f"is a {kind}, but the {reference_locale} value is a {reference_kind}",
        )

    if (
        isinstance(reference, list)
        and isinstance(value, list)
        and len(reference) != len(value)
    ):
        return (
            "kind",
            f"has {len(value)} items, but the {reference_locale} value has "
            f"{len(reference)}",
        )

    # Checked before the placeholders, as an empty value has none
    if check_text:
        problem = _compare_text(reference, value, reference_locale, untranslated)
        if problem:
            return problem

    if isinstance(reference, list) and isinstance(value, list):
        for i, (reference_item, item) in enumerate(zip(reference, value, strict=True)):
            problem = _compare_placeholders([reference_item], [item], reference_locale)
            if problem:
                return problem[0], f"item {i} {problem[1]}"
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
) -> tuple[str, str] | None:
    expected = _signature(references)
    actual = _signature(values)
    if expected == actual:
        return None

    return (
        "placeholders",
        f"has the placeholders {_format(actual)}, but the {reference_locale} value has "
        f"{_format(expected)}",
    )


def _compare_text(
    reference: Value, value: Value, reference_locale: str, untranslated: bool
) -> tuple[str, str] | None:
    """
    Returns the code and message of an empty or untranslated value, if it is one. Both
    values must be of the same kind.
    """

    reference_texts, texts = _texts(reference), _texts(value)

    if any(reference_texts) and not any(texts):
        return "empty", f"is empty, but the {reference_locale} value is not"

    if (
        untranslated
        and reference == value
        and any(_LETTER_PATTERN.search(placeholders.remove(text)) for text in texts)
    ):
        return "untranslated", f"is the same as the {reference_locale} value"

    return None


def _texts(value: Value) -> list[str]:
    if isinstance(value, dict):
        return list(value.values())
    if isinstance(value, list):
        return value
    return [value]


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
