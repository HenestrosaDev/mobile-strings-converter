import unittest

from base_tests import BaseTests


class TestToCsv(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.csv"


class TestFromCsv(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.csv"


if __name__ == "__main__":
    unittest.main()
