import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from mobile_strings_converter.converter import get_strings


class TestGetStringsAndroid(unittest.TestCase):
    def setUp(self):
        self.data = """
        <?xml version="1.0" encoding="UTF-8"?>
        <resources>
            <!--<string name="chinese">  欢迎来到我的申请  </string>-->
            <!--    <string name="escaped_quote">MyA\\\"pp</string>  -->
            <string name="hindi">मेरे ऐप का आनंद लें</string>
                    <string name="korean">내 앱을 즐기세요</string>
            "3" = "3";
        </resources>
        """
        self.extension = ".xml"

    def test_valid_localizable_file_without_printing_comments(self):
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
            get_strings(filepath, should_print_comments=False),
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
            get_strings(filepath, should_print_comments=True),
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
            localizable_filepath = Path(f.name)

        # Call the function and check that it raises a ValueError
        with self.assertRaises(ValueError):
            get_strings(localizable_filepath, should_print_comments=True)

        # Clean up the temporary file
        localizable_filepath.unlink()

    def test_commented_localizable_file(self):
        # Create a temporary file with invalid XML data
        data = """
        <!--<string name="app_name">MyApp</string>-->
        <!--    <string name="1">MyA\\\"pp</string>  -->
        """
        with NamedTemporaryFile(
            suffix=self.extension, mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write(data)
            localizable_filepath = Path(f.name)

        # Call the function and check that it raises a ValueError
        with self.assertRaises(ValueError):
            get_strings(localizable_filepath, should_print_comments=False)

        # Clean up the temporary file
        localizable_filepath.unlink()


if __name__ == "__main__":
    unittest.main()
