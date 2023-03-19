from unittest import main

from base_tests import BaseTests


class TestToOds(BaseTests.BaseTestToSheet):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.ods"


if __name__ == "__main__":
    main()
