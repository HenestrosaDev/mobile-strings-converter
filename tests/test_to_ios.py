from unittest import main

from base_tests import BaseTests


class TestToIos(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "Localizable.strings"


if __name__ == "__main__":
    main()
