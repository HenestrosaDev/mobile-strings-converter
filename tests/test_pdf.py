import unittest
import warnings
from pathlib import Path

from base_tests import BaseTests

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    INPUT_FILE_TYPES,
    Catalog,
    Entry,
    get_strings,
    parse,
    serialize,
)
from mobile_strings_converter.converter import convert_strings


class TestToPdf(BaseTests.ConvertToTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.pdf"

    def _assert_same_content(
        self, output_filepath: Path, template_filepath: Path
    ) -> None:
        # PDF files can't be read back, and they hold their creation date
        data = output_filepath.read_bytes()
        self.assertTrue(data.startswith(b"%PDF-"))
        self.assertTrue(data.rstrip().endswith(b"%%EOF"))

    def test_converter_lists_unsupported_strings(self):
        errors_filepath = self.output_dir / "strings-errors.txt"

        # The file is overwritten on each conversion
        for _ in range(2):
            convert_strings(self.input_filepath_android, self.output_filepath)

        errors = errors_filepath.read_text(encoding="utf-8").splitlines()
        self.assertIn("මගේ යෙදුම භුක්ති විඳින්න not supported", errors)
        self.assertEqual(len(errors), len(set(errors)))


class TestPdfIsOutputOnly(unittest.TestCase):
    def setUp(self):
        catalog = Catalog([Entry("hello", {DEFAULT_LOCALE: "Hello", "es": "Hola"})])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.data = serialize(catalog, ".pdf")

    def test_parse(self):
        with self.assertRaisesRegex(ValueError, "can only be written"):
            parse(self.data, ".pdf")

    def test_get_strings(self):
        with self.assertRaises(ValueError):
            get_strings(Path("strings.pdf"))

    def test_not_an_input_file_type(self):
        self.assertNotIn(".pdf", INPUT_FILE_TYPES)

    def test_strings_are_not_embedded(self):
        self.assertNotIn(b"/EmbeddedFile", self.data)


if __name__ == "__main__":
    unittest.main()
