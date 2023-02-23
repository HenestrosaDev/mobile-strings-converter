from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_ods


class TestToOds(BaseTests.BaseTestToXlsxOds):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.ods"
        self.converter_func = to_ods


if __name__ == "__main__":
    main()
