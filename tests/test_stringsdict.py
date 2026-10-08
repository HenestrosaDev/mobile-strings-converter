import plistlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    Catalog,
    ConversionWarning,
    Entry,
    parse,
    save_split,
    serialize,
)

SONGS = {"one": "%d song", "other": "%d songs"}


class TestStringsdict(unittest.TestCase):
    def test_round_trip(self):
        catalog = Catalog(
            [
                Entry("songs", {DEFAULT_LOCALE: SONGS}),
                Entry("planets", {DEFAULT_LOCALE: {"other": "Planets"}}),
            ]
        )

        self.assertEqual(
            catalog, parse(serialize(catalog, ".stringsdict"), ".stringsdict")
        )

    def test_output(self):
        catalog = Catalog(
            [Entry("songs", {DEFAULT_LOCALE: {"one": "%s song", "other": "%ld songs"}})]
        )

        plist = plistlib.loads(serialize(catalog, ".stringsdict"))

        self.assertEqual(
            {
                "songs": {
                    "NSStringLocalizedFormatKey": "%#@value@",
                    "value": {
                        "NSStringFormatSpecTypeKey": "NSStringPluralRuleType",
                        "NSStringFormatValueTypeKey": "ld",
                        "one": "%@ song",
                        "other": "%ld songs",
                    },
                }
            },
            plist,
        )

    def test_strings_and_arrays_are_skipped(self):
        catalog = Catalog(
            [
                Entry("hello", {DEFAULT_LOCALE: "Hello"}),
                Entry("planets", {DEFAULT_LOCALE: ["Mercury"]}),
                Entry("songs", {DEFAULT_LOCALE: SONGS}),
            ]
        )

        with self.assertWarns(ConversionWarning):
            data = serialize(catalog, ".stringsdict")

        self.assertEqual(["songs"], list(plistlib.loads(data)))

    def test_parse_xcode_file(self):
        data = plistlib.dumps(
            {
                "songs": {
                    "NSStringLocalizedFormatKey": "%#@count@",
                    "count": {
                        "NSStringFormatSpecTypeKey": "NSStringPluralRuleType",
                        "NSStringFormatValueTypeKey": "lld",
                        "other": "%lld songs",
                        "one": "%lld song",
                        "zero": "No songs",
                    },
                },
                # Several variables can't be represented
                "files": {
                    "NSStringLocalizedFormatKey": "%#@files@ in %#@folders@",
                    "files": {"NSStringFormatSpecTypeKey": "NSStringPluralRuleType"},
                },
            }
        )

        with self.assertWarns(ConversionWarning):
            catalog = parse(data, ".stringsdict", locale="es")

        self.assertEqual(
            Catalog(
                [
                    Entry(
                        "songs",
                        {
                            "es": {
                                "zero": "No songs",
                                "one": "%lld song",
                                "other": "%lld songs",
                            }
                        },
                    )
                ]
            ),
            catalog,
        )

    def test_invalid_file(self):
        with self.assertRaises(ValueError):
            parse(b"not a plist", ".stringsdict")

    def test_split(self):
        catalog = Catalog([Entry("songs", {DEFAULT_LOCALE: SONGS, "es": SONGS})])

        with TemporaryDirectory() as temp_dir:
            filepaths = save_split(catalog, Path(temp_dir), "stringsdict")

            self.assertEqual(
                {
                    DEFAULT_LOCALE: Path(temp_dir)
                    / "Base.lproj/Localizable.stringsdict",
                    "es": Path(temp_dir) / "es.lproj/Localizable.stringsdict",
                },
                filepaths,
            )


if __name__ == "__main__":
    unittest.main()
