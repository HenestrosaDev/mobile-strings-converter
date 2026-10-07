"""
iOS plural strings (`Localizable.stringsdict`).

Only plurals whose format is a single variable (`%#@variable@`) are supported, which
is how Xcode and most tools write them. Strings and arrays can't be written to
`.stringsdict` files, so they are skipped (see `ios` for strings).
"""

import plistlib
import re
import warnings

from .. import placeholders
from ..exceptions import ConversionWarning
from ..model import PLURAL_QUANTITIES, Catalog, Entry

MULTI_LOCALE = False

FORMAT_KEY = "NSStringLocalizedFormatKey"
SPEC_TYPE_KEY = "NSStringFormatSpecTypeKey"
VALUE_TYPE_KEY = "NSStringFormatValueTypeKey"
PLURAL_RULE_TYPE = "NSStringPluralRuleType"

# Name of the variable of the plurals written by `serialize`
VARIABLE = "value"

# Length and conversion of a placeholder, e.g. `ld` in `%1$ld`
_PLACEHOLDER_TYPE_PATTERN = re.compile(
    r"%(?:\d+\$)?[-#+0]*\d*(?:\.\d+)?(?P<type>(?:hh|h|ll|l|q|z|t|j)?[dDiuUxXoOfeEgGaA])"
)


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    try:
        plist = plistlib.loads(data)
    except Exception:
        raise ValueError(
            "The file provided is not a valid .stringsdict file."
        ) from None

    if not isinstance(plist, dict):
        raise ValueError("The file provided is not a valid .stringsdict file.")

    entries = []
    skipped = []

    for name, definition in plist.items():
        plural = _get_plural(definition)
        if plural is None:
            skipped.append(name)
        else:
            entries.append(Entry(name, {locale: plural}))

    if skipped:
        warnings.warn(
            f"Skipped {len(skipped)} entry(ies) because only plurals with a single "
            f"variable (`%#@variable@`) are supported: {', '.join(skipped)}",
            ConversionWarning,
        )

    return Catalog(entries)


def serialize(catalog: Catalog) -> bytes:
    if catalog.is_multi_locale:
        raise ValueError(
            "An iOS .stringsdict file can only hold one locale, but the strings have "
            f"{len(catalog.locales)}: {', '.join(catalog.locales)}."
        )

    plist = {}
    skipped = []

    for entry in catalog.entries:
        value = next(iter(entry.values.values()), "")
        if not isinstance(value, dict):
            skipped.append(entry.name)
            continue

        plural = {
            quantity: placeholders.to_ios(item) for quantity, item in value.items()
        }
        plist[entry.name] = {
            FORMAT_KEY: f"%#@{VARIABLE}@",
            VARIABLE: {
                SPEC_TYPE_KEY: PLURAL_RULE_TYPE,
                VALUE_TYPE_KEY: _get_value_type(plural),
                **plural,
            },
        }

    if skipped:
        warnings.warn(
            f"Skipped {len(skipped)} string(s)/array(s) because .stringsdict files can "
            f"only hold plurals: {', '.join(skipped)}. Strings can be written to "
            f".strings files.",
            ConversionWarning,
        )

    return plistlib.dumps(plist, sort_keys=False)


def _get_plural(definition):
    """Returns the plural of a definition, or None if it's not supported."""

    if not isinstance(definition, dict):
        return None

    match = re.fullmatch(r"%#@(?P<variable>[^@]+)@", str(definition.get(FORMAT_KEY)))
    variable = match and definition.get(match.group("variable"))
    if not isinstance(variable, dict) or variable.get(SPEC_TYPE_KEY) != (
        PLURAL_RULE_TYPE
    ):
        return None

    return {
        quantity: str(variable[quantity])
        for quantity in PLURAL_QUANTITIES
        if quantity in variable
    }


def _get_value_type(plural) -> str:
    """Returns the type of the number of the plural, e.g. `d` or `ld`."""

    for item in [plural.get("other", ""), *plural.values()]:
        match = _PLACEHOLDER_TYPE_PATTERN.search(item.replace("%%", ""))
        if match:
            return match.group("type")

    return "d"
