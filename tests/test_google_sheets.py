import sys
import unittest
from pathlib import Path
from unittest import mock

import gspread
from base_tests import get_strings

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    Catalog,
    Entry,
    MissingDependencyError,
    load,
    read_google_sheets,
    write_google_sheets,
)

ANDROID_FILEPATH = Path(__file__).parent / "files/input/strings.xml"
CREDENTIALS_FILEPATH = Path("service_account.json")


@mock.patch("gspread.service_account")
class TestWriteGoogleSheets(unittest.TestCase):
    def test_writes_all_rows_in_one_request(self, service_account):
        sheet = service_account.return_value.open.return_value.sheet1

        write_google_sheets(load(ANDROID_FILEPATH), "strings", CREDENTIALS_FILEPATH)

        service_account.assert_called_once_with(filename=CREDENTIALS_FILEPATH)
        service_account.return_value.open.assert_called_once_with("strings")
        sheet.clear.assert_called_once()
        sheet.update.assert_called_once_with(
            [["NAME", "VALUE"]]
            + [[name, value] for name, value in get_strings(ANDROID_FILEPATH)]
        )

    def test_default_credentials(self, service_account):
        write_google_sheets(load(ANDROID_FILEPATH), "strings")

        service_account.assert_called_once_with()

    def test_spreadsheet_not_found(self, service_account):
        service_account.return_value.open.side_effect = gspread.SpreadsheetNotFound

        with self.assertRaises(ValueError):
            write_google_sheets(load(ANDROID_FILEPATH), "strings")


@mock.patch("gspread.service_account")
class TestReadGoogleSheets(unittest.TestCase):
    def test_reads_the_first_sheet(self, service_account):
        sheet = service_account.return_value.open.return_value.sheet1
        sheet.get_all_values.return_value = [
            ["NAME", "VALUE", "es", "COMMENT"],
            ["hello", "Hello", "Hola", "Greeting"],
            ["songs[one]", "%d song", "%d canción", ""],
            ["songs[other]", "%d songs", "", ""],
        ]

        catalog = read_google_sheets("translations", CREDENTIALS_FILEPATH)

        service_account.return_value.open.assert_called_once_with("translations")
        self.assertEqual(
            Catalog(
                [
                    Entry(
                        "hello",
                        {DEFAULT_LOCALE: "Hello", "es": "Hola"},
                        comment="Greeting",
                    ),
                    Entry(
                        "songs",
                        {
                            DEFAULT_LOCALE: {"one": "%d song", "other": "%d songs"},
                            "es": {"one": "%d canción"},
                        },
                    ),
                ]
            ),
            catalog,
        )

    def test_empty_sheet(self, service_account):
        sheet = service_account.return_value.open.return_value.sheet1
        sheet.get_all_values.return_value = []

        self.assertEqual(Catalog(), read_google_sheets("translations"))


class TestMissingDependencies(unittest.TestCase):
    def test_google_sheets(self):
        with (
            mock.patch.dict(sys.modules, {"gspread": None}),
            self.assertRaisesRegex(MissingDependencyError, r"\[sheets\]"),
        ):
            read_google_sheets("translations")

    def test_pdf(self):
        from mobile_strings_converter import serialize

        catalog = Catalog([Entry("hello", {DEFAULT_LOCALE: "Hello"})])
        with (
            mock.patch.dict(sys.modules, {"fpdf": None}),
            self.assertRaisesRegex(MissingDependencyError, r"\[pdf\]"),
        ):
            serialize(catalog, ".pdf")

    def test_pdf_fonts(self):
        from mobile_strings_converter import serialize

        catalog = Catalog([Entry("hello", {DEFAULT_LOCALE: "Hello"})])
        with (
            mock.patch.dict(sys.modules, {"mobile_strings_converter_fonts": None}),
            self.assertRaisesRegex(MissingDependencyError, r"\[pdf\]"),
        ):
            serialize(catalog, ".pdf")


if __name__ == "__main__":
    unittest.main()
