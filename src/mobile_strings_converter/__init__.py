"""Convert Android & iOS strings files to any supported file type and vice versa."""

from importlib.metadata import PackageNotFoundError, version

from .check import Issue, check, find_duplicates
from .exceptions import (
    ConversionWarning,
    MissingDependencyError,
    UnsupportedCharactersWarning,
)
from .files import load, locale_from_path, localized_path, save, save_split
from .formats import INPUT_FILE_TYPES, SUPPORTED_FILE_TYPES, parse, serialize
from .google_sheets import read_google_sheets, write_google_sheets
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
    # Google Sheets
    "read_google_sheets",
    "write_google_sheets",
    # Checks
    "Issue",
    "check",
    "find_duplicates",
    # Errors and warnings
    "ConversionWarning",
    "MissingDependencyError",
    "UnsupportedCharactersWarning",
]

try:
    # The version is defined in `pyproject.toml`
    __version__ = version("mobile-strings-converter")
except PackageNotFoundError:
    __version__ = "unknown"
