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

        # The source language is the default locale
        self.assertEqual(
            Catalog(
                [
                    Entry(
                        "Hello, world!",
                        {DEFAULT_LOCALE: "Hello, world!", "es": "¡Hola, mundo!"},
                    ),
                    Entry(
                        "songs",
                        {DEFAULT_LOCALE: {"one": "%lld song", "other": "%lld songs"}},
                        comment="Number of songs",
                    ),
                    Entry("Songbook", {DEFAULT_LOCALE: "Songbook"}, translatable=False),
                    # Device variations are not supported
                    Entry("Tap here", {}),
                ]
            ),
            catalog,
        )

    def test_round_trip(self):
        catalog = Catalog(
            [
                Entry(
                    "hello", {DEFAULT_LOCALE: "Hello", "es": "Hola"}, comment="Greeting"
                ),
                Entry(
                    "songs",
                    {
                        DEFAULT_LOCALE: SONGS,
                        "es": {"one": "%d canción", "other": "%d canciones"},
                    },
                ),
                Entry("app_name", {DEFAULT_LOCALE: "Songbook"}, translatable=False),
            ]
        )

        data = serialize(catalog, ".xcstrings", source_language="en")

        self.assertEqual(catalog, parse(data, ".xcstrings"))

    def test_default_locale_is_written_as_the_source_language(self):
        catalog = Catalog(
            [Entry("hello", {DEFAULT_LOCALE: "Hello %s", "es": "Hola %s"})]
        )

        catalog_data = json.loads(
            serialize(catalog, ".xcstrings", source_language="fr")
        )

        self.assertEqual("fr", catalog_data["sourceLanguage"])
        self.assertEqual(
            {
                "extractionState": "manual",
                "localizations": {
                    "fr": {"stringUnit": {"state": "translated", "value": "Hello %@"}},
                    "es": {"stringUnit": {"state": "translated", "value": "Hola %@"}},
                },
            },
            catalog_data["strings"]["hello"],
        )

    def test_source_language_is_required(self):
        catalog = Catalog([Entry("hello", {DEFAULT_LOCALE: "Hello"})])

        with self.assertRaisesRegex(ValueError, "--source-language"):
            serialize(catalog, ".xcstrings")

    def test_source_language_with_its_own_strings(self):
        catalog = Catalog([Entry("hello", {DEFAULT_LOCALE: "Hi", "en": "Hello"})])

        with self.assertRaisesRegex(ValueError, "already has its own strings"):
            serialize(catalog, ".xcstrings", source_language="en")

    def test_strings_without_default_locale(self):
        # e.g. merged from `en.lproj` and `es.lproj`
        catalog = Catalog([Entry("hello", {"en": "Hello", "es": "Hola"})])

        data = serialize(catalog, ".xcstrings", source_language="en")

        self.assertEqual(
            {DEFAULT_LOCALE: "Hello", "es": "Hola"},
            parse(data, ".xcstrings").entries[0].values,
        )

    def test_default_locale_goes_first(self):
        data = json.dumps(
            {
                "sourceLanguage": "en",
                "strings": {
                    "hello": {
                        "localizations": {
                            "de": {"stringUnit": {"value": "Hallo"}},
                            "en": {"stringUnit": {"value": "Hello"}},
                        }
                    }
                },
            }
        ).encode()

        self.assertEqual([DEFAULT_LOCALE, "de"], parse(data, ".xcstrings").locales)

    def test_arrays_are_skipped(self):
        catalog = Catalog(
            [Entry("planets", {DEFAULT_LOCALE: ["Mercury"], "es": ["Mercurio"]})]
        )

        with self.assertWarns(ConversionWarning) as context:
            serialize(catalog, ".xcstrings", source_language="en")

        self.assertIn("1 array(s)", str(context.warning))

    def test_xcode_format(self):
        catalog = Catalog([Entry("hello", {DEFAULT_LOCALE: "Hello"})])

        self.assertTrue(
            serialize(catalog, ".xcstrings", source_language="en")
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
        for data in [
            b"[]",
            b"{}",
            b'{"strings": []}',
            b'{"strings": {}}',
            b"not json",
        ]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                parse(data, ".xcstrings")


if __name__ == "__main__":
    unittest.main()
