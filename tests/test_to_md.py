from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_md


class TestToMd(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.md"
        self.converter_func = to_md


if __name__ == "__main__":
    main()
