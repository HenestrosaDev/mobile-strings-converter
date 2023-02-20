from pathlib import Path
from unittest import main

from android_strings_converter import to_csv
from base_converter_test import BaseConverterTest


class TestToCsv(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepath = Path(__file__).parent / "files/strings.csv"
        self.output_filepath = Path("strings.csv")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_csv)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        super().converter_writes_correct_data_helper(to_csv)


if __name__ == "__main__":
    main()
