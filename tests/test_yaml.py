import unittest

from base_tests import BaseTests


class TestToYaml(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.yaml"


class TestFromYaml(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.yaml"


if __name__ == "__main__":
    unittest.main()
