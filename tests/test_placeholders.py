import unittest

from mobile_strings_converter import DEFAULT_LOCALE, Catalog, Entry, parse, serialize
from mobile_strings_converter.placeholders import to_android, to_ios


class TestPlaceholders(unittest.TestCase):
    def test_to_ios(self):
        cases = {
            "Hello %s": "Hello %@",
            "%1$s has %2$d songs": "%1$@ has %2$d songs",
            "%S": "%@",
            "%-10s|": "%-10@|",
            "%.2f%%": "%.2f%%",
            "%d %x %c": "%d %x %c",
            "%%s is not a placeholder": "%%s is not a placeholder",
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(expected, to_ios(value))

    def test_to_android(self):
        cases = {
            "Hello %@": "Hello %s",
            "%1$@ has %2$ld songs": "%1$s has %2$d songs",
            "%lld %llu %u %i %D": "%d %d %d %d %d",
            "%.2lf": "%.2f",
            "100%% done": "100%% done",
            "%%@ is not a placeholder": "%%@ is not a placeholder",
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(expected, to_android(value))

    def test_text_with_percent_signs(self):
        for value in ["100% sure", "50% of 10", "% off"]:
            with self.subTest(value=value):
                self.assertEqual(value, to_ios(value))
                self.assertEqual(value, to_android(value))

    def test_round_trip(self):
        value = "%1$s has %2$d songs and %3$.1f%% left"

        self.assertEqual(value, to_android(to_ios(value)))


class TestPlaceholdersInFiles(unittest.TestCase):
    def test_android_to_ios(self):
        catalog = parse(
            b'<resources><string name="greeting">Hello %1$s</string></resources>',
            ".xml",
        )

        self.assertEqual(
            '"greeting" = "Hello %1$@";\n', serialize(catalog, ".strings").decode()
        )

    def test_ios_to_android(self):
        catalog = parse(b'"greeting" = "Hello %@, you have %ld songs";', ".strings")

        self.assertIn(
            '<string name="greeting">Hello %s, you have %d songs</string>',
            serialize(catalog, ".xml").decode(),
        )

    def test_other_file_types_keep_the_placeholders(self):
        catalog = Catalog([Entry("greeting", {DEFAULT_LOCALE: "Hello %@"})])

        self.assertIn("Hello %@", serialize(catalog, ".json").decode())


if __name__ == "__main__":
    unittest.main()
