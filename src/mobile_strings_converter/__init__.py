# Copyright (c) 2024 mobile-strings-converter

# @license: http://www.opensource.org/licenses/mit-license.php
# @author: José Carlos López Henestrosa

"""Imports for the mobile-strings-converter package."""

from importlib.metadata import PackageNotFoundError, version

from .converter import (
    convert_strings,
    get_strings,
    to_google_sheets,
    write_google_sheets,
)
from .exceptions import ConversionWarning, UnsupportedCharactersWarning
from .files import load, locale_from_path, localized_path, save, save_split
from .formats import INPUT_FILE_TYPES, SUPPORTED_FILE_TYPES, parse, serialize
from .model import DEFAULT_LOCALE, PLURAL_QUANTITIES, Catalog, Entry

__all__ = [
    # Data model
    "Catalog",
    "Entry",
    "DEFAULT_LOCALE",
    "PLURAL_QUANTITIES",
    # Content of the files
    "SUPPORTED_FILE_TYPES",
    "INPUT_FILE_TYPES",
    "parse",
    "serialize",
    # Files
    "load",
    "save",
    "save_split",
    "locale_from_path",
    "localized_path",
    # Path-based conversions
    "convert_strings",
    "get_strings",
    "to_google_sheets",
    "write_google_sheets",
    # Warnings
    "ConversionWarning",
    "UnsupportedCharactersWarning",
]

# Constants
try:
    # The version is defined in `pyproject.toml`
    __version__ = version("mobile-strings-converter")
except PackageNotFoundError:
    __version__ = "unknown"

__author__ = "José Carlos López Henestrosa"
__license__ = "MIT"
__author_email__ = "henestrosadev@gmail.com"
__maintainer_email__ = "henestrosadev@gmail.com"
