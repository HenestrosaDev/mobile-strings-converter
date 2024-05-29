import unittest

from base_tests import BaseTests


class TestToJson(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.json"


class TestFromJson(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.json"


if __name__ == "__main__":
    unittest.main()
