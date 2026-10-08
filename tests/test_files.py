import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    Catalog,
    Entry,
    load,
    locale_from_path,
    localized_path,
    save,
    save_split,
)


class TestLocales(unittest.TestCase):
    def test_locale_from_path(self):
        cases = {
            "res/values/strings.xml": DEFAULT_LOCALE,
            "res/values-es/strings.xml": "es",
            "res/values-pt-rBR/strings.xml": "pt-BR",
            "res/values-b+sr+Latn/strings.xml": "sr-Latn",
            "res/values-b+es+419/strings.xml": "es-419",
            "res/values-night/strings.xml": DEFAULT_LOCALE,
            "res/values-es-night/strings.xml": "es",
            "Base.lproj/Localizable.strings": DEFAULT_LOCALE,
            "pt-BR.lproj/Localizable.strings": "pt-BR",
            "translations/strings.xlsx": DEFAULT_LOCALE,
        }

        for path, locale in cases.items():
            with self.subTest(path=path):
                self.assertEqual(locale, locale_from_path(Path(path)))

    def test_localized_path(self):
        cases = {
            (DEFAULT_LOCALE, ".xml"): "res/values/strings.xml",
            ("es", ".xml"): "res/values-es/strings.xml",
            ("pt-BR", "xml"): "res/values-pt-rBR/strings.xml",
            ("sr-Latn", ".xml"): "res/values-b+sr+Latn/strings.xml",
            ("es-419", ".xml"): "res/values-b+es+419/strings.xml",
            (DEFAULT_LOCALE, ".strings"): "res/Base.lproj/Localizable.strings",
            ("pt-BR", ".strings"): "res/pt-BR.lproj/Localizable.strings",
            ("es", ".json"): "res/es.json",
        }

        for (locale, file_type), path in cases.items():
            with self.subTest(locale=locale, file_type=file_type):
                self.assertEqual(
                    Path(path), localized_path(Path("res"), locale, file_type)
                )
                if file_type in (".xml", "xml", ".strings"):
                    self.assertEqual(locale, locale_from_path(Path(path)))


class TestSaveAndLoad(unittest.TestCase):
    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self.output_dir = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_split_and_merge(self):
        catalog = Catalog(
            [
                Entry("hello", {DEFAULT_LOCALE: "Hello", "es": "Hola", "pt-BR": "Olá"}),
                Entry("bye", {DEFAULT_LOCALE: "Bye", "es": "Adiós"}),
            ]
        )

        filepaths = save_split(catalog, self.output_dir / "res", ".xml")

        self.assertEqual(
            {
                DEFAULT_LOCALE: self.output_dir / "res/values/strings.xml",
                "es": self.output_dir / "res/values-es/strings.xml",
                "pt-BR": self.output_dir / "res/values-pt-rBR/strings.xml",
            },
            filepaths,
        )
        self.assertEqual(
            catalog, Catalog.merge(load(filepath) for filepath in filepaths.values())
        )

    def test_load_with_locale(self):
        filepath = self.output_dir / "values-es/strings.xml"
        save(Catalog.from_pairs([("hello", "Hello")]), filepath)

        self.assertEqual(["es"], load(filepath).locales)
        self.assertEqual(["fr"], load(filepath, locale="fr").locales)


if __name__ == "__main__":
    unittest.main()
