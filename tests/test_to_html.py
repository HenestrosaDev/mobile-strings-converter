from unittest import main

from base_tests import BaseTests


class TestToHtml(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.html"


if __name__ == "__main__":
    main()
