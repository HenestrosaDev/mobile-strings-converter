"""
Reading and writing the strings of a Google spreadsheet, laid out like any other table
(see `formats.table`).

The spreadsheet must exist and be shared with the `client_email` of the service account
whose credentials are used.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from .exceptions import MissingDependencyError
from .formats import table
from .model import DEFAULT_LOCALE, Catalog

if TYPE_CHECKING:
    from gspread import Worksheet


def read_google_sheets(
    spreadsheet_name: str,
    credentials_filepath: Path | None = None,
    locale: str = DEFAULT_LOCALE,
) -> Catalog:
    """
    Reads the strings of the first sheet of a Google spreadsheet.

    :param spreadsheet_name: Name of the spreadsheet to read
    :type spreadsheet_name: str
    :param credentials_filepath: Path to the `service_account.json` of the service
        account. If None, gspread's default path is used
        (`~/.config/gspread/service_account.json`).
    :type credentials_filepath: Path | None
    :param locale: Locale of the `VALUE` column
    :type locale: str
    :return: The strings of the spreadsheet
    :rtype: Catalog
    """

    rows = _open_sheet(spreadsheet_name, credentials_filepath).get_all_values()
    return table.from_table(rows[0] if rows else None, rows[1:], locale)


def write_google_sheets(
    catalog: Catalog,
    spreadsheet_name: str,
    credentials_filepath: Path | None = None,
) -> None:
    """
    Writes the strings to the first sheet of a Google spreadsheet, replacing its
    content.

    :param catalog: Strings to write
    :type catalog: Catalog
    :param spreadsheet_name: Name of the spreadsheet to write to
    :type spreadsheet_name: str
    :param credentials_filepath: Path to the `service_account.json` of the service
        account. If None, gspread's default path is used
        (`~/.config/gspread/service_account.json`).
    :type credentials_filepath: Path | None
    """

    sheet = _open_sheet(spreadsheet_name, credentials_filepath)

    # Replace the existing data with the strings in a single request
    sheet.clear()
    sheet.update(table.to_table(catalog))


def _open_sheet(
    spreadsheet_name: str, credentials_filepath: Path | None
) -> "Worksheet":
    try:
        import gspread
    except ImportError:
        raise MissingDependencyError("Google Sheets support", "sheets") from None

    if credentials_filepath is None:
        client = gspread.service_account()
    else:
        client = gspread.service_account(filename=credentials_filepath)

    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        raise ValueError(
            f"Spreadsheet '{spreadsheet_name}' not found. Create it in Google Sheets "
            f"and share it with the `client_email` of your `service_account.json`."
        ) from None

    return spreadsheet.sheet1
