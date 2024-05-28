import unittest

from base_tests import BaseTests


class TestToMd(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.md"


class TestFromMd(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.md"


if __name__ == "__main__":
    unittest.main()
