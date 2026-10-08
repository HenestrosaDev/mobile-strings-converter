import unittest

from base_tests import BaseTests, SameStringsMixin


class TestToXlsx(SameStringsMixin, BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xlsx"


class TestFromXlsx(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xlsx"


if __name__ == "__main__":
    unittest.main()
