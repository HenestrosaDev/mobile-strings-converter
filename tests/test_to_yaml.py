from pathlib import Path
from unittest import main

from android_strings_converter.converter import to_yaml
from base_converter_test import BaseConverterTest
from constants import YAML_FILEPATHS


class TestYaml(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepaths = YAML_FILEPATHS
        self.output_filepath = Path("strings.yaml")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_yaml)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        super().converter_writes_correct_data_helper(to_yaml)


if __name__ == "__main__":
    main()
