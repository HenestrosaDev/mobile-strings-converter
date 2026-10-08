import argparse
import os
import re
import sys
import warnings
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path

from . import __version__
from .check import check, find_duplicates
from .console_style import ConsoleStyle
from .files import load, save, save_split
from .formats import (
    INPUT_FILE_TYPES,
    SUPPORTED_FILE_TYPES,
    is_multi_locale,
    normalize_file_type,
)
from .google_sheets import read_google_sheets, write_google_sheets
from .model import Catalog

# Suffix of the name of the input that stands for the spreadsheet of
# `--from-google-sheets`
_GOOGLE_SHEETS_SUFFIX = ".gsheet"


def get_filepaths_from_dir(directory: str, extensions: Iterable[str]) -> list[Path]:
    """Return a list of filepaths in the directory matching the given extensions."""
    matched_files = []
    for root, dirs, files in os.walk(directory):
        # Walk the subdirectories in a stable order
        dirs.sort()
        for file in sorted(files):
            if file.lower().endswith(tuple(extensions)):
                matched_files.append(Path(root) / file)

    return matched_files


def build_parser() -> argparse.ArgumentParser:
    supported_file_types_str = "\n".join(
        f"  - {ext}" + ("" if ext in INPUT_FILE_TYPES else " (output only)")
        for ext in SUPPORTED_FILE_TYPES
    )

    parser = argparse.ArgumentParser(
        prog="mobile-strings-converter",
        description="Script to convert Android & iOS string files to any supported "
        "file type, and vice versa.\n\n"
        f"Supported file types:\n{supported_file_types_str}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "input_paths",
        type=str,
        nargs="*",
        help="Files or directory paths of supported files to convert. Check the list "
        "of the supported file types above. Not needed with `--from-google-sheets`.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="Show program version info and exit.",
    )
    parser.add_argument(
        "-f",
        "--output-file",
        required=False,
        type=str,
        metavar="FILE_PATH",
        help="File path to save the converted file. Only works if only one input file "
        "is specified, or with `--merge`. Check the list of the supported file types "
        "above.",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        required=False,
        type=str,
        metavar="DIR_PATH",
        help="Directory path to save the converted files. Compatible with single and "
        "multiple input files as well as directories. The specified directory will be "
        "created if it does not already exist. Files with several locales (e.g. a "
        "spreadsheet with a column per language) converted to `.xml`, `.strings` or "
        "`.stringsdict` are split into a file per locale (e.g. "
        "`values-es/strings.xml`).",
    )
    parser.add_argument(
        "-t",
        "--target-type",
        type=str,
        metavar="FILE_TYPE",
        help="Target file type to convert the files (e.g. `json` or `.json`). "
        "Required when using `--output-dir`. Check the list of the supported file "
        "types above.",
    )
    parser.add_argument(
        "-g",
        "--to-google-sheets",
        required=False,
        type=str,
        metavar="SPREADSHEET_NAME",
        help="Write the strings to the first sheet of a Google spreadsheet, replacing "
        "its content. Only works if only one input file is specified, or with "
        "`--merge`. See `--credentials`.",
    )
    parser.add_argument(
        "-G",
        "--from-google-sheets",
        required=False,
        type=str,
        metavar="SPREADSHEET_NAME",
        help="Read the strings from the first sheet of a Google spreadsheet instead of "
        "input files. See `--credentials`.",
    )
    parser.add_argument(
        "-c",
        "--credentials",
        required=False,
        type=str,
        metavar="CREDENTIALS_PATH",
        help="Path of the `service_account.json` file used to access Google Sheets. "
        "Defaults to `~/.config/gspread/service_account.json`. You can learn how to "
        "generate it in the Google Sheets section in the README.",
    )
    parser.add_argument(
        "--check",
        required=False,
        action="store_true",
        help="Check the translations instead of converting them: report missing and "
        "obsolete translations, placeholders that differ from the default strings and "
        "names defined more than once. Exits with code 1 if any issue is found.",
    )
    parser.add_argument(
        "-p",
        "--print-comments",
        required=False,
        action="store_true",
        help="Print commented strings from the input file to the output file. Only "
        "valid for `.xml` or `.strings` input file types, otherwise it is ignored.",
    )
    parser.add_argument(
        "-s",
        "--source-language",
        required=False,
        type=str,
        metavar="LANGUAGE_CODE",
        help="Code of the language of the default strings (e.g. `en`), such as the "
        "ones in Android's `values` directory or iOS' `Base.lproj` directory. "
        "Required to write `.xcstrings` files, which need the code of their source "
        "language.",
    )
    parser.add_argument(
        "-m",
        "--merge",
        required=False,
        action="store_true",
        help="Merge the input files into a single output with a column per locale. The "
        "locale of each file is taken from its directory (e.g. `values-es` or "
        "`es.lproj`). Use it with `--output-file` or `--to-google-sheets`.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.input_paths and args.from_google_sheets:
        parser.error("pass input paths or -G/--from-google-sheets, not both.")

    if not (args.input_paths or args.from_google_sheets):
        parser.error("you must specify input paths or -G/--from-google-sheets.")

    has_output = args.output_file or args.output_dir or args.to_google_sheets
    if args.check and has_output:
        parser.error("--check doesn't write files. Remove -f, -d and -g.")

    if not (has_output or args.check):
        parser.error("you must specify an output with -f, -d or -g, or use --check.")

    if args.output_file and args.output_dir:
        parser.error("-f/--output-file and -d/--output-dir cannot be used together.")

    if args.merge and args.output_dir:
        parser.error(
            "-m/--merge writes a single file. Use -f/--output-file instead of "
            "-d/--output-dir."
        )

    if args.output_file and (
        Path(args.output_file).suffix.lower() not in SUPPORTED_FILE_TYPES
    ):
        parser.error(f"unsupported output file type: {args.output_file}")

    if args.output_dir:
        if not args.target_type:
            parser.error("-d/--output-dir requires -t/--target-type.")

        target_type = normalize_file_type(args.target_type)
        if target_type not in SUPPORTED_FILE_TYPES:
            parser.error(f"unsupported target type: {args.target_type}")

    if args.credentials and not os.path.isfile(args.credentials):
        parser.error(f"credentials file not found: {args.credentials}")

    # Each input is paired with the base directory used to mirror its relative path
    # inside the output directory
    input_files = []

    if args.from_google_sheets:
        # Named like a file so that `-d` writes `[SPREADSHEET_NAME].[TARGET_TYPE]`
        safe_name = re.sub(r"[\\/]", "_", args.from_google_sheets)
        input_files.append((Path(f"{safe_name}{_GOOGLE_SHEETS_SUFFIX}"), Path()))

    for path in args.input_paths:
        if os.path.isdir(path):
            # If it's a directory, get all matching files
            for filepath in get_filepaths_from_dir(path, INPUT_FILE_TYPES):
                input_files.append((filepath, Path(path)))
        elif os.path.isfile(path) and path.lower().endswith(tuple(INPUT_FILE_TYPES)):
            # If it's a supported file type, add it to the list
            input_files.append((Path(path), Path(path).parent))
        else:
            print(
                f"{ConsoleStyle.YELLOW}Skipping unsupported file or path: {path}"
                f"{ConsoleStyle.END}"
            )

    if not input_files:
        parser.error("no supported input files found.")

    if len(input_files) > 1 and not args.merge and not args.check:
        if args.output_file:
            parser.error(
                "cannot use -f/--output-file with multiple input files. Use "
                "-d/--output-dir or -m/--merge instead."
            )
        if args.to_google_sheets:
            parser.error(
                "cannot use -g/--to-google-sheets with multiple input files. Use "
                "-m/--merge instead."
            )

    if args.output_dir:
        # Different input files may have the same name (e.g. `values-es/strings.xml`
        # and `values-fr/strings.xml` passed as files)
        output_filepaths = [
            _output_dir_filepath(args.output_dir, filepath, base_dir, target_type)
            for filepath, base_dir in input_files
        ]
        duplicates = sorted(
            {str(p) for p in output_filepaths if output_filepaths.count(p) > 1}
        )
        if duplicates:
            parser.error(
                "several input files would be written to the same output file: "
                + ", ".join(duplicates)
                + ". Pass their parent directory instead to keep the directory "
                "structure."
            )

    exit_code = 0

    def fail(message: str) -> None:
        nonlocal exit_code
        exit_code = 1
        print(f"{ConsoleStyle.RED}{message}{ConsoleStyle.END}", file=sys.stderr)

    def read(input_filepath: Path) -> Catalog:
        with _print_warnings():
            if input_filepath.suffix == _GOOGLE_SHEETS_SUFFIX:
                return read_google_sheets(args.from_google_sheets, _credentials(args))
            return load(input_filepath, None, args.print_comments)

    # Each source is converted to the outputs: a single one with all the input files
    # when merging or checking, or one per input file
    if args.merge or args.check:
        catalogs = []
        for input_filepath, _ in input_files:
            try:
                catalogs.append((input_filepath, read(input_filepath)))
            except Exception as e:
                fail(f"Could not read {input_filepath}: {e}")

        if args.check:
            return _check(catalogs) or exit_code

        merged = Catalog.merge(catalog for _, catalog in catalogs)
        sources = [(input_files[0], merged)] if catalogs else []
    else:
        sources = []
        for input_file in input_files:
            try:
                sources.append((input_file, read(input_file[0])))
            except Exception as e:
                fail(f"Could not convert {input_file[0]}: {e}")

    for (input_filepath, base_dir), catalog in sources:
        if args.output_file or args.output_dir:
            try:
                with _print_warnings():
                    _write_outputs(args, catalog, input_filepath, base_dir)
            except Exception as e:
                fail(f"Could not convert {input_filepath}: {e}")

        if args.to_google_sheets:
            try:
                with _print_warnings():
                    write_google_sheets(
                        catalog, args.to_google_sheets, _credentials(args)
                    )
                print(
                    f"{ConsoleStyle.GREEN}Data successfully written to the "
                    f"'{args.to_google_sheets}' Google spreadsheet{ConsoleStyle.END}"
                )
            except Exception as e:
                fail(f"Could not write {input_filepath} to Google Sheets: {e}")

    return exit_code


def _credentials(args: argparse.Namespace) -> Path | None:
    return Path(args.credentials) if args.credentials else None


def _check(catalogs: list[tuple[Path, Catalog]]) -> int:
    """Prints the issues of the catalogs. Returns 1 if there is any, or 0 otherwise."""

    issues = [
        f"{filepath}: {issue}"
        for filepath, catalog in catalogs
        for issue in find_duplicates(catalog)
    ]
    issues += [str(issue) for issue in check(Catalog.merge(c for _, c in catalogs))]

    for issue in issues:
        print(f"{ConsoleStyle.YELLOW}{issue}{ConsoleStyle.END}")

    if issues:
        print(f"{ConsoleStyle.RED}{len(issues)} issue(s) found{ConsoleStyle.END}")
        return 1

    print(f"{ConsoleStyle.GREEN}No issues found{ConsoleStyle.END}")
    return 0


def _output_dir_filepath(
    output_dir: str, input_filepath: Path, base_dir: Path, target_type: str
) -> Path:
    relative_path = input_filepath.relative_to(base_dir)
    return Path(output_dir) / relative_path.with_suffix(target_type)


def _write_outputs(
    args: argparse.Namespace, catalog: Catalog, input_filepath: Path, base_dir: Path
) -> None:
    if args.output_file:
        output_filepaths = [Path(args.output_file)]
        if catalog.is_multi_locale and not is_multi_locale(output_filepaths[0].suffix):
            raise ValueError(
                f"the strings have {len(catalog.locales)} locales and "
                f"{output_filepaths[0].suffix} files can only hold one. Use "
                f"-d/--output-dir to write a file per locale."
            )
        save(catalog, output_filepaths[0], args.source_language)
    else:
        target_type = normalize_file_type(args.target_type)
        output_filepath = _output_dir_filepath(
            args.output_dir, input_filepath, base_dir, target_type
        )

        if catalog.is_multi_locale and not is_multi_locale(target_type):
            # Write `values-es/strings.xml`, `es.lproj/Localizable.strings`... next to
            # where the converted file would be
            output_filepaths = list(
                save_split(catalog, output_filepath.parent, target_type).values()
            )
        else:
            save(catalog, output_filepath, args.source_language)
            output_filepaths = [output_filepath]

    for output_filepath in output_filepaths:
        print(
            f"{ConsoleStyle.GREEN}Data successfully written to {output_filepath}"
            f"{ConsoleStyle.END}"
        )


@contextmanager
def _print_warnings() -> Iterator[None]:
    """Prints the warnings raised inside the context."""

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        try:
            yield
        finally:
            for caught in caught_warnings:
                print(f"{ConsoleStyle.YELLOW}{caught.message}{ConsoleStyle.END}")


if __name__ == "__main__":
    sys.exit(main())
