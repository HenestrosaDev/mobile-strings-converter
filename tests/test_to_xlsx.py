from pathlib import Path
from unittest import main

import pandas as pd
from android_strings_converter import to_xlsx_ods
from base_converter_test import BaseConverterTest


class TestToXlsx(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepath = Path(__file__).parent / "files/strings.xlsx"
        self.output_filepath = Path("strings.xlsx")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_xlsx_ods)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        to_xlsx_ods(self.input_filepath, self.output_filepath)

        # Load the two Excel files into pandas dataframes
        df1 = pd.read_excel(self.template_filepath)
        df2 = pd.read_excel(self.output_filepath)

        # Compare the dataframes to check if they are equal
        self.assertTrue(df1.equals(df2))


if __name__ == "__main__":
    main()
