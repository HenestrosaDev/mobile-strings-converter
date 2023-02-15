import os
import unittest
from pathlib import Path

import gspread
from android_strings_converter import to_google_sheets
from google.oauth2.credentials import Credentials


class TestGoogleSheets(unittest.TestCase):
    def setUp(self):
        # Set up a credentials file for the Google Sheets API
        credentials_filepath = Path("./test_file/test_credentials.json")
        with open(credentials_filepath, "w") as file:
            file.write("test")

        self.xml_filepath = Path("./test_file/test_strings.xml")
        self.sheet_name = "Test Sheet"
        self.credentials_filepath = credentials_filepath

    def tearDown(self):
        # Remove the credentials file after the tests are done
        os.remove(self.credentials_filepath)

    def test_to_google_sheets(self):
        to_google_sheets(self.xml_filepath, self.sheet_name, self.credentials_filepath)

        # Check if the sheet has been created and has the correct data
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_file(
            self.credentials_filepath, scope
        )
        client = gspread.authorize(credentials)
        sheet = client.open(self.sheet_name).sheet1
        self.assertEqual(sheet.row_count, 2)
        self.assertEqual(sheet.col_count, 2)
        self.assertEqual(sheet.cell(1, 1).value, "name")
        self.assertEqual(sheet.cell(1, 2).value, "value")
        self.assertEqual(sheet.cell(2, 1).value, "app_name")
        self.assertEqual(sheet.cell(2, 2).value, "Test App")


if __name__ == "__main__":
    unittest.main()
