from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_csv


class TestToCsv(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.csv"
        self.converter_func = to_csv


if __name__ == "__main__":
    main()
