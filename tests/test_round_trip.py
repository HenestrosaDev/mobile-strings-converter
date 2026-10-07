import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from mobile_strings_converter import INPUT_FILE_TYPES, Catalog, save
from mobile_strings_converter.converter import convert_strings, get_strings

# fmt: off
TRICKY_STRINGS = [
    ("apostrophe", "I'm here"),
    ("quote", 'Say "hi"'),
    ("ampersand", "Tom & Jerry <3"),
    ("pipe", "a | b"),
    ("new_line", "line 1\nline 2"),
    ("backslash", "back\\slash"),
    ("reference", "@string/app_name"),
    ("unicode", "欢迎 مرحبا"),
    ("markup", "Hello <b>World</b> &amp; you"),
    ("url", "http://example.com/*path*/"),
]
# fmt: on


class TestRoundTrip(unittest.TestCase):
    """Strings must be preserved when converted to any file type and back."""

    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self.output_dir = Path(self._temp_dir.name)
        self.input_filepath = self.output_dir / "input.json"
        save(Catalog.from_pairs(TRICKY_STRINGS), self.input_filepath)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_round_trip(self):
        for file_type in INPUT_FILE_TYPES:
            if file_type == ".stringsdict":
                # It only holds plurals
                continue

            with self.subTest(file_type=file_type):
                output_filepath = self.output_dir / f"strings{file_type}"
                convert_strings(
                    self.input_filepath, output_filepath, source_language="en"
                )
                self.assertEqual(TRICKY_STRINGS, get_strings(output_filepath))

    def test_ods_is_an_opendocument_spreadsheet(self):
        output_filepath = self.output_dir / "strings.ods"
        convert_strings(self.input_filepath, output_filepath)

        with zipfile.ZipFile(output_filepath) as ods:
            self.assertEqual(
                b"application/vnd.oasis.opendocument.spreadsheet",
                ods.read("mimetype"),
            )

    def test_unsupported_output_file_type(self):
        with self.assertRaises(ValueError):
            convert_strings(self.input_filepath, self.output_dir / "strings.txt")

    def test_unsupported_input_file_type(self):
        with self.assertRaises(ValueError):
            get_strings(self.output_dir / "strings.txt")


if __name__ == "__main__":
    unittest.main()
