import argparse
from pathlib import Path

import converter as conv
from console_style import ConsoleStyle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_filepath",
        type=str,
        help="Input XML filepath with the Android strings.",
    )
    parser.add_argument(
        "-o",
        "--output-filepath",
        required=False,
        type=str,
        help="Output filepath with the strings properly arranged. It can be a JSON, "
        "CSV, YAML, HTML, XLS, XLSX, Google Sheet and ODS.",
    )
    parser.add_argument(
        "-gs",
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
    args = parser.parse_args()

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
            Path(args.input_filepath), args.google_sheets, Path(args.credentials)
        )

    if args.output_filepath:
        input_path = Path(args.input_filepath)
        output_path = Path(args.output_filepath)

        should_print_success = True

        if output_path.suffix == ".csv":
            conv.to_csv(input_path, output_path)
        elif output_path.suffix == ".xlsx":
            conv.to_xlsx(input_path, output_path)
        elif output_path.suffix == ".json":
            conv.to_json(input_path, output_path)
        elif output_path.suffix == ".ods":
            conv.to_ods(input_path, output_path)
        elif output_path.suffix == ".yaml":
            conv.to_yaml(input_path, output_path)
        elif output_path.suffix == ".html":
            conv.to_html(input_path, output_path)
        else:
            print(
                f"{ConsoleStyle.YELLOW}File type not supported. Feel free to create "
                f"an issue here (https://github.com/HenestrosaConH/android-strings"
                f"-converter/issues) if you want the file type to be supported by the "
                f"package.{ConsoleStyle.END}"
            )
            should_print_success = False

        if should_print_success:
            print(
                f"{ConsoleStyle.GREEN}Data successfully written to {output_path}"
                f"{ConsoleStyle.END}"
            )


if __name__ == "__main__":
    main()
