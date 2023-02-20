import argparse
from pathlib import Path

import converter as conv
from console_style import ConsoleStyle


def main():
    parser = argparse.ArgumentParser()
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
        help="Output filepath with the strings properly arranged. It can be a JSON, "
        "CSV, YAML, HTML, XLS, XLSX, Google Sheet, MD, PDF, iOS strings file or ODS "
        "file.",
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

    input_path = Path(args.input_filepath)

    if input_path.suffix == ".strings":
        strings = conv.get_strings(input_path, pattern=r'"([^"]+)"\s*=\s*"([^"]*)";')
    elif input_path.suffix == ".xml":
        strings = conv.get_strings(
            input_path, pattern=r'<string name="(.*?)">(.*?)</string>'
        )
    else:
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
            strings,
            sheet_name=args.google_sheets,
            credentials_filepath=Path(args.credentials),
        )

    if args.output_filepath:
        output_path = Path(args.output_filepath)

        if output_path.suffix == ".csv":
            conv.to_csv(strings, output_path)
        elif output_path.suffix == ".xlsx" or output_path.suffix == ".ods":
            conv.to_xlsx_ods(strings, output_path)
        elif output_path.suffix == ".json":
            conv.to_json(strings, output_path)
        elif output_path.suffix == ".yaml":
            conv.to_yaml(strings, output_path)
        elif output_path.suffix == ".html":
            conv.to_html(strings, output_path)
        elif output_path.suffix == ".strings":
            conv.to_ios(strings, output_path)
        elif output_path.suffix == ".xml":
            conv.to_android(strings, output_path)
        elif output_path.suffix == ".pdf":
            conv.to_pdf(strings, output_path)
        elif output_path.suffix == ".md":
            conv.to_md(strings, output_path)
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
