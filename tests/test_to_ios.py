from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_ios


class TestToIos(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "Localizable.strings"
        self.converter_func = to_ios


if __name__ == "__main__":
    main()
