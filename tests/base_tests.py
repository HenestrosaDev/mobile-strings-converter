import unittest
from pathlib import Path
from typing import Callable


class TestHelpers(object):
    class BaseConverterTest(unittest.TestCase):
        # Hook methods
        def setUp(self):
            self.files_path = "files"
            self._file_name: str | None = None

            self.input_filepath_android = (
                Path(__file__).parent / self.files_path / "input/strings.xml"
            )
            self.input_filepath_ios = (
                Path(__file__).parent / self.files_path / "input/Localizable.strings"
            )

            self.converter_func: Callable[[Path, Path, bool], None] | None = None

        def tearDown(self):
            if self.output_filepath and self.output_filepath.exists():
                self.output_filepath.unlink()

        # Properties

        @property
        def file_name(self):
            return self._file_name

        @file_name.setter
        def file_name(self, value):
            self._file_name = value
            self.template_with_comments_filepath: Path = (
                Path(__file__).parent
                / self.files_path
                / f"template-with-comments/{self._file_name}"
            )
            self.template_without_comments_filepath: Path = (
                Path(__file__).parent
                / self.files_path
                / f"template-without-comments/{self._file_name}"
            )
            self.output_filepath = Path(self._file_name)

        # Test methods

        # ------------ ANDROID ------------

        def test_converter_creates_file_with_comments_android(self):
            self._converter_creates_file(
                input_filepath=self.input_filepath_android,
                should_print_comments=True,
            )

        def test_converter_creates_file_without_comments_android(self):
            self._converter_creates_file(
                input_filepath=self.input_filepath_android,
                should_print_comments=False,
            )

        def test_converter_writes_correct_data_with_comments_android(self):
            self._converter_writes_correct_data(
                self.template_with_comments_filepath,
                self.input_filepath_android,
                should_print_comments=True,
            )

        def test_converter_writes_correct_data_without_comments_android(self):
            self._converter_writes_correct_data(
                self.template_without_comments_filepath,
                self.input_filepath_android,
                should_print_comments=False,
            )

        # -------------- iOS --------------

        def test_converter_creates_file_with_comments_ios(self):
            self._converter_creates_file(
                input_filepath=self.input_filepath_ios,
                should_print_comments=True,
            )

        def test_converter_creates_file_without_comments_ios(self):
            self._converter_creates_file(
                input_filepath=self.input_filepath_ios,
                should_print_comments=False,
            )

        def test_converter_writes_correct_data_with_comments_ios(self):
            self._converter_writes_correct_data(
                self.template_with_comments_filepath,
                self.input_filepath_ios,
                should_print_comments=True,
            )

        def test_converter_writes_correct_data_without_comments_ios(self):
            self._converter_writes_correct_data(
                self.template_without_comments_filepath,
                self.input_filepath_ios,
                should_print_comments=False,
            )

        # Private methods

        def _converter_creates_file(
            self,
            input_filepath: Path,
            should_print_comments: bool,
        ):
            self.converter_func(
                input_filepath, self.output_filepath, should_print_comments
            )
            self.assertTrue(self.output_filepath.exists())

        def _converter_writes_correct_data(
            self,
            template_filepath: Path,
            input_filepath: Path,
            should_print_comments: bool,
        ):
            self.converter_func(
                input_filepath, self.output_filepath, should_print_comments
            )

            with open(self.output_filepath, "rb") as test_file, open(
                template_filepath, "rb"
            ) as template_file:
                self.assertEqual(
                    test_file.read().decode("utf-8").replace("\r\n", "\n"),
                    template_file.read().decode("utf-8").replace("\r\n", "\n"),
                )
