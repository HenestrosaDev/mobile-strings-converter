from unittest import main

from base_tests import BaseTests


class TestToJson(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.json"


if __name__ == "__main__":
    main()
