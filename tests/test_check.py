import unittest

from mobile_strings_converter import (
    DEFAULT_LOCALE,
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
