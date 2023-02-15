from pathlib import Path
from unittest import main

import pandas as pd
from android_strings_converter.converter import to_xlsx
from base_converter_test import BaseConverterTest
from constants import XLSX_FILEPATHS


class TestXlsx(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepaths = XLSX_FILEPATHS
        self.output_filepath = Path("strings.xlsx")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_xlsx)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        for xml_filepath in self.input_filepaths:
            to_xlsx(xml_filepath, self.output_filepath)

            language_code = xml_filepath.stem[-2:]  # strings-zh
            extension = self.output_filepath.suffix
            template_filepath = [
                template_filepath
                for template_filepath in self.template_filepaths
                if f"strings-{language_code}{extension}" in template_filepath.name
            ][0]

            # Load the two Excel files into pandas dataframes
            df1 = pd.read_excel(template_filepath)
            df2 = pd.read_excel(self.output_filepath)

            # Compare the dataframes to check if they are equal
            self.assertTrue(df1.equals(df2))


if __name__ == "__main__":
    main()
