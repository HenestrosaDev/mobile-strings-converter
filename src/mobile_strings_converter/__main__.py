import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .console_style import ConsoleStyle
from .converter import SUPPORTED_FILE_TYPES, convert_strings, to_google_sheets


def get_filepaths_from_dir(directory, extensions):
    """Return a list of filepaths in the directory matching the given extensions."""
    matched_files = []
    for root, _, files in os.walk(directory):
        for file in sorted(files):
            if file.lower().endswith(tuple(extensions)):
                matched_files.append(Path(root) / file)

    return matched_files


def normalize_file_type(file_type):
    """Return the file type as a lowercase extension with a leading dot."""
    file_type = file_type.lower()
    return file_type if file_type.startswith(".") else f".{file_type}"


def build_parser():
    supported_file_types_str = "\n".join(f"  - {ext}" for ext in SUPPORTED_FILE_TYPES)

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
        nargs="+",  # Accept one or more values
        help="Files or directory paths of supported files to convert. Check the list "
        "of the supported file types above.",
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
        "is specified. Check the list of the supported file types above.",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        required=False,
        type=str,
        metavar="DIR_PATH",
        help="Directory path to save the converted files. Compatible with single and "
        "multiple input files as well as directories. The specified directory will be "
        "created if it does not already exist.",
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
        "--google-sheets",
        required=False,
        type=str,
        metavar="CREDENTIALS_PATH",
        help="Write the strings to the Google spreadsheet named after each input file "
        "(without its extension) in your Google account. You must specify the "
        "`service_account.json` path. You can learn how to generate it in the "
        "Generating a Spreadsheet in Google Sheets section in the README.",
    )
    parser.add_argument(
        "-p",
        "--print-comments",
        required=False,
        action="store_true",
        help="Print commented strings from the input file to the output file. "
        "Only valid for `.xml` or `.strings` input file types, otherwise it is ignored.",
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not (args.output_file or args.output_dir or args.google_sheets):
        parser.error("you must specify an output with -f, -d or -g.")

    if args.output_file and args.output_dir:
        parser.error("-f/--output-file and -d/--output-dir cannot be used together.")

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

    if args.google_sheets and not os.path.isfile(args.google_sheets):
        parser.error(
            "you need to pass the path of the `service_account.json` file to generate "
            "a Sheet."
        )

    # Each input file is paired with the base directory used to mirror its relative
    # path inside the output directory
    input_files = []

    for path in args.input_paths:
        if os.path.isdir(path):
            # If it's a directory, get all matching files
            for filepath in get_filepaths_from_dir(path, SUPPORTED_FILE_TYPES):
                input_files.append((filepath, Path(path)))
        elif os.path.isfile(path) and path.lower().endswith(
            tuple(SUPPORTED_FILE_TYPES)
        ):
            # If it's a supported file type, add it to the list
            input_files.append((Path(path), Path(path).parent))
        else:
            print(
                f"{ConsoleStyle.YELLOW}Skipping unsupported file or path: {path}"
                f"{ConsoleStyle.END}"
            )

    if not input_files:
        parser.error("no supported input files found.")

    # Ensure the correct output options are used
    conversions = []

    if args.output_file:
        if len(input_files) > 1:
            parser.error(
                "cannot use -f/--output-file with multiple input files. Use "
                "-d/--output-dir instead."
            )
        conversions.append((input_files[0][0], Path(args.output_file)))
    elif args.output_dir:
        output_dir = Path(args.output_dir)
        for input_filepath, base_dir in input_files:
            relative_path = input_filepath.relative_to(base_dir)
            conversions.append(
                (input_filepath, output_dir / relative_path.with_suffix(target_type))
            )

        # Different input files may have the same name (e.g. `values-es/strings.xml`
        # and `values-fr/strings.xml` passed as files)
        output_filepaths = [output_filepath for _, output_filepath in conversions]
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

    for input_filepath, output_filepath in conversions:
        try:
            output_filepath.parent.mkdir(parents=True, exist_ok=True)
            convert_strings(input_filepath, output_filepath, args.print_comments)
        except Exception as e:
            exit_code = 1
            print(
                f"{ConsoleStyle.RED}Could not convert {input_filepath}: {e}"
                f"{ConsoleStyle.END}",
                file=sys.stderr,
            )

    if args.google_sheets:
        for input_filepath, _ in input_files:
            try:
                to_google_sheets(
                    input_filepath,
                    sheet_name=input_filepath.stem,
                    credentials_filepath=Path(args.google_sheets),
                    with_comments=args.print_comments,
                )
                print(
                    f"{ConsoleStyle.GREEN}Data successfully written to the "
                    f"'{input_filepath.stem}' Google spreadsheet{ConsoleStyle.END}"
                )
            except Exception as e:
                exit_code = 1
                print(
                    f"{ConsoleStyle.RED}Could not write {input_filepath} to Google "
                    f"Sheets: {e}{ConsoleStyle.END}",
                    file=sys.stderr,
                )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
