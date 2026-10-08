"""
YAML files map names to values in single-locale catalogs. Multi-locale catalogs map
each locale to its names and values, e.g. `es: {hello: Hola}`.

Plurals are written as mappings (e.g. `{one: ..., other: ...}`) and arrays as lists.
"""

import yaml

from ..model import PLURAL_QUANTITIES, Catalog, Entry, to_value
from .text import decode


def parse(data: bytes, locale: str, with_comments: bool = False) -> Catalog:
    yaml_data = yaml.safe_load(decode(data)) or {}

    if not isinstance(yaml_data, dict):
        raise ValueError("The file provided is not a valid .yaml file.")

    if _is_multi_locale(yaml_data):
        return Catalog.merge(
            _parse_mapping(strings, str(mapping_locale))
            for mapping_locale, strings in yaml_data.items()
        )

    return _parse_mapping(yaml_data, locale)


def serialize(catalog: Catalog) -> bytes:
    if catalog.is_multi_locale:
        yaml_data = {
            locale: _to_mapping(catalog.for_locale(locale), locale)
            for locale in catalog.locales
        }
    else:
        locale = next(iter(catalog.locales), None)
        yaml_data = _to_mapping(catalog, locale)

    # Keep the order of the input file
    return yaml.dump(
        yaml_data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    ).encode("utf-8")


def _is_multi_locale(yaml_data: dict) -> bool:
    """
    Returns True if every value is a mapping of names, as opposed to a mapping of
    plural quantities.
    """

    return all(isinstance(value, dict) for value in yaml_data.values()) and any(
        key not in PLURAL_QUANTITIES for value in yaml_data.values() for key in value
    )


def _parse_mapping(mapping: dict, locale: str) -> Catalog:
    entries = []
    for name, raw_value in mapping.items():
        value = to_value(raw_value)
        entries.append(Entry(str(name), {} if value is None else {locale: value}))

    return Catalog(entries)


def _to_mapping(catalog: Catalog, locale) -> dict:
    return {entry.name: entry.values.get(locale, "") for entry in catalog.entries}
