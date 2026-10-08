"""
Path-based functions to convert files, kept for backwards compatibility. See `files`
and `formats` for the functions that work with `Catalog`s.
"""

from pathlib import Path
from typing import List, Optional, Tuple

import gspread

from .files import load, save
from .formats import SUPPORTED_FILE_TYPES, normalize_file_type
from .formats.table import to_table
from .model import Catalog

__all__ = [
    "SUPPORTED_FILE_TYPES",
    "convert_strings",
    "get_strings",
    "to_google_sheets",
    "write_google_sheets",
]


def convert_strings(
    input_filepath: Path,
    output_filepath: Path,
    with_comments: bool = False,
    source_language: Optional[str] = None,
):
    """
    Converts the strings of the input file to the type of the output file, which is
    set by its extension. See `SUPPORTED_FILE_TYPES`.

    :param input_filepath: File to extract the strings from
    :type input_filepath: Path
    :param output_filepath: Path of the file to be generated
    :type output_filepath: Path
    :param with_comments: True if the user wants to include comments from
        .strings/.xml to the output file
    :type with_comments: bool
    :param source_language: Code of the language of the default strings (e.g. `en`).
        Required to write `.xcstrings` files, and ignored by any other file type.
    :type source_language: Optional[str]
    """

    output_filepath = Path(output_filepath)

    # Fail before reading the input file
    if normalize_file_type(output_filepath.suffix) not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Output file type not supported: {output_filepath}")

    save(
        load(input_filepath, with_comments=with_comments),
        output_filepath,
        source_language,
    )


def get_strings(
    input_filepath: Path, with_comments: bool = False
) -> List[Tuple[str, str]]:
    """
    Extracts the strings of the first locale of a file as (name, value) pairs.
    Plurals and arrays are flattened, e.g. `songs[one]` or `planets[0]`.

    :param input_filepath: Path to the input file.
    :type input_filepath: Path
    :param with_comments: True if comments should be included (for .strings and
        .xml files), False otherwise.
    :type with_comments: bool
    :return: A list of tuples containing extracted strings and their corresponding values.
    :rtype: List[Tuple[str, str]]
    """

    return load(input_filepath, with_comments=with_comments).to_pairs()


def to_google_sheets(
    input_filepath: Path,
    sheet_name: str,
    credentials_filepath: Path,
    with_comments: bool = False,
):
    """
    Writes the extracted strings from the input filepath to an existing Google
    spreadsheet. The spreadsheet must be shared with the service account's email.

    :param input_filepath: File to extract the strings from
    :type input_filepath: Path
    :param sheet_name: Name of the spreadsheet to write to
    :type sheet_name: str
    :param credentials_filepath: Path to the service_account.json in order to be able
        to access the sheet in the user's Google account
    :type credentials_filepath: Path
    :param with_comments: True if the user wants to include comments from
        .strings/.xml to the sheet
    :type with_comments: bool
    """

    write_google_sheets(
        load(input_filepath, with_comments=with_comments),
        sheet_name,
        credentials_filepath,
    )


def write_google_sheets(
    catalog: Catalog, sheet_name: str, credentials_filepath: Optional[Path]
):
    """
    Writes the strings to the first sheet of an existing Google spreadsheet, replacing
    its content. The spreadsheet must be shared with the service account's email.

    :param catalog: Strings to write
    :type catalog: Catalog
    :param sheet_name: Name of the spreadsheet to write to
    :type sheet_name: str
    :param credentials_filepath: Path to the service_account.json in order to be able
        to access the sheet in the user's Google account
    :type credentials_filepath: Path
    """

    client = gspread.service_account(filename=credentials_filepath)

    try:
        spreadsheet = client.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        raise ValueError(
            f"Spreadsheet '{sheet_name}' not found. Create it in Google Sheets and "
            f"share it with the `client_email` from your `service_account.json`."
        ) from None

    sheet = spreadsheet.sheet1

    # Replace the existing data with the strings in a single request
    sheet.clear()
    sheet.update(to_table(catalog))
