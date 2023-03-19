from unittest import main

from base_tests import BaseTests


class TestToAndroid(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xml"


if __name__ == "__main__":
    main()
