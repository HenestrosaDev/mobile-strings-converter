import unittest

from base_tests import BaseTests, SameStringsMixin

from mobile_strings_converter.converter import convert_strings


class TestToPdf(SameStringsMixin, BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.pdf"

    def test_converter_lists_unsupported_strings(self):
        errors_filepath = self.output_dir / "strings-errors.txt"

        # The file is overwritten on each conversion
        for _ in range(2):
            convert_strings(self.input_filepath_android, self.output_filepath)

        errors = errors_filepath.read_text(encoding="utf-8").splitlines()
        self.assertIn("මගේ යෙදුම භුක්ති විඳින්න not supported", errors)
        self.assertEqual(len(errors), len(set(errors)))


class TestFromPdf(BaseTests.ConvertFromTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.pdf"


if __name__ == "__main__":
    unittest.main()
