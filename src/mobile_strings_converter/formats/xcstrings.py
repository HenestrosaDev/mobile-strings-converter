"""
Xcode String Catalogs (`Localizable.xcstrings`), which hold the strings and plurals of
every language of an iOS app.

The source language of a catalog is the default locale, like Android's `values`
directory or iOS' `Base.lproj` directory, and the other languages keep their code (e.g.
`es`). Catalogs need the code of their source language, so it must be given when
writing them. Strings without a value in the source language take their key as the
value, as Xcode does. Arrays, device variations and plurals with several variables
(substitutions) are not supported, so they are skipped.
"""

import json
import warnings
from typing import Dict, Optional

from .. import placeholders
from ..exceptions import ConversionWarning
from ..model import DEFAULT_LOCALE, PLURAL_QUANTITIES, Catalog, Entry, Value
from .text import decode


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    try:
        catalog_data = json.loads(decode(data))
        strings = catalog_data["strings"]
        source_language = catalog_data["sourceLanguage"]
    except (ValueError, KeyError, TypeError, AttributeError):
        strings = source_language = None

    if not isinstance(strings, dict) or not isinstance(source_language, str):
        raise ValueError("The file provided is not a valid .xcstrings file.")

    entries = []
    skipped = []

    for name, definition in strings.items():
        definition = definition or {}
        localizations = definition.get("localizations", {})
        values = {}

        if source_language not in localizations:
            # Xcode leaves out the source language when the value is the key
            values[DEFAULT_LOCALE] = name

        for language, localization in localizations.items():
            value = _get_value(localization)
            if value is None:
                skipped.append(f"{name} ({language})")
            elif language == source_language:
                values[DEFAULT_LOCALE] = value
            else:
                values[language] = value

        # The default locale goes first, as in the other file types
        if DEFAULT_LOCALE in values:
            values = {DEFAULT_LOCALE: values.pop(DEFAULT_LOCALE), **values}

        entries.append(
            Entry(
                name,
                values,
                comment=definition.get("comment"),
                translatable=definition.get("shouldTranslate", True),
            )
        )

    if skipped:
        warnings.warn(
            f"Skipped {len(skipped)} translation(s) because only strings and plurals "
            f"with a single variable are supported: {', '.join(skipped)}",
            ConversionWarning,
        )

    return Catalog(entries)


def serialize(catalog: Catalog, source_language: Optional[str] = None) -> bytes:
    """
    :param catalog: Strings to write
    :type catalog: Catalog
    :param source_language: Code of the source language of the catalog (e.g. `en`),
        which the strings of the default locale are written as
    :type source_language: Optional[str]
    """

    if not source_language:
        raise ValueError(
            "String Catalogs need the code of their source language, which the "
            "default strings (e.g. Android's `values` or iOS' `Base.lproj`) are "
            "written as. Pass it with `--source-language` (e.g. `--source-language "
            "en`)."
        )

    if DEFAULT_LOCALE in catalog.locales and source_language in catalog.locales:
        raise ValueError(
            f"The strings of the default locale can't be written as {source_language}, "
            f"as {source_language} already has its own strings. Pass another source "
            f"language."
        )

    strings = {}
    skipped = []

    for entry in catalog.entries:
        definition = {}
        if entry.comment:
            definition["comment"] = entry.comment
        definition["extractionState"] = "manual"

        localizations = {}
        for locale, value in entry.values.items():
            if locale == DEFAULT_LOCALE:
                locale = source_language

            localization = _to_localization(value)
            if localization is None:
                skipped.append(entry.name)
            else:
                localizations[locale] = localization

        if localizations:
            definition["localizations"] = localizations
        if not entry.translatable:
            definition["shouldTranslate"] = False

        strings[entry.name] = definition

    if skipped:
        warnings.warn(
            f"Skipped {len(set(skipped))} array(s) because .xcstrings files can't hold "
            f"them: {', '.join(dict.fromkeys(skipped))}",
            ConversionWarning,
        )

    catalog_data = {
        "sourceLanguage": source_language,
        "strings": strings,
        "version": "1.0",
    }

    # Same format as Xcode
    return (
        json.dumps(catalog_data, ensure_ascii=False, indent=2, separators=(",", " : "))
        + "\n"
    ).encode("utf-8")


def _get_value(localization) -> Optional[Value]:
    """Returns the value of a localization, or None if it's not supported."""

    if not isinstance(localization, dict):
        return None

    if "stringUnit" in localization:
        return _get_string_unit_value(localization["stringUnit"])

    plural = localization.get("variations", {}).get("plural")
    if isinstance(plural, dict) and set(localization) == {"variations"}:
        values = {
            quantity: _get_string_unit_value(plural[quantity].get("stringUnit"))
            for quantity in PLURAL_QUANTITIES
            if isinstance(plural.get(quantity), dict)
        }
        if all(value is not None for value in values.values()):
            return values

    return None


def _get_string_unit_value(string_unit) -> Optional[str]:
    if not isinstance(string_unit, dict) or "value" not in string_unit:
        return None
    return str(string_unit["value"])


def _to_localization(value: Value) -> Optional[Dict]:
    if isinstance(value, str):
        return _string_unit(value)

    if isinstance(value, dict):
        return {
            "variations": {
                "plural": {
                    quantity: _string_unit(item) for quantity, item in value.items()
                }
            }
        }

    return None


def _string_unit(value: str) -> Dict:
    return {"stringUnit": {"state": "translated", "value": placeholders.to_ios(value)}}
