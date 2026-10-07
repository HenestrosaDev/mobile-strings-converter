# Copyright (c) 2024 mobile-strings-converter

# @license: http://www.opensource.org/licenses/mit-license.php
# @author: José Carlos López Henestrosa

"""Imports for the mobile-strings-converter package."""

from importlib.metadata import PackageNotFoundError, version

from .converter import convert_strings, get_strings, to_google_sheets

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
