from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_json


class TestToJson(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.json"
        self.converter_func = to_json


if __name__ == "__main__":
    main()
