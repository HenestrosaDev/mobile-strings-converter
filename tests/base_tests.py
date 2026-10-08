import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from mobile_strings_converter.converter import convert_strings, get_strings

FILES_PATH = Path(__file__).parent / "files"


# This is a wrapper class that prevents its nested classes from running as tests.
class BaseTests:
    class OutputDirTest(unittest.TestCase):
        """Writes the generated files to a temporary directory."""

        def setUp(self):
            self._temp_dir = TemporaryDirectory()
            self.output_dir = Path(self._temp_dir.name)

        def tearDown(self):
            self._temp_dir.cleanup()

        def _assert_same_content(
            self, output_filepath: Path, template_filepath: Path
        ) -> None:
            """
            Checks that both files have the same content. Binary file types override
            this method.
            """

            with (
                open(output_filepath, "rb") as test_file,
                open(template_filepath, "rb") as template_file,
            ):
                self.assertEqual(
                    test_file.read().decode("utf-8").replace("\r\n", "\n"),
                    template_file.read().decode("utf-8").replace("\r\n", "\n"),
                )

    # For converting Android & iOS files to each supported file type

    class ConvertToTest(OutputDirTest):
        # Hook methods

        def setUp(self):
            super().setUp()
            self._file_name: str | None = None

            self.input_filepath_android = FILES_PATH / "input/strings.xml"
            self.input_filepath_ios = FILES_PATH / "input/Localizable.strings"

        # Properties

        @property
        def file_name(self):
            return self._file_name

        @file_name.setter
        def file_name(self, value):
            self._file_name = value
            self.template_with_comments_filepath: Path = (
                FILES_PATH / f"template-with-comments/{self._file_name}"
            )
            self.template_without_comments_filepath: Path = (
                FILES_PATH / f"template-without-comments/{self._file_name}"
            )
            self.output_filepath = self.output_dir / self._file_name

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
        ) -> None:
            convert_strings(input_filepath, self.output_filepath, with_comments)
            self.assertTrue(self.output_filepath.exists())

        def _converter_writes_correct_data(
            self,
            template_filepath: Path,
            input_filepath: Path,
            with_comments: bool,
        ) -> None:
            convert_strings(input_filepath, self.output_filepath, with_comments)
            self._assert_same_content(self.output_filepath, template_filepath)

    # For converting each supported file type to Android & iOS files

    class ConvertFromTest(OutputDirTest):
        # Hook methods

        def setUp(self):
            super().setUp()
            self._file_name: str | None = None

            self.template_android_filepath = (
                FILES_PATH / "template-without-comments/strings.xml"
            )
            self.template_ios_filepath = (
                FILES_PATH / "template-without-comments/Localizable.strings"
            )

        # Properties

        @property
        def file_name(self):
            return self._file_name

        @file_name.setter
        def file_name(self, value):
            self.input_filepath = FILES_PATH / f"template-without-comments/{value}"
            self._file_name = value

        # Test methods

        # ------------ ANDROID ------------

        def test_converter_creates_file_android(self):
            self._converter_creates_file(self.output_dir / "strings.xml")

        def test_converter_writes_correct_data_android(self):
            self._converter_writes_correct_data(
                template_filepath=self.template_android_filepath,
                output_filepath=self.output_dir / "strings.xml",
            )

        # -------------- iOS --------------

        def test_converter_creates_file_ios(self):
            self._converter_creates_file(self.output_dir / "Localizable.strings")

        def test_converter_writes_correct_data_ios(self):
            self._converter_writes_correct_data(
                template_filepath=self.template_ios_filepath,
                output_filepath=self.output_dir / "Localizable.strings",
            )

        # Private methods

        def _converter_creates_file(self, output_filepath: Path) -> None:
            convert_strings(self.input_filepath, output_filepath)
            self.assertTrue(output_filepath.exists())

        def _converter_writes_correct_data(
            self,
            template_filepath: Path,
            output_filepath: Path,
        ) -> None:
            convert_strings(self.input_filepath, output_filepath)
            self._assert_same_content(output_filepath, template_filepath)

    class GetStringsTest(unittest.TestCase):
        def setUp(self):
            self.data: str = ""
            self.extension: str = ""

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
                ("escaped_quote", 'MyA"pp'),
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


class SameStringsMixin(unittest.TestCase):
    """For binary file types, whose content is compared by the strings they hold."""

    def _assert_same_content(
        self, output_filepath: Path, template_filepath: Path
    ) -> None:
        self.assertEqual(get_strings(output_filepath), get_strings(template_filepath))
