"""
Reading and writing files, and mapping locales to the paths of Android and iOS
projects (e.g. `values-pt-rBR/strings.xml` or `pt-BR.lproj/Localizable.strings`).
"""

import re
import warnings
from pathlib import Path

from .exceptions import UnsupportedCharactersWarning
from .formats import INPUT_FILE_TYPES, normalize_file_type, parse, serialize
from .model import DEFAULT_LOCALE, Catalog

ANDROID_FILENAME = "strings.xml"
IOS_FILENAME = "Localizable"


def load(
    filepath: Path, locale: str | None = None, with_comments: bool = False
) -> Catalog:
    """
    Reads the strings of a file.

    :param filepath: File to read
    :type filepath: Path
    :param locale: Locale of the strings. If None, it's taken from the directory of the
        file (see `locale_from_path`).
    :type locale: str | None
    :param with_comments: True to read the commented out strings of `.xml` and
        `.strings` files as well
    :type with_comments: bool
    :return: The strings of the file
    :rtype: Catalog
    """

    filepath = Path(filepath)
    if normalize_file_type(filepath.suffix) not in INPUT_FILE_TYPES:
        raise ValueError(f"Input file type not supported: {filepath}")

    if locale is None:
        locale = locale_from_path(filepath)

    return parse(filepath.read_bytes(), filepath.suffix, locale, with_comments)


def save(catalog: Catalog, filepath: Path, source_language: str | None = None) -> None:
    """
    Writes the strings to a file, creating its directory if needed.

    If some strings can't be rendered in a PDF, they are listed in a
    `[FILE_NAME]-errors.txt` file next to it.

    :param catalog: Strings to write
    :type catalog: Catalog
    :param filepath: File to write. Its extension sets the file type.
    :type filepath: Path
    :param source_language: Code of the language of the default strings (e.g. `en`).
        Required by `.xcstrings` files, and ignored by any other file type.
    :type source_language: str | None
    """

    filepath = Path(filepath)

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        data = serialize(catalog, filepath.suffix, source_language)

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


def save_split(catalog: Catalog, directory: Path, file_type: str) -> dict[str, Path]:
    """
    Writes a file per locale to the directory, following the layout of the file type
    (see `localized_path`).

    :param catalog: Strings to write
    :type catalog: Catalog
    :param directory: Directory to write the files to
    :type directory: Path
    :param file_type: Extension of the files, e.g. `.xml` or `xml`
    :type file_type: str
    :return: The path of the file of each locale
    :rtype: dict[str, Path]
    """

    filepaths = {}
    for locale, locale_catalog in catalog.split().items():
        filepaths[locale] = localized_path(directory, locale, file_type)
        save(locale_catalog, filepaths[locale])

    return filepaths


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


def localized_path(directory: Path, locale: str, file_type: str) -> Path:
    """
    Returns the path of the file of a locale inside a directory:

    - `.xml`: `values/strings.xml`, `values-es/strings.xml`, `values-pt-rBR/strings.xml`
    - `.strings`: `Base.lproj/Localizable.strings`, `es.lproj/Localizable.strings`
    - `.stringsdict`: `Base.lproj/Localizable.stringsdict`,
      `es.lproj/Localizable.stringsdict`
    - Any other file type: `default.json`, `es.json`, `pt-BR.json`

    :param directory: Directory of the files
    :type directory: Path
    :param locale: Locale of the file
    :type locale: str
    :param file_type: Extension of the file, e.g. `.xml` or `xml`
    :type file_type: str
    :return: The path of the file
    :rtype: Path
    """

    directory = Path(directory)
    file_type = normalize_file_type(file_type)
    is_default = locale == DEFAULT_LOCALE

    if file_type == ".xml":
        values_dir = "values" if is_default else f"values-{_android_qualifier(locale)}"
        return directory / values_dir / ANDROID_FILENAME

    if file_type in (".strings", ".stringsdict"):
        lproj_dir = "Base.lproj" if is_default else f"{locale}.lproj"
        return directory / lproj_dir / f"{IOS_FILENAME}{file_type}"

    return directory / f"{locale}{file_type}"


def _locale_from_android_qualifiers(qualifiers: str | None) -> str:
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


def _android_qualifier(locale: str) -> str:
    parts = locale.split("-")

    if len(parts) == 1:
        return locale
    if len(parts) == 2 and re.fullmatch(r"[A-Za-z]{2}", parts[1]):
        return f"{parts[0]}-r{parts[1].upper()}"

    # Scripts (e.g. `sr-Latn`) and numeric regions (e.g. `es-419`) need BCP 47 tags
    return "b+" + "+".join(parts)
