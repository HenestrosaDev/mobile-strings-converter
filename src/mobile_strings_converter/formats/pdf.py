"""
PDF files with a table of the strings. See `table` for the columns.

PDF files can only be written, as they are meant to be read by people. Reading the
strings back from the text of a table is not reliable.
"""

import os
import unicodedata
import warnings
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from arabic_reshaper import reshape
from bidi.algorithm import get_display
from fpdf import FPDF
from fpdf.fonts import TTFFont

from ..exceptions import UnsupportedCharactersWarning
from ..model import Catalog
from . import table

FONTS_PATH = Path(__file__).parent.parent / "assets/fonts"

# Each cell is written with the first font that has glyphs for all its characters
FONTS = [
    "DejaVuSansCondensed",  # Latin, Greek, Cyrillic, Arabic, Hebrew, Armenian...
    "gargi",  # Devanagari
    "Aakar",  # Gujarati
    "AnekTelugu-VariableFont_wdth,wght",  # Telugu
    "Latha",  # Tamil
    "Gurvetica_a8_Heavy",  # Gurmukhi
    "Waree",  # Thai
    "fireflysung",  # Chinese and Japanese
    "Eunjin",  # Korean
]

FONT_SIZE = 12
PAGE_WIDTH = 190
CELL_HEIGHT = 10


def serialize(catalog: Catalog) -> bytes:
    header, *rows = table.to_table(catalog)

    pdf = FPDF(orientation="P", format="A4")
    pdf.add_page()

    cell_width = PAGE_WIDTH / len(header)

    # Add headers to table
    pdf.set_font("helvetica", "B", FONT_SIZE)
    for label in header:
        pdf.cell(cell_width, CELL_HEIGHT, label, border=1)
    pdf.ln()

    fonts = _FontPicker(pdf)
    # Used as an ordered set
    unsupported_values: dict[str, None] = {}

    # Add table data
    # https://stackoverflow.com/questions/53526311/fpdf-multicell-same-height
    for i, row in enumerate(rows):
        x = pdf.get_x()
        y = pdf.get_y()
        max_height = 0.0

        for j, value in enumerate(row):
            text = get_display(reshape(value)) if _is_rtl(value) else value

            if not fonts.use_best_font_for(text):
                unsupported_values[value] = None

            try:
                pdf.multi_cell(cell_width, CELL_HEIGHT, text)
            except Exception:
                unsupported_values[value] = None

            max_height = max(max_height, pdf.get_y() - y)
            pdf.set_xy(x + (cell_width * (j + 1)), y)

        for j in range(len(row) + 1):
            pdf.line(x + cell_width * j, y, x + cell_width * j, y + max_height)

        pdf.line(x, y, x + PAGE_WIDTH, y)
        pdf.line(x, y + max_height, x + PAGE_WIDTH, y + max_height)

        pdf.ln()

        if i < len(rows) - 1 and pdf.get_y() + (max_height * 2) > pdf.h - 10:
            pdf.add_page()

    # Inside this context manager, all output to stdout and stderr will be suppressed
    # This is done because in Windows, the following exception is raised if the
    # strings contain unsupported characters:
    #
    # UnicodeEncodeError: 'charmap'
    # codec can't encode characters in position 0-9: character maps to <undefined>
    with (
        open(os.devnull, "w") as devnull,
        redirect_stdout(devnull),
        redirect_stderr(devnull),
    ):
        output = bytes(pdf.output())

    if unsupported_values:
        warnings.warn(
            UnsupportedCharactersWarning(list(unsupported_values)), stacklevel=2
        )

    return output


def _is_rtl(text: str) -> bool:
    """Returns True if the text has right-to-left characters (e.g. Arabic)."""
    return any(unicodedata.bidirectional(char) in ("R", "AL") for char in text)


class _FontPicker:
    """Loads the fonts on demand and picks the one that can render a text."""

    def __init__(self, pdf: FPDF):
        self._pdf = pdf
        self._cmaps: dict[str, set[int]] = {}

    def use_best_font_for(self, text: str) -> bool:
        """
        Sets the first font that has glyphs for all the characters of the text, or the
        one that has the most if none has all of them. Returns True if the font has
        glyphs for all the characters.
        """

        code_points = {ord(char) for char in text if not char.isspace()}
        best_font, best_missing = None, None

        for font in FONTS:
            missing = len(code_points - self._get_cmap(font))
            if best_missing is None or missing < best_missing:
                best_font, best_missing = font, missing
            if missing == 0:
                break

        self._pdf.set_font(best_font, size=FONT_SIZE)
        return best_missing == 0

    def _get_cmap(self, font: str) -> set[int]:
        if font not in self._cmaps:
            self._pdf.add_font(fname=str(FONTS_PATH / f"{font}.ttf"))
            self._pdf.set_font(font, size=FONT_SIZE)
            current_font = self._pdf.current_font
            assert isinstance(current_font, TTFFont)
            self._cmaps[font] = set(current_font.cmap)

        return self._cmaps[font]
