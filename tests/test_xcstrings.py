import json
import unittest

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    Catalog,
    ConversionWarning,
    Entry,
    parse,
    serialize,
)

SONGS = {"one": "%d song", "other": "%d songs"}


XCODE_CATALOG = {
    "sourceLanguage": "en",
    "strings": {
        # Xcode leaves out the source language when the value is the key
        "Hello, world!": {
            "localizations": {
                "es": {"stringUnit": {"state": "translated", "value": "¡Hola, mundo!"}}
            }
        },
        "songs": {
            "comment": "Number of songs",
            "localizations": {
                "en": {
                    "variations": {
                        "plural": {
                            "one": {
                                "stringUnit": {
                                    "state": "translated",
                                    "value": "%lld song",
                                }
                            },
                            "other": {
                                "stringUnit": {
                                    "state": "translated",
                                    "value": "%lld songs",
                                }
                            },
                        }
                    }
                }
            },
        },
        "Songbook": {"shouldTranslate": False},
        "Tap here": {
            "localizations": {
                "en": {
                    "variations": {
                        "device": {
                            "mac": {
                                "stringUnit": {
                                    "state": "translated",
                                    "value": "Click here",
                                }
                            }
                        }
                    }
                }
            }
        },
    },
    "version": "1.0",
}


class TestXcstrings(unittest.TestCase):
    def test_parse_xcode_file(self):
        with self.assertWarns(ConversionWarning):
            catalog = parse(json.dumps(XCODE_CATALOG).encode(), ".xcstrings")

        self.assertEqual(
            Catalog(
                [
                    Entry(
                        "Hello, world!", {"en": "Hello, world!", "es": "¡Hola, mundo!"}
                    ),
                    Entry(
                        "songs",
                        {"en": {"one": "%lld song", "other": "%lld songs"}},
                        comment="Number of songs",
                    ),
                    Entry("Songbook", {"en": "Songbook"}, translatable=False),
                    # Device variations are not supported
                    Entry("Tap here", {}),
                ]
            ),
            catalog,
        )

    def test_round_trip(self):
        catalog = Catalog(
            [
                Entry("hello", {"en": "Hello", "es": "Hola"}, comment="Greeting"),
                Entry(
                    "songs",
                    {"en": SONGS, "es": {"one": "%d canción", "other": "%d canciones"}},
                ),
                Entry("app_name", {"en": "Songbook"}, translatable=False),
            ]
        )

        self.assertEqual(catalog, parse(serialize(catalog, ".xcstrings"), ".xcstrings"))

    def test_default_locale_is_the_source_language(self):
        catalog = Catalog(
            [Entry("hello", {DEFAULT_LOCALE: "Hello %s", "es": "Hola %s"})]
        )

        catalog_data = json.loads(serialize(catalog, ".xcstrings"))

        self.assertEqual("en", catalog_data["sourceLanguage"])
        self.assertEqual(
            {
                "extractionState": "manual",
                "localizations": {
                    "en": {"stringUnit": {"state": "translated", "value": "Hello %@"}},
                    "es": {"stringUnit": {"state": "translated", "value": "Hola %@"}},
                },
            },
            catalog_data["strings"]["hello"],
        )

    def test_default_locale_with_source_language(self):
        catalog = Catalog([Entry("hello", {DEFAULT_LOCALE: "Hi", "en": "Hello"})])

        with self.assertWarns(ConversionWarning):
            data = serialize(catalog, ".xcstrings")

        self.assertEqual({"en": "Hello"}, parse(data, ".xcstrings").entries[0].values)

    def test_arrays_are_skipped(self):
        catalog = Catalog([Entry("planets", {"en": ["Mercury"], "es": ["Mercurio"]})])

        with self.assertWarns(ConversionWarning) as context:
            serialize(catalog, ".xcstrings")

        self.assertIn("1 array(s)", str(context.warning))

    def test_xcode_format(self):
        catalog = Catalog([Entry("hello", {"en": "Hello"})])

        self.assertTrue(
            serialize(catalog, ".xcstrings")
            .decode()
            .startswith(
                "{\n"
                '  "sourceLanguage" : "en",\n'
                '  "strings" : {\n'
                '    "hello" : {\n'
                '      "extractionState" : "manual",\n'
            )
        )

    def test_invalid_file(self):
        for data in [b"[]", b"{}", b'{"strings": []}', b"not json"]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                parse(data, ".xcstrings")


if __name__ == "__main__":
    unittest.main()
