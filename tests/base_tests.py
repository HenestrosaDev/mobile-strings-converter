import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from mobile_strings_converter.converter import convert_strings, get_strings


# This is a wrapper class that prevents its nested classes from running as tests.
class BaseTests(object):
    # For `test_to_*` files

    class ConvertToTest(unittest.TestCase):
        # Hook methods

        def setUp(self):
            self._file_name: str | None = None

            self.files_path = "files"
            self.input_filepath_android = (
                Path(__file__).parent / self.files_path / "input/strings.xml"
            )
            self.input_filepath_ios = (
                Path(__file__).parent / self.files_path / "input/Localizable.strings"
            )

        def tearDown(self):
            if self.output_filepath.exists():
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
                with_comments=True,
            )

        def test_converter_creates_file_without_comments_android(self):
            self._converter_creates_file(
                input_filepath=self.input_filepath_android,
                with_comments=False,
            )

        def test_converter_writes_correct_data_with_comments_android(self):
            self._converter_writes_correct_data(
                self.template_with_comments_filepath,
                self.input_filepath_android,
                with_comments=True,
            )

        def test_converter_writes_correct_data_without_comments_android(self):
            self._converter_writes_correct_data(
                self.template_without_comments_filepath,
                self.input_filepath_android,
                with_comments=False,
            )

        # -------------- iOS --------------

        def test_converter_creates_file_with_comments_ios(self):
            self._converter_creates_file(
                input_filepath=self.input_filepath_ios,
                with_comments=True,
            )

        def test_converter_creates_file_without_comments_ios(self):
            self._converter_creates_file(
                input_filepath=self.input_filepath_ios,
                with_comments=False,
            )

        def test_converter_writes_correct_data_with_comments_ios(self):
            self._converter_writes_correct_data(
                self.template_with_comments_filepath,
                self.input_filepath_ios,
                with_comments=True,
            )

        def test_converter_writes_correct_data_without_comments_ios(self):
            self._converter_writes_correct_data(
                self.template_without_comments_filepath,
                self.input_filepath_ios,
                with_comments=False,
            )

        # Private methods

        def _converter_creates_file(
            self,
            input_filepath: Path,
            with_comments: bool,
        ):
            convert_strings(input_filepath, self.output_filepath, with_comments)
            self.assertTrue(self.output_filepath.exists())

        def _converter_writes_correct_data(
            self,
            template_filepath: Path,
            input_filepath: Path,
            with_comments: bool,
        ):
            convert_strings(input_filepath, self.output_filepath, with_comments)

            with open(self.output_filepath, "rb") as test_file, open(
                template_filepath, "rb"
            ) as template_file:
                self.assertEqual(
                    test_file.read().decode("utf-8").replace("\r\n", "\n"),
                    template_file.read().decode("utf-8").replace("\r\n", "\n"),
                )

    # For `test_from_*` files

    class ConvertFromTest(unittest.TestCase):
        # Hook methods

        def setUp(self):
            self._file_name: str | None = None

            self.files_path = "files"
            self.android_filepath = (
                Path(__file__).parent / self.files_path / "input/strings.xml"
            )
            self.ios_filepath = (
                Path(__file__).parent / self.files_path / "input/Localizable.strings"
            )

        def tearDown(self):
            if self.output_filepath.exists():
                self.output_filepath.unlink()

        # Properties

        @property
        def file_name(self):
            return self._file_name

        @file_name.setter
        def file_name(self, value):
            self.input_filepath = (
                Path(__file__).parent
                / self.files_path
                / f"template-without-comments/{value}"
            )
            self.output_filepath = Path(value)
            self._file_name = value

        # Test methods

        # ------------ ANDROID ------------

        def test_converter_creates_file_android(self):
            self._converter_creates_file(self.input_filepath)

        def test_converter_writes_correct_data_android(self):
            self._converter_writes_correct_data(
                template_filepath=self.input_filepath,
                input_filepath=self.android_filepath,
            )

        # -------------- iOS --------------

        def test_converter_creates_file_ios(self):
            self._converter_creates_file(self.input_filepath)

        def test_converter_writes_correct_data_ios(self):
            self._converter_writes_correct_data(
                template_filepath=self.input_filepath, input_filepath=self.ios_filepath
            )

        # Private methods

        def _converter_creates_file(
            self,
            input_filepath: Path,
        ):
            convert_strings(input_filepath, self.output_filepath)
            self.assertTrue(self.output_filepath.exists())

        def _converter_writes_correct_data(
            self,
            template_filepath: Path,
            input_filepath: Path,
        ):
            convert_strings(input_filepath, self.output_filepath)

            with open(self.output_filepath, "rb") as test_file, open(
                template_filepath, "rb"
            ) as template_file:
                self.assertEqual(
                    test_file.read().decode("utf-8").replace("\r\n", "\n"),
                    template_file.read().decode("utf-8").replace("\r\n", "\n"),
                )

    class GetStringsTest(unittest.TestCase):
        def setUp(self):
            self.data: str | None = None
            self.extension: str | None = None

        def test_valid_file_without_printing_comments(self):
            # Create a temporary file with valid data
            with NamedTemporaryFile(
                suffix=self.extension, mode="w", delete=False, encoding="utf-8"
            ) as f:
                f.writelines(self.data)
                filepath = Path(f.name)

            # fmt: off
            expected_output = [
                ("hindi", "मेरे ऐप का आनंद लें"),
                ("korean", "내 앱을 즐기세요")
            ]
            # fmt: on

            # Call the function and check the output
            self.assertEqual(
                expected_output,
                get_strings(filepath, with_comments=False),
            )

            # Remove the temporary file
            filepath.unlink()

        def test_valid_localizable_file_printing_comments(self):
            # Create a temporary file with valid data
            with NamedTemporaryFile(
                suffix=self.extension, mode="w", delete=False, encoding="utf-8"
            ) as f:
                f.writelines(self.data)
                filepath = Path(f.name)

            # fmt: off
            expected_output = [
                ("chinese", "  欢迎来到我的申请  "),
                ("escaped_quote", "MyA\\\"pp"),
                ("hindi", "मेरे ऐप का आनंद लें"),
                ("korean", "내 앱을 즐기세요")
            ]
            # fmt: on

            # Call the function and check the output
            self.assertEqual(
                expected_output,
                get_strings(filepath, with_comments=True),
            )

            # Remove the temporary file
            filepath.unlink()

        def test_invalid_file(self):
            # Create a temporary file with invalid XML data
            data = """
            <?xml version="1.0" encoding="UTF-8"?>
            <bookstore>
              <book category="fiction">
                <title>The Great Gatsby</title>
                <author>F. Scott Fitzgerald</author>
                <year>1925</year>
                <price>10.99</price>
              </book>
              <book category="non-fiction">
                <title>The Elements of Style</title>
                <author>William Strunk Jr.</author>
                <author>E. B. White</author>
                <year>1918</year>
                <price>9.99</price>
              </book>
            </bookstore>
            'comment' = 'comment';
            comment" = "comment;
            """
            with NamedTemporaryFile(
                suffix=self.extension, mode="w", delete=False, encoding="utf-8"
            ) as f:
                f.write(data)
                filepath = Path(f.name)

            # Call the function and check that it raises a ValueError
            with self.assertRaises(ValueError):
                get_strings(filepath, with_comments=True)

            # Clean up the temporary file
            filepath.unlink()

        def test_commented_file(self):
            # Create a temporary file with invalid XML data
            data = """
            <!--<string name="app_name">MyApp</string>-->
            <!--    <string name="1">MyA\\\"pp</string>  -->
            //  "hi" = "hi";
                //      "bye" = "bye";
            //"No" = "No";
            """
            with NamedTemporaryFile(
                suffix=self.extension, mode="w", delete=False, encoding="utf-8"
            ) as f:
                f.write(data)
                filepath = Path(f.name)

            # Call the function and check that it raises a ValueError
            with self.assertRaises(ValueError):
                get_strings(filepath, with_comments=False)

            # Clean up the temporary file
            filepath.unlink()
