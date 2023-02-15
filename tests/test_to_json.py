import sys
from pathlib import Path
from unittest import main

# https://stackoverflow.com/a/34938623/15675885
sys.path.append(str(Path(__file__).parent.parent / "src"))
from android_strings_converter import to_json
from base_converter_test import BaseConverterTest


class TestJson(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepaths = [
            Path(__file__).parent / "files/json/strings-en.json",
            Path(__file__).parent / "files/json/strings-es.json",
            Path(__file__).parent / "files/json/strings-zh.json",
        ]
        self.output_filepath = Path("strings.json")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_json)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        super().converter_writes_correct_data_helper(to_json)


if __name__ == "__main__":
    main()
