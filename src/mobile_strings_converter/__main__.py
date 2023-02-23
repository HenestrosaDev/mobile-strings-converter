import argparse
from pathlib import Path

import converter as conv
from console_style import ConsoleStyle


def main():
    parser = argparse.ArgumentParser(
        description="Takes input and output files from console."
    )
    parser.add_argument(
        "input_filepath",
        type=str,
        help=".xml or .strings filepath that contains the strings.",
    )
    parser.add_argument(
        "-o",
        "--output-filepath",
        required=False,
        type=str,
        help="Output filepath where you want to store the converted file. It can be a "
        "CSV, HTML, iOS strings file, MD, JSON, ODS, PDF, XLSX, XML or YAML file.",
    )
    parser.add_argument(
        "-g",
        "--google-sheets",
        required=False,
        type=str,
        help="Creates a spreadsheet in Google Sheets with the name passed as argument.",
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
        help="If called, indicates that commented strings will be printed in the "
        "output file.",
    )
    args = parser.parse_args()

    input_filepath = Path(args.input_filepath)

    if input_filepath.suffix not in [".strings", ".xml"]:
        print(
            f"{ConsoleStyle.RED}Invalid input file. Its extension must be .strings "
            f"for iOS strings or .xml for Android strings.{ConsoleStyle.RED}"
        )
        return

    if args.google_sheets and not args.credentials:
        print(
            f"{ConsoleStyle.RED}Error: You need to pass the path of the "
            f"`service_account.json` file to generate a Sheet.{ConsoleStyle.END}"
        )
        return
    elif not args.google_sheets and args.credentials:
        print(
            f"{ConsoleStyle.RED}Error: You need to pass the name of the Sheet to be "
            f"generated.{ConsoleStyle.END}"
        )
        return
    elif args.google_sheets and args.credentials:
        conv.to_google_sheets(
            input_filepath,
            sheet_name=args.google_sheets,
            credentials_filepath=Path(args.credentials),
            should_print_comments=args.print_comments,
        )

    if args.output_filepath:
        conversion_functions = {
            ".csv": conv.to_csv,
            ".xlsx": conv.to_xlsx,
            ".ods": conv.to_ods,
            ".md": conv.to_md,
            ".json": conv.to_json,
            ".yaml": conv.to_yaml,
            ".html": conv.to_html,
            ".strings": conv.to_ios,
            ".xml": conv.to_android,
            ".pdf": conv.to_pdf,
        }

        output_path = Path(args.output_filepath)

        if output_path.suffix in conversion_functions:
            conversion_functions[output_path.suffix](
                input_filepath, output_path, args.print_comments
            )
        else:
            print(
                f"{ConsoleStyle.YELLOW}File type not supported. Feel free to create "
                f"an issue here (https://github.com/HenestrosaConH/mobile-strings"
                f"-converter/issues) if you want the file type to be supported by the "
                f"package.{ConsoleStyle.END}"
            )
            return

        print(
            f"{ConsoleStyle.GREEN}Data successfully written to {output_path}"
            f"{ConsoleStyle.END}"
        )


if __name__ == "__main__":
    main()
