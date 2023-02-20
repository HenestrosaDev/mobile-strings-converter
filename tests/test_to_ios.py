from pathlib import Path
from unittest import main

from android_strings_converter import to_ios
from base_converter_test import BaseConverterTest


class TestToIos(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepath = Path(__file__).parent / "files/Localizable.strings"
        self.output_filepath = Path("Localizable.strings")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_ios)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        super().converter_writes_correct_data_helper(to_ios)


if __name__ == "__main__":
    main()