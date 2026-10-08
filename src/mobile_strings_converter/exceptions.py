class NoStringsError(ValueError):
    """
    The file is valid, but has no strings, such as the layouts and `colors.xml` files of
    Android projects.
    """


class ConversionWarning(UserWarning):
    """Some data of the input could not be converted to the output file type."""


class UnsupportedCharactersWarning(ConversionWarning):
    """Some strings have characters that no bundled font can render in a PDF."""

    def __init__(self, values: list[str]):
        self.values = values
        super().__init__(f"{len(values)} string(s) could not be rendered in the PDF.")


class MissingDependencyError(ImportError):
    """A feature needs an optional dependency that is not installed."""

    def __init__(self, feature: str, extra: str):
        self.extra = extra
        super().__init__(
            f"{feature} needs optional dependencies. Install them with "
            f"`pip install 'mobile-strings-converter[{extra}]'`."
        )
