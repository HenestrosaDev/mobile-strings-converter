import unittest
from pathlib import Path
from unittest import mock

import gspread

from mobile_strings_converter.converter import get_strings, to_google_sheets

ANDROID_FILEPATH = Path(__file__).parent / "files/input/strings.xml"


class TestToGoogleSheets(unittest.TestCase):
    @mock.patch("gspread.service_account")
    def test_writes_all_rows_in_one_request(self, service_account):
        sheet = service_account.return_value.open.return_value.sheet1

        to_google_sheets(ANDROID_FILEPATH, "strings", Path("service_account.json"))

        service_account.assert_called_once_with(filename=Path("service_account.json"))
        service_account.return_value.open.assert_called_once_with("strings")
        sheet.clear.assert_called_once()
        sheet.update.assert_called_once_with(
            [["NAME", "VALUE"]]
            + [[name, value] for name, value in get_strings(ANDROID_FILEPATH)]
        )

    @mock.patch("gspread.service_account")
    def test_spreadsheet_not_found(self, service_account):
        service_account.return_value.open.side_effect = gspread.SpreadsheetNotFound

        with self.assertRaises(ValueError):
            to_google_sheets(ANDROID_FILEPATH, "strings", Path("service_account.json"))


if __name__ == "__main__":
    unittest.main()
