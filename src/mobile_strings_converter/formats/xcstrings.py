"""
Xcode String Catalogs (`Localizable.xcstrings`), which hold the strings and plurals of
every language of an iOS app.

The languages keep their code (e.g. `en`), and the default locale is written as the
source language of the catalog (`en` unless the strings already have an `en`
locale). Strings without a value in the source language take their key as the value,
as Xcode does. Arrays, device variations and plurals with several variables
(substitutions) are not supported, so they are skipped.
"""

import json
import warnings
from typing import Dict, Optional

from .. import placeholders
from ..exceptions import ConversionWarning
from ..model import DEFAULT_LOCALE, PLURAL_QUANTITIES, Catalog, Entry, Value
from .text import decode

# Source language of the catalogs written from strings with a default locale
SOURCE_LANGUAGE = "en"


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    try:
        catalog_data = json.loads(decode(data))
        strings = catalog_data["strings"]
        source_language = catalog_data.get("sourceLanguage", SOURCE_LANGUAGE)
    except (ValueError, KeyError, TypeError, AttributeError):
        strings = None

    if not isinstance(strings, dict):
        raise ValueError("The file provided is not a valid .xcstrings file.")

    entries = []
    skipped = []

    for name, definition in strings.items():
        definition = definition or {}
        localizations = definition.get("localizations", {})
        values = {}

        for language, localization in localizations.items():
            value = _get_value(localization)
            if value is None:
                skipped.append(f"{name} ({language})")
            else:
                values[language] = value

        if source_language not in localizations:
            # Xcode leaves out the source language when the value is the key
            values = {source_language: name, **values}

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


def serialize(catalog: Catalog) -> bytes:
    locales = catalog.locales
    has_source_language = SOURCE_LANGUAGE in locales

    if DEFAULT_LOCALE in locales and has_source_language:
        warnings.warn(
            f"Skipped the default locale because the source language of the catalog "
            f"({SOURCE_LANGUAGE}) already has its own strings.",
            ConversionWarning,
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
                if has_source_language:
                    continue
                locale = SOURCE_LANGUAGE

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
        "sourceLanguage": SOURCE_LANGUAGE,
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
