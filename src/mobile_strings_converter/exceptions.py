class ConversionWarning(UserWarning):
    """Some data of the input could not be converted to the output file type."""


class UnsupportedCharactersWarning(ConversionWarning):
    """Some strings have characters that no bundled font can render in a PDF."""

    def __init__(self, values: list[str]):
        self.values = values
        super().__init__(f"{len(values)} string(s) could not be rendered in the PDF.")
