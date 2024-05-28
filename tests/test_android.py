import unittest

from base_tests import BaseTests


class TestToAndroid(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xml"


class TestFromAndroid(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xml"


if __name__ == "__main__":
    unittest.main()
