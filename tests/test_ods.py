import unittest

from base_tests import BaseTests, SameStringsMixin


class TestToOds(SameStringsMixin, BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.ods"


class TestFromOds(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.ods"


if __name__ == "__main__":
    unittest.main()
