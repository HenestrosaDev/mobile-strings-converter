"""
Reading and writing files, and getting the locale of the files of Android and iOS
projects (e.g. `values-pt-rBR/strings.xml` or `pt-BR.lproj/Localizable.strings`).
"""

import re
import warnings
from pathlib import Path
from typing import Optional

from .exceptions import UnsupportedCharactersWarning
from .formats import SUPPORTED_FILE_TYPES, normalize_file_type, parse, serialize
from .model import DEFAULT_LOCALE, Catalog


def load(
    filepath: Path, locale: Optional[str] = None, with_comments: bool = False
) -> Catalog:
    """
    Reads the strings of a file.

    :param filepath: File to read
    :type filepath: Path
    :param locale: Locale of the strings. If None, it's taken from the directory of the
        file (see `locale_from_path`).
    :type locale: Optional[str]
    :param with_comments: True to read the commented out strings of `.xml` and
        `.strings` files as well
    :type with_comments: bool
    :return: The strings of the file
    :rtype: Catalog
    """

    filepath = Path(filepath)
    if normalize_file_type(filepath.suffix) not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Input file type not supported: {filepath}")

    if locale is None:
        locale = locale_from_path(filepath)

    return parse(filepath.read_bytes(), filepath.suffix, locale, with_comments)


def save(catalog: Catalog, filepath: Path):
    """
    Writes the strings to a file, creating its directory if needed.

    If some strings can't be rendered in a PDF, they are listed in a
    `[FILE_NAME]-errors.txt` file next to it.

    :param catalog: Strings to write
    :type catalog: Catalog
    :param filepath: File to write. Its extension sets the file type.
    :type filepath: Path
    """

    filepath = Path(filepath)

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        data = serialize(catalog, filepath.suffix)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_bytes(data)

    # Emit the warnings again once the file is written
    for caught in caught_warnings:
        warning = caught.message
        if isinstance(warning, UnsupportedCharactersWarning):
            errors_filepath = filepath.parent / f"{filepath.stem}-errors.txt"
            errors_filepath.write_text(
                "".join(f"{value} not supported\n" for value in warning.values),
                encoding="utf-8",
            )
            warning = UnsupportedCharactersWarning(warning.values)
            warning.args = (f"{warning.args[0]} See {errors_filepath}",)

        warnings.warn(warning, stacklevel=2)


def locale_from_path(filepath: Path) -> str:
    """
    Returns the locale of a file from the name of its directory:

    - Android: `values` -> `default`, `values-es` -> `es`, `values-pt-rBR` -> `pt-BR`
      and `values-b+sr+Latn` -> `sr-Latn`.
    - iOS: `Base.lproj` -> `default` and `pt-BR.lproj` -> `pt-BR`.

    Any other directory is the default locale.

    :param filepath: Path of the file
    :type filepath: Path
    :return: The locale of the file
    :rtype: str
    """

    directory = Path(filepath).parent.name

    android_match = re.fullmatch(r"values(?:-(?P<qualifiers>.+))?", directory)
    if android_match:
        return _locale_from_android_qualifiers(android_match.group("qualifiers"))

    ios_match = re.fullmatch(r"(?P<locale>.+)\.lproj", directory)
    if ios_match and ios_match.group("locale") != "Base":
        return ios_match.group("locale")

    return DEFAULT_LOCALE


def _locale_from_android_qualifiers(qualifiers: Optional[str]) -> str:
    if not qualifiers:
        return DEFAULT_LOCALE

    # BCP 47 tags, e.g. `b+sr+Latn` or `b+es+419`
    if qualifiers.startswith("b+"):
        return "-".join(qualifiers.split("-")[0][2:].split("+"))

    # The language is the first qualifier, optionally followed by the region (e.g.
    # `rBR`). Other qualifiers, such as `night` or `v21`, are ignored.
    parts = qualifiers.split("-")
    if not re.fullmatch(r"[a-z]{2,3}", parts[0]):
        return DEFAULT_LOCALE

    if len(parts) > 1 and re.fullmatch(r"r[A-Z]{2}", parts[1]):
        return f"{parts[0]}-{parts[1][1:]}"

    return parts[0]
