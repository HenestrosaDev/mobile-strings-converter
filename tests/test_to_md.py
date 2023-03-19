from unittest import main

from base_tests import BaseTests


class TestToMd(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.md"


if __name__ == "__main__":
    main()
