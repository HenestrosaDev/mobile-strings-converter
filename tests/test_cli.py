import contextlib
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from mobile_strings_converter import load
from mobile_strings_converter.__main__ import main
from mobile_strings_converter.converter import get_strings

FILES_PATH = Path(__file__).parent / "files"
ANDROID_FILEPATH = FILES_PATH / "input/strings.xml"
IOS_FILEPATH = FILES_PATH / "input/Localizable.strings"


class TestCli(unittest.TestCase):
    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self.output_dir = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def _run(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                exit_code = main([str(arg) for arg in args])
            except SystemExit as e:
                exit_code = e.code
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_output_file(self):
        output_filepath = self.output_dir / "nested/strings.json"

        exit_code, _, _ = self._run(ANDROID_FILEPATH, "-f", output_filepath)

        self.assertEqual(0, exit_code)
        self.assertEqual(get_strings(ANDROID_FILEPATH), get_strings(output_filepath))

    def test_output_dir_with_multiple_files(self):
        exit_code, _, _ = self._run(
            ANDROID_FILEPATH, IOS_FILEPATH, "-d", self.output_dir, "-t", "csv"
        )

        self.assertEqual(0, exit_code)
        self.assertTrue((self.output_dir / "strings.csv").exists())
        self.assertTrue((self.output_dir / "Localizable.csv").exists())

    def test_output_dir_keeps_directory_structure(self):
        input_dir = self.output_dir / "res"
        for language in ["es", "fr"]:
            (input_dir / f"values-{language}").mkdir(parents=True)
            (input_dir / f"values-{language}/strings.xml").write_bytes(
                ANDROID_FILEPATH.read_bytes()
            )

        output_dir = self.output_dir / "output"
        exit_code, _, _ = self._run(input_dir, "-d", output_dir, "-t", ".json")

        self.assertEqual(0, exit_code)
        self.assertTrue((output_dir / "values-es/strings.json").exists())
        self.assertTrue((output_dir / "values-fr/strings.json").exists())

    def test_print_comments(self):
        output_filepath = self.output_dir / "strings.json"

        self._run(ANDROID_FILEPATH, "-f", output_filepath, "-p")

        self.assertEqual(
            get_strings(ANDROID_FILEPATH, with_comments=True),
            get_strings(output_filepath),
        )

    def test_output_is_required(self):
        exit_code, _, stderr = self._run(ANDROID_FILEPATH)

        self.assertEqual(2, exit_code)
        self.assertIn("-f, -d or -g", stderr)

    def test_output_dir_requires_target_type(self):
        exit_code, _, stderr = self._run(ANDROID_FILEPATH, "-d", self.output_dir)

        self.assertEqual(2, exit_code)
        self.assertIn("--target-type", stderr)

    def test_unsupported_target_type(self):
        exit_code, _, _ = self._run(
            ANDROID_FILEPATH, "-d", self.output_dir, "-t", "txt"
        )

        self.assertEqual(2, exit_code)

    def test_output_file_with_multiple_files(self):
        exit_code, _, _ = self._run(
            ANDROID_FILEPATH, IOS_FILEPATH, "-f", self.output_dir / "strings.json"
        )

        self.assertEqual(2, exit_code)

    def test_files_with_the_same_name(self):
        other_filepath = self.output_dir / "other/strings.xml"
        other_filepath.parent.mkdir()
        other_filepath.write_bytes(ANDROID_FILEPATH.read_bytes())

        exit_code, _, stderr = self._run(
            ANDROID_FILEPATH, other_filepath, "-d", self.output_dir, "-t", "json"
        )

        self.assertEqual(2, exit_code)
        self.assertIn("same output file", stderr)

    def test_invalid_input_file(self):
        invalid_filepath = self.output_dir / "invalid.xml"
        invalid_filepath.write_text("<resources></resources>")

        exit_code, _, stderr = self._run(
            invalid_filepath, "-f", self.output_dir / "strings.json"
        )

        self.assertEqual(1, exit_code)
        self.assertIn("Could not convert", stderr)

    def test_google_sheets(self):
        credentials_filepath = self.output_dir / "service_account.json"
        credentials_filepath.write_text("{}")

        with mock.patch(
            "mobile_strings_converter.__main__.write_google_sheets"
        ) as write_google_sheets:
            exit_code, _, _ = self._run(ANDROID_FILEPATH, "-g", credentials_filepath)

        self.assertEqual(0, exit_code)
        write_google_sheets.assert_called_once_with(
            load(ANDROID_FILEPATH),
            sheet_name="strings",
            credentials_filepath=credentials_filepath,
        )

    def _write_android_project(self):
        res_dir = self.output_dir / "res"
        for directory, value in [("values", "Hello"), ("values-es", "Hola")]:
            (res_dir / directory).mkdir(parents=True)
            (res_dir / directory / "strings.xml").write_text(
                f'<resources><string name="hello">{value}</string></resources>',
                encoding="utf-8",
            )
        return res_dir

    def test_merge(self):
        res_dir = self._write_android_project()
        output_filepath = self.output_dir / "strings.csv"

        exit_code, _, _ = self._run(res_dir, "-m", "-f", output_filepath)

        self.assertEqual(0, exit_code)
        self.assertEqual(
            "name,value,es\nhello,Hello,Hola\n",
            output_filepath.read_text(encoding="utf-8").replace("\r\n", "\n"),
        )

    def test_merge_to_string_catalog(self):
        res_dir = self._write_android_project()
        output_filepath = self.output_dir / "Localizable.xcstrings"

        exit_code, _, stderr = self._run(res_dir, "-m", "-f", output_filepath)

        self.assertEqual(1, exit_code)
        self.assertIn("--source-language", stderr)

        exit_code, _, _ = self._run(res_dir, "-m", "-f", output_filepath, "-s", "en")

        self.assertEqual(0, exit_code)
        catalog_data = json.loads(output_filepath.read_text(encoding="utf-8"))
        self.assertEqual("en", catalog_data["sourceLanguage"])
        self.assertEqual(
            {"en", "es"}, set(catalog_data["strings"]["hello"]["localizations"])
        )

    def test_merge_requires_output_file(self):
        exit_code, _, stderr = self._run(
            ANDROID_FILEPATH, "-m", "-d", self.output_dir, "-t", "csv"
        )

        self.assertEqual(2, exit_code)
        self.assertIn("--merge", stderr)

    def test_output_dir_splits_locales(self):
        input_filepath = self.output_dir / "translations.csv"
        input_filepath.write_text("name,value,es\nhello,Hello,Hola\n", encoding="utf-8")
        output_dir = self.output_dir / "output"

        exit_code, _, _ = self._run(input_filepath, "-d", output_dir, "-t", "strings")

        self.assertEqual(0, exit_code)
        self.assertEqual(
            [("hello", "Hola")],
            get_strings(output_dir / "es.lproj/Localizable.strings"),
        )
        self.assertEqual(
            [("hello", "Hello")],
            get_strings(output_dir / "Base.lproj/Localizable.strings"),
        )

    def test_output_file_with_several_locales(self):
        input_filepath = self.output_dir / "translations.csv"
        input_filepath.write_text("name,value,es\nhello,Hello,Hola\n", encoding="utf-8")

        exit_code, _, stderr = self._run(
            input_filepath, "-f", self.output_dir / "strings.xml"
        )

        self.assertEqual(1, exit_code)
        self.assertIn("-d/--output-dir", stderr)

    def test_warnings_are_printed(self):
        output_filepath = self.output_dir / "Localizable.strings"
        input_filepath = self.output_dir / "strings.xml"
        input_filepath.write_text(
            '<resources><string-array name="list"><item>A</item></string-array>'
            '<string name="a">A</string></resources>',
            encoding="utf-8",
        )

        exit_code, stdout, _ = self._run(input_filepath, "-f", output_filepath)

        self.assertEqual(0, exit_code)
        self.assertIn("Skipped 1 plural(s)/array(s)", stdout)

    def test_pdf_input(self):
        input_filepath = self.output_dir / "strings.pdf"
        input_filepath.write_bytes(b"%PDF-1.4")

        exit_code, stdout, stderr = self._run(
            input_filepath, "-f", self.output_dir / "strings.json"
        )

        self.assertEqual(2, exit_code)
        self.assertIn("Skipping unsupported file", stdout)
        self.assertIn("no supported input files", stderr)

    def test_module_entry_point(self):
        result = subprocess.run(
            [sys.executable, "-m", "mobile_strings_converter", "--version"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
