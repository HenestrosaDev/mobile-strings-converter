from unittest import main

from base_tests import BaseTests
from mobile_strings_converter import to_yaml


class TestToYaml(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.yaml"
        self.converter_func = to_yaml


if __name__ == "__main__":
    main()
