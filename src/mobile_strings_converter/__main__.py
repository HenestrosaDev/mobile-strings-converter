import argparse
import os
from pathlib import Path

from console_style import ConsoleStyle
from converter import convert_strings, to_google_sheets
from mobile_strings_converter import __version__


def get_filepaths_from_dir(directory, extensions):
    """Return a list of filepaths in the directory matching the given extensions."""
    matched_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(extensions)):
                matched_files.append(Path(root) / file)

    return matched_files


def main():
    supported_file_types = [
        ".csv",
        ".xlsx",
        ".ods",
        ".md",
        ".json",
        ".yaml",
        ".html",
        ".strings",
        ".xml",
        ".pdf",
    ]
    supported_file_types_str = "\n".join(f"  - {ext}" for ext in supported_file_types)

    parser = argparse.ArgumentParser(
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
        help="Target file type to convert the files. Required when specifying "
        "multiple file paths or `--output-dir`. Check the list of the supported file "
        "types above.",
    )
    parser.add_argument(
        "-g",
        "--google-sheets",
        required=False,
        type=str,
        metavar="CREDENTIALS_PATH",
        help="Create a Google spreadsheet with the output in your Google account. "
        "You must specify the `service_account.json` path. You can learn how to "
        "generate it in the Generating a Spreadsheet in Google Sheets section in the "
        "README.",
    )
    parser.add_argument(
        "-p",
        "--print-comments",
        required=False,
        action="store_true",
        help="Print commented strings from the input file to the output file. "
        "Only valid for `.xml` or `.strings` input file types, otherwise it is ignored.",
    )

    args = parser.parse_args()

    # Check if the output-extension argument is provided when output-dir is specified
    if args.output_dir and not args.target_type:
        raise ValueError(
            f"{ConsoleStyle.RED}--output-dir requires --output-extension."
            f"{ConsoleStyle.END}"
        )

    input_filepaths = []
    output_dir = None

    for path in args.input_paths:
        if os.path.isdir(path):
            # If it's a directory, get all matching files
            input_filepaths.extend(get_filepaths_from_dir(path, supported_file_types))
        elif os.path.isfile(path) and path.endswith(tuple(supported_file_types)):
            # If it's a supported file type, add it to the list
            input_filepaths.append(Path(path))
        else:
            print(
                f"{ConsoleStyle.YELLOW}Skipping unsupported file or path: {path}"
                f"{ConsoleStyle.END}"
            )

    # Ensure the correct output options are used
    if args.output_filepath:
        if len(input_filepaths) > 1:
            raise ValueError(
                "Cannot use --output-filepath with multiple input files. Use "
                "--output-dir instead."
            )
        output_path = Path(args.output_filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    elif args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        raise ValueError(
            f"{ConsoleStyle.RED}You must specify an output path with the "
            f"-f or -d flag.{ConsoleStyle.END}"
        )

    if credentials_path := args.google_sheets:
        if os.path.isfile(credentials_path):
            for input_filepath in input_filepaths:
                to_google_sheets(
                    args.input_filepath,
                    sheet_name=Path(input_filepath).stem,
                    credentials_filepath=Path(credentials_path),
                    with_comments=args.print_comments,
                )
        else:
            raise ValueError(
                f"{ConsoleStyle.RED}You need to pass the path of the "
                f"`service_account.json` file to generate a Sheet.{ConsoleStyle.END}"
            )

    for input_filepath in input_filepaths:
        if args.output_filepath:
            output_filepath = Path(args.output_filepath)
        else:
            output_filename = Path(input_filepath).stem + args.target_type
            output_filepath = output_dir / output_filename

        convert_strings(input_filepath, output_filepath, args.print_comments)


if __name__ == "__main__":
    main()
