import unittest

from mobile_strings_converter import (
    DEFAULT_LOCALE,
    ISSUE_CODES,
    Catalog,
    Entry,
    Issue,
    check,
    find_duplicates,
)
from mobile_strings_converter.placeholders import signature


class TestCheck(unittest.TestCase):
    def _check(
        self, *entries: Entry, reference_locale: str | None = None
    ) -> list[Issue]:
        return check(Catalog(list(entries)), reference_locale)

    def test_no_issues(self):
        self.assertEqual(
            [],
            self._check(
                Entry("hello", {DEFAULT_LOCALE: "Hello, %s", "es": "Hola, %1$@"}),
                Entry("app_name", {DEFAULT_LOCALE: "App"}, translatable=False),
            ),
        )

    def test_missing_translation(self):
        self.assertEqual(
            [Issue("es", "bye", "missing translation", "missing")],
            self._check(
                Entry("hello", {DEFAULT_LOCALE: "Hello", "es": "Hola"}),
                Entry("bye", {DEFAULT_LOCALE: "Bye"}),
            ),
        )

    def test_obsolete_translation(self):
        self.assertEqual(
            [
                Issue(
                    "es",
                    "old",
                    "obsolete translation, as there is no default value",
                    "obsolete",
                )
            ],
            self._check(
                Entry("hello", {DEFAULT_LOCALE: "Hello", "es": "Hola"}),
                Entry("old", {"es": "Viejo"}),
            ),
        )

    def test_placeholders(self):
        [issue] = self._check(
            Entry("songs", {DEFAULT_LOCALE: "%1$s has %2$d", "es": "%1$s tiene %2$s"})
        )

        self.assertEqual(
            "has the placeholders %1$s %2$s, but the default value has %1$s %2$d",
            issue.message,
        )

    def test_reordered_placeholders(self):
        self.assertEqual(
            [],
            self._check(
                Entry("a", {DEFAULT_LOCALE: "%s has %d", "ja": "%2$ld %1$@"}),
            ),
        )

    def test_plurals_can_leave_out_the_number(self):
        self.assertEqual(
            [],
            self._check(
                Entry(
                    "songs",
                    {
                        DEFAULT_LOCALE: {"one": "%d song", "other": "%d songs"},
                        "es": {"one": "Una canción", "other": "%d canciones"},
                    },
                )
            ),
        )

    def test_kind(self):
        [issue] = self._check(
            Entry("songs", {DEFAULT_LOCALE: {"other": "%d songs"}, "es": "Canciones"})
        )

        self.assertEqual(
            "is a string, but the default value is a plural", issue.message
        )

    def test_array_size(self):
        [issue] = self._check(
            Entry("planets", {DEFAULT_LOCALE: ["A", "B"], "es": ["A"]})
        )

        self.assertEqual("has 1 items, but the default value has 2", issue.message)

    def test_array_placeholders(self):
        [issue] = self._check(
            Entry(
                "steps", {DEFAULT_LOCALE: ["Step %d", "Done"], "es": ["Paso", "Hecho"]}
            )
        )

        self.assertEqual(
            "item 0 has the placeholders none, but the default value has %1$d",
            issue.message,
        )

    def test_arrays_without_issues(self):
        self.assertEqual(
            [], self._check(Entry("planets", {DEFAULT_LOCALE: ["A"], "es": ["B"]}))
        )

    def test_empty_catalog(self):
        self.assertEqual([], self._check())

    def test_reference_locale(self):
        self.assertEqual(
            [Issue("fr", "bye", "missing translation", "missing")],
            self._check(
                Entry("hello", {"en": "Hello", "fr": "Bonjour"}),
                Entry("bye", {"en": "Bye"}),
                reference_locale="en",
            ),
        )

    def test_unknown_reference_locale(self):
        with self.assertRaisesRegex(ValueError, "default, es"):
            self._check(
                Entry("hello", {DEFAULT_LOCALE: "Hello", "es": "Hola"}),
                reference_locale="fr",
            )

    def test_empty_translation(self):
        self.assertEqual(
            [
                Issue(
                    "es",
                    "bye",
                    "is empty, but the default value is not",
                    "empty",
                ),
                Issue(
                    "es",
                    "songs",
                    "is empty, but the default value is not",
                    "empty",
                ),
            ],
            self._check(
                Entry("bye", {DEFAULT_LOCALE: "Bye", "es": ""}),
                Entry("blank", {DEFAULT_LOCALE: "", "es": ""}),
                Entry(
                    "app_name", {DEFAULT_LOCALE: "App", "es": ""}, translatable=False
                ),
                Entry(
                    "songs",
                    {
                        DEFAULT_LOCALE: {"one": "1 song", "other": "%d songs"},
                        "es": {"one": "", "other": ""},
                    },
                ),
                # Some quantities can be empty, as long as the plural is not
                Entry(
                    "files",
                    {
                        DEFAULT_LOCALE: {"one": "1 file", "other": "%d files"},
                        "es": {"one": "", "other": "%d archivos"},
                    },
                ),
            ),
        )

    def test_untranslated(self):
        entries = [
            Entry("settings", {DEFAULT_LOCALE: "Settings", "es": "Settings"}),
            Entry("count", {DEFAULT_LOCALE: "%1$d / %2$s", "es": "%1$d / %2$s"}),
            Entry("app", {DEFAULT_LOCALE: "App", "es": "App"}, translatable=False),
            Entry("hello", {DEFAULT_LOCALE: "Hello", "es": "Hola"}),
            Entry(
                "planets",
                {DEFAULT_LOCALE: ["Mars", "Venus"], "es": ["Mars", "Venus"]},
            ),
        ]

        self.assertEqual([], check(Catalog(entries)))
        self.assertEqual(
            [
                Issue(
                    "es",
                    "settings",
                    "is the same as the default value",
                    "untranslated",
                ),
                Issue(
                    "es",
                    "planets",
                    "is the same as the default value",
                    "untranslated",
                ),
            ],
            check(Catalog(entries), untranslated=True),
        )

    def test_codes(self):
        issues = self._check(
            Entry("bye", {DEFAULT_LOCALE: "Bye"}),
            Entry("old", {"es": "Viejo"}),
            Entry("hello", {DEFAULT_LOCALE: "Hello %s", "es": "Hola %d"}),
            Entry("songs", {DEFAULT_LOCALE: {"other": "Songs"}, "es": "Canciones"}),
            Entry("planets", {DEFAULT_LOCALE: ["A", "B"], "es": ["A"]}),
            Entry("title", {DEFAULT_LOCALE: "Title", "es": ""}),
        )

        self.assertEqual(
            ["missing", "obsolete", "placeholders", "kind", "kind", "empty"],
            [issue.code for issue in issues],
        )
        for issue in issues:
            self.assertIn(issue.code, ISSUE_CODES)

    def test_first_locale_is_the_reference_without_default_locale(self):
        self.assertEqual(
            [Issue("fr", "bye", "missing translation", "missing")],
            self._check(
                Entry("hello", {"en": "Hello", "fr": "Bonjour"}),
                Entry("bye", {"en": "Bye"}),
            ),
        )


class TestFindDuplicates(unittest.TestCase):
    def test_duplicates(self):
        catalog = Catalog(
            [
                Entry("a", {"es": "1"}),
                Entry("b", {"es": "2"}),
                Entry("a", {"es": "3"}),
            ]
        )

        self.assertEqual(
            [Issue("es", "a", "defined 2 times", "duplicate")], find_duplicates(catalog)
        )


class TestSignature(unittest.TestCase):
    def test_signature(self):
        self.assertEqual([(1, "s"), (2, "d")], signature("%s has %d"))
        self.assertEqual([(1, "s"), (2, "d")], signature("%2$ld %1$@"))
        self.assertEqual([(1, "f")], signature("%.2f%% done"))
        self.assertEqual([], signature("100% sure"))


if __name__ == "__main__":
    unittest.main()
