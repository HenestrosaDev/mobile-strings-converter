from pathlib import Path
from unittest import main

from android_strings_converter.converter import to_html
from base_converter_test import BaseConverterTest
from constants import HTML_FILEPATHS


class TestHtml(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepaths = HTML_FILEPATHS
        self.output_filepath = Path("strings.html")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_html)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        super().converter_writes_correct_data_helper(to_html)


if __name__ == "__main__":
    main()
