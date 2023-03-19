from unittest import main

from base_tests import BaseTests


class TestToCsv(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.csv"


if __name__ == "__main__":
    main()
