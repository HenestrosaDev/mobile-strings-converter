from unittest import main

from base_tests import BaseTests


class TestToXlsx(BaseTests.BaseTestToSheet):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.xlsx"


if __name__ == "__main__":
    main()
