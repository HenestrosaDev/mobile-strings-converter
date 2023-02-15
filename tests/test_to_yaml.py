import sys
from pathlib import Path
from unittest import main

# https://stackoverflow.com/a/34938623/15675885
sys.path.append(str(Path(__file__).parent.parent / "src"))
from android_strings_converter import to_yaml
from base_converter_test import BaseConverterTest


class TestYaml(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepaths = [
            Path(__file__).parent / "files/yaml/strings-en.yaml",
            Path(__file__).parent / "files/yaml/strings-es.yaml",
            Path(__file__).parent / "files/yaml/strings-zh.yaml",
        ]
        self.output_filepath = Path("strings.yaml")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_yaml)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        super().converter_writes_correct_data_helper(to_yaml)


if __name__ == "__main__":
    main()
