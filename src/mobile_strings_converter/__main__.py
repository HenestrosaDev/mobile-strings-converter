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
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="Show program version info and exit.",
    )
    parser.add_argument(
        "-f",
        "--output-filepath",
        required=False,
        type=str,
        help="Path to save the converted file. Only works if only one input file  "
        "is provided. See the README for a list of supported file types.",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        required=False,
        type=str,
        help="Directory where the converted files will be saved. Compatible with "
        "single and multiple input files as well as directories. The specified "
        "directory will be created if it does not already exist.",
    )
    parser.add_argument(
        "-t",
        "--target-type",
        type=str,
        help="Target file type to convert the files (e.g., .pdf, .json). Required if "
        "multiple file paths or the `--output-dir` is specified.",
    )
    parser.add_argument(
        "-g",
        "--google-sheets",
        required=False,
        action="store_true",
        help="If provided, a Google spreadsheet will be created in your Google "
        "account. You must pass the `service_account.json` with the -c flag.",
    )
    parser.add_argument(
        "-c",
        "--credentials",
        required=False,
        type=str,
        help="`service_account.json` filepath. Mandatory if you want to generate a "
        "spreadsheet in your Google account. You can learn how to generate "
        "it in the README.",
    )
    parser.add_argument(
        "-p",
        "--print-comments",
        required=False,
        action="store_true",
        help="If provided, the commented strings will be printed in the output file. "
        "Only valid for input files of type `.xml` or `.strings`. Otherwise it is "
        "ignored.",
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

    if args.google_sheets and not args.credentials:
        raise ValueError(
            f"{ConsoleStyle.RED}You need to pass the path of the "
            f"`service_account.json` file to generate a Sheet.{ConsoleStyle.END}"
        )
    elif not args.google_sheets and args.credentials:
        raise ValueError(
            f"{ConsoleStyle.RED}You need to pass the name of the Sheet to be "
            f"generated.{ConsoleStyle.END}"
        )
    elif args.google_sheets and args.credentials:
        for input_filepath in input_filepaths:
            to_google_sheets(
                args.input_filepath,
                sheet_name=Path(input_filepath).stem,
                credentials_filepath=Path(args.credentials),
                with_comments=args.print_comments,
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
