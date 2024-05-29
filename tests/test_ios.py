import unittest

from base_tests import BaseTests


class TestToIos(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "Localizable.strings"


class TestFromIos(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "Localizable.strings"


if __name__ == "__main__":
    unittest.main()
