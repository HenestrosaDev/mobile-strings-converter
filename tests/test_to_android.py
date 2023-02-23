from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_android


class TestToAndroid(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xml"
        self.converter_func = to_android


if __name__ == "__main__":
    main()
