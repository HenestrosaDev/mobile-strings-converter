from unittest import main

from base_tests import BaseTests


class TestToYaml(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.yaml"


if __name__ == "__main__":
    main()
