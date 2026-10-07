import unittest
import warnings
from dataclasses import replace

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    SUPPORTED_FILE_TYPES,
    Catalog,
    Entry,
    parse,
    serialize,
)
from mobile_strings_converter.formats import is_multi_locale

MULTI_LOCALE_CATALOG = Catalog(
    [
        Entry(
            "hello",
            {DEFAULT_LOCALE: "Hello", "es": "Hola", "fr": "Bonjour"},
            comment="Greeting on the home screen",
        ),
        # Not translated to French
        Entry("bye", {DEFAULT_LOCALE: "Bye", "es": "Adiós"}),
    ]
)

SINGLE_LOCALE_CATALOG = Catalog(
    [
        Entry("app_name", {DEFAULT_LOCALE: "My App"}, translatable=False),
        Entry("hello", {DEFAULT_LOCALE: "Hello"}, comment="Greeting"),
    ]
)


def _without_comments(catalog: Catalog) -> Catalog:
    return Catalog([replace(entry, comment=None) for entry in catalog.entries])


class TestMultiLocaleRoundTrip(unittest.TestCase):
    """Every file type that can hold several locales must keep all of them."""

    def test_round_trip(self):
        for file_type in SUPPORTED_FILE_TYPES:
            if not is_multi_locale(file_type):
                continue

            with self.subTest(file_type=file_type), warnings.catch_warnings():
                warnings.simplefilter("ignore")
                catalog = parse(serialize(MULTI_LOCALE_CATALOG, file_type), file_type)

            expected = MULTI_LOCALE_CATALOG
            if file_type == ".yaml":
                # YAML files don't hold comments
                expected = _without_comments(expected)

            self.assertEqual(expected, catalog)

    def test_single_locale_file_types_reject_several_locales(self):
        for file_type in [".xml", ".strings"]:
            with self.subTest(file_type=file_type), self.assertRaises(ValueError):
                serialize(MULTI_LOCALE_CATALOG, file_type)

    def test_csv_columns(self):
        csv = serialize(MULTI_LOCALE_CATALOG, "csv").decode("utf-8").splitlines()

        self.assertEqual("name,value,es,fr,comment", csv[0])
        self.assertEqual("hello,Hello,Hola,Bonjour,Greeting on the home screen", csv[1])
        self.assertEqual("bye,Bye,Adiós,,", csv[2])

    def test_for_locale_and_merge(self):
        catalogs = {
            locale: MULTI_LOCALE_CATALOG.for_locale(locale)
            for locale in MULTI_LOCALE_CATALOG.locales
        }

        self.assertEqual([DEFAULT_LOCALE, "es", "fr"], list(catalogs))
        self.assertEqual([("hello", "Bonjour")], catalogs["fr"].to_pairs())
        self.assertEqual(MULTI_LOCALE_CATALOG, Catalog.merge(catalogs.values()))


class TestAndroid(unittest.TestCase):
    def test_round_trip(self):
        data = serialize(SINGLE_LOCALE_CATALOG, ".xml")

        self.assertEqual(SINGLE_LOCALE_CATALOG, parse(data, ".xml"))

    def test_output(self):
        self.assertEqual(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<resources>\n"
            '\t<string name="app_name" translatable="false">My App</string>\n'
            "\t<!-- Greeting -->\n"
            '\t<string name="hello">Hello</string>\n'
            "</resources>\n",
            serialize(SINGLE_LOCALE_CATALOG, ".xml").decode("utf-8"),
        )

    def test_comment_with_double_hyphens(self):
        catalog = Catalog([Entry("a", {DEFAULT_LOCALE: "A"}, comment="a -- b---c")])

        self.assertIn(
            "<!-- a - - b- - -c -->", serialize(catalog, ".xml").decode("utf-8")
        )

    def test_comments(self):
        data = b"""<resources>
            <!-- Commented out: -->
            <!--<string name="old">Old</string>-->
            <string name="a">A</string> <!-- Trailing comment -->
            <string name="b">B</string>
            <!-- Note for C -->
            <string name="c">C</string>
        </resources>"""

        catalog = parse(data, ".xml")

        self.assertEqual(
            [None, None, "Note for C"], [entry.comment for entry in catalog.entries]
        )
        self.assertEqual(
            ["old", "a", "b", "c"],
            [entry.name for entry in parse(data, ".xml", with_comments=True).entries],
        )

    def test_locale(self):
        catalog = parse(
            b'<resources><string name="a">A</string></resources>', "xml", "es"
        )

        self.assertEqual(["es"], catalog.locales)


class TestIos(unittest.TestCase):
    def test_comments_round_trip(self):
        catalog = Catalog(
            [Entry("hello", {DEFAULT_LOCALE: "Hello"}, comment="Greeting */ here")]
        )

        data = serialize(catalog, ".strings")

        self.assertEqual(
            '/* Greeting * / here */\n"hello" = "Hello";\n', data.decode("utf-8")
        )
        self.assertEqual(
            "Greeting * / here", parse(data, ".strings").entries[0].comment
        )

    def test_trailing_comments_are_not_notes(self):
        catalog = parse(b'"a" = "A"; // Trailing\n"b" = "B";', ".strings")

        self.assertIsNone(catalog.entries[1].comment)


class TestTables(unittest.TestCase):
    def test_value_column_locale(self):
        catalog = parse(b"name,value,fr\nhello,Hola,Bonjour\n", ".csv", locale="es")

        self.assertEqual(["es", "fr"], catalog.locales)

    def test_html_without_header(self):
        data = b"<table><tr><td>hello</td><td>Hello</td></tr></table>"

        self.assertEqual([("hello", "Hello")], parse(data, ".html").to_pairs())


class TestYaml(unittest.TestCase):
    def test_multi_locale(self):
        data = "default:\n  hello: Hello\nes:\n  hello: Hola\n".encode("utf-8")

        self.assertEqual(
            {DEFAULT_LOCALE: "Hello", "es": "Hola"},
            parse(data, ".yaml").entries[0].values,
        )


class TestUnsupportedFileType(unittest.TestCase):
    def test_parse(self):
        with self.assertRaises(ValueError):
            parse(b"", ".txt")

    def test_serialize(self):
        with self.assertRaises(ValueError):
            serialize(SINGLE_LOCALE_CATALOG, "txt")


if __name__ == "__main__":
    unittest.main()
