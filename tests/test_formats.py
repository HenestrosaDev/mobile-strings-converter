import codecs
import unittest
import warnings
from dataclasses import replace

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    SUPPORTED_FILE_TYPES,
    Catalog,
    ConversionWarning,
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
        Entry(
            "songs",
            {
                DEFAULT_LOCALE: {"one": "%d song", "other": "%d songs"},
                "es": {"one": "%d canción", "other": "%d canciones"},
            },
        ),
        Entry(
            "planets",
            {DEFAULT_LOCALE: ["Mercury", "Venus"], "es": ["Mercurio", "Venus"]},
        ),
        # Not translated to French
        Entry("bye", {DEFAULT_LOCALE: "Bye", "es": "Adiós"}),
    ]
)

SINGLE_LOCALE_CATALOG = Catalog(
    [
        Entry("app_name", {DEFAULT_LOCALE: "My App"}, translatable=False),
        Entry("hello", {DEFAULT_LOCALE: "Hello"}, comment="Greeting"),
        Entry("songs", {DEFAULT_LOCALE: {"one": "%d song", "other": "%d songs"}}),
        Entry("planets", {DEFAULT_LOCALE: ["Mercury", "Venus"]}),
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
        self.assertEqual("songs[one],%d song,%d canción,,", csv[2])
        self.assertEqual("bye,Bye,Adiós,,", csv[-1])

    def test_split(self):
        catalogs = MULTI_LOCALE_CATALOG.split()

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
            '\t<plurals name="songs">\n'
            '\t\t<item quantity="one">%d song</item>\n'
            '\t\t<item quantity="other">%d songs</item>\n'
            "\t</plurals>\n"
            '\t<string-array name="planets">\n'
            "\t\t<item>Mercury</item>\n"
            "\t\t<item>Venus</item>\n"
            "\t</string-array>\n"
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

    def test_plurals_and_arrays_are_skipped(self):
        with self.assertWarns(ConversionWarning):
            data = serialize(SINGLE_LOCALE_CATALOG, ".strings")

        self.assertEqual(
            [("app_name", "My App"), ("hello", "Hello")],
            parse(data, ".strings").to_pairs(),
        )

    def test_utf16(self):
        data = codecs.BOM_UTF16_LE + '"hello" = "Hola";'.encode("utf-16-le")

        self.assertEqual([("hello", "Hola")], parse(data, ".strings").to_pairs())


class TestTables(unittest.TestCase):
    def test_flattened_names_are_grouped(self):
        data = b"name,value\nsongs[one],1 song\nsongs[other],%d songs\nlist[1],B\n"

        self.assertEqual(
            Catalog(
                [
                    Entry(
                        "songs",
                        {DEFAULT_LOCALE: {"one": "1 song", "other": "%d songs"}},
                    ),
                    Entry("list", {DEFAULT_LOCALE: ["", "B"]}),
                ]
            ),
            parse(data, ".csv"),
        )

    def test_flattened_names_of_strings_are_kept(self):
        data = b"name,value\nitem,Item\nitem[0],First\n"

        self.assertEqual(
            [("item", "Item"), ("item[0]", "First")], parse(data, ".csv").to_pairs()
        )

    def test_value_column_locale(self):
        catalog = parse(b"name,value,fr\nhello,Hola,Bonjour\n", ".csv", locale="es")

        self.assertEqual(["es", "fr"], catalog.locales)

    def test_html_without_header(self):
        data = b"<table><tr><td>hello</td><td>Hello</td></tr></table>"

        self.assertEqual([("hello", "Hello")], parse(data, ".html").to_pairs())


class TestYaml(unittest.TestCase):
    def test_single_locale_with_plurals_only(self):
        data = b"songs:\n  one: '%d song'\n  other: '%d songs'\n"

        catalog = parse(data, ".yaml")

        self.assertEqual([DEFAULT_LOCALE], catalog.locales)
        self.assertEqual(
            {"one": "%d song", "other": "%d songs"},
            catalog.entries[0].values[DEFAULT_LOCALE],
        )

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
