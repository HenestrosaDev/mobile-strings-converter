from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_xlsx


class TestToXlsx(BaseTests.BaseTestToXlsxOds):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xlsx"
        self.converter_func = to_xlsx


if __name__ == "__main__":
    main()
