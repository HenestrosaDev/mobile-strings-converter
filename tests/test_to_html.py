from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_html


class TestToHtml(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.html"
        self.converter_func = to_html


if __name__ == "__main__":
    main()
