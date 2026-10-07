import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from base_tests import BaseTests

from mobile_strings_converter.converter import get_strings


class TestGetStringsIos(BaseTests.GetStringsTest):
    def setUp(self):
        self.data = """
        //      "chinese" = "  欢迎来到我的申请  "   ;
            //"escaped_quote"="MyA\\\"pp";
        "hindi" = "मेरे ऐप का आनंद लें";
        "korean" = "내 앱을 즐기세요";
        """
        self.extension = ".strings"


class TestGetStringsAndroid(BaseTests.GetStringsTest):
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


class TestAndroidParsing(unittest.TestCase):
    def _get_strings(self, data: str, with_comments: bool = False):
        with NamedTemporaryFile(
            suffix=".xml", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write(data)
            filepath = Path(f.name)

        try:
            return get_strings(filepath, with_comments)
        finally:
            filepath.unlink()

    def test_attributes_multiline_and_unsupported_resources(self):
        data = """<?xml version="1.0" encoding="utf-8"?>
        <resources>
            <string name="app_name" translatable="false">My App</string>
            <string
                name="multiline">first\\nsecond</string>
            <string name="quoted">"It's quoted"</string>
            <plurals name="songs">
                <item quantity="one">%d song</item>
                <item quantity="other">%d songs</item>
            </plurals>
            <string-array name="planets">
                <item>Mercury</item>
            </string-array>
            <!-- Just a regular comment -->
        </resources>
        """

        self.assertEqual(
            [
                ("app_name", "My App"),
                ("multiline", "first\nsecond"),
                ("quoted", "It's quoted"),
            ],
            self._get_strings(data, with_comments=True),
        )


class TestIosParsing(unittest.TestCase):
    def _get_strings(self, data: str, with_comments: bool = False):
        with NamedTemporaryFile(
            suffix=".strings", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write(data)
            filepath = Path(f.name)

        try:
            return get_strings(filepath, with_comments)
        finally:
            filepath.unlink()

    def test_block_comments(self):
        data = """
        /* Title of the main screen */
        "title" = "Home";
        /* "old_title" = "Start"; */
        "url" = "https://example.com"; // Trailing comment
        "unicode" = "\\U00e9t\\u00e9";
        """

        self.assertEqual(
            [("title", "Home"), ("url", "https://example.com"), ("unicode", "été")],
            self._get_strings(data, with_comments=False),
        )
        self.assertEqual(
            [
                ("title", "Home"),
                ("old_title", "Start"),
                ("url", "https://example.com"),
                ("unicode", "été"),
            ],
            self._get_strings(data, with_comments=True),
        )


if __name__ == "__main__":
    unittest.main()
