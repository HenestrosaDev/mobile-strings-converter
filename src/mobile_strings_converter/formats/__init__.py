"""
Readers and writers of every supported file type. They work with the content of the
files (bytes), not with paths, so they can be used without a file system.
"""

from types import ModuleType
from typing import Dict

from ..model import DEFAULT_LOCALE, Catalog
from . import (
    android,
    csvfile,
    html_table,
    ios,
    jsonfile,
    markdown,
    ods,
    pdf,
    stringsdict,
    xcstrings,
    xlsx,
    yamlfile,
)

FORMATS: Dict[str, ModuleType] = {
    ".csv": csvfile,
    ".xlsx": xlsx,
    ".ods": ods,
    ".md": markdown,
    ".json": jsonfile,
    ".yaml": yamlfile,
    ".html": html_table,
    ".strings": ios,
    ".stringsdict": stringsdict,
    ".xcstrings": xcstrings,
    ".xml": android,
    ".pdf": pdf,
}

SUPPORTED_FILE_TYPES = list(FORMATS)


def normalize_file_type(file_type: str) -> str:
    """Returns the file type as a lowercase extension with a leading dot."""

    file_type = file_type.lower()
    return file_type if file_type.startswith(".") else f".{file_type}"


def is_multi_locale(file_type: str) -> bool:
    """Returns True if files of this type can hold the strings of several locales."""

    return getattr(_get_format(file_type), "MULTI_LOCALE", True)


def parse(
    data: bytes,
    file_type: str,
    locale: str = DEFAULT_LOCALE,
    with_comments: bool = False,
) -> Catalog:
    """
    Reads the strings from the content of a file.

    :param data: Content of the file
    :type data: bytes
    :param file_type: Extension of the file, e.g. `.xml` or `xml`
    :type file_type: str
    :param locale: Locale of the strings. For tabular file types, it's the locale of the
        `VALUE` column, as the other columns are named after their locale.
    :type locale: str
    :param with_comments: True to read the commented out strings of `.xml` and
        `.strings` files as well
    :type with_comments: bool
    :return: The strings of the file
    :rtype: Catalog
    """

    return _get_format(file_type).parse(data, locale, with_comments)


def serialize(catalog: Catalog, file_type: str) -> bytes:
    """
    Writes the strings to the content of a file.

    `.xml`, `.strings` and `.stringsdict` files can only hold one locale, so a
    `ValueError` is raised for multi-locale catalogs. Use `Catalog.split` to write a
    file per locale.

    :param catalog: Strings to write
    :type catalog: Catalog
    :param file_type: Extension of the file, e.g. `.xml` or `xml`
    :type file_type: str
    :return: The content of the file
    :rtype: bytes
    """

    return _get_format(file_type).serialize(catalog)


def _get_format(file_type: str) -> ModuleType:
    file_type = normalize_file_type(file_type)
    if file_type not in FORMATS:
        raise ValueError(
            f"File type not supported: {file_type}. Feel free to create an issue here "
            f"(https://github.com/HenestrosaDev/mobile-strings-converter/issues) if you "
            f"want the file type to be supported by the package."
        )

    return FORMATS[file_type]
