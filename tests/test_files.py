import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    Catalog,
    load,
    locale_from_path,
    save,
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


class TestSaveAndLoad(unittest.TestCase):
    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self.output_dir = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_load_with_locale(self):
        filepath = self.output_dir / "values-es/strings.xml"
        save(Catalog.from_pairs([("hello", "Hello")]), filepath)

        self.assertEqual(["es"], load(filepath).locales)
        self.assertEqual(["fr"], load(filepath, locale="fr").locales)


if __name__ == "__main__":
    unittest.main()
