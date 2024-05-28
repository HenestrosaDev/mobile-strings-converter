import unittest

from base_tests import BaseTests


class TestToHtml(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.html"


class TestFromHtml(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.html"


if __name__ == "__main__":
    unittest.main()
