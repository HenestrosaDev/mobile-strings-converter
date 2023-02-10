import argparse
import csv
import json
import re
from pathlib import Path

import ezodf
import gspread
import xlsxwriter
import yaml
from oauth2client.service_account import ServiceAccountCredentials
from style import Style


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
            f"{Style.RED}Error: You need to pass the path of the "
            f"`service_account.json` file to generate a Sheet.{Style.END}"
        )
        return
    elif not args.google_sheets and args.credentials:
        print(
            f"{Style.RED}Error: You need to pass the name of the Sheet to be "
            f"generated.{Style.END}"
        )
        return
    elif args.google_sheets and args.credentials:
        to_google_sheets(Path(args.input_filepath), args.google_sheets)

    if args.output_filepath:
        output_path = Path(args.output_filepath)
        if output_path.suffix == ".csv":
            to_csv(Path(args.input_filepath), output_path)
        elif output_path.suffix == ".xlsx":
            to_xlsx(Path(args.input_filepath), Path(output_path))
        elif output_path.suffix == ".json":
            to_json(Path(args.input_filepath), Path(output_path))
        elif output_path.suffix == ".ods":
            to_json(Path(args.input_filepath), Path(output_path))
        elif output_path.suffix == ".yaml":
            to_yaml(Path(args.input_filepath), Path(output_path))
        elif output_path.suffix == ".html":
            to_html(Path(args.input_filepath), Path(output_path))

        print(f"{Style.GREEN}Data successfully written to {output_path}{Style.END}")


def get_xml_data(xml_filepath: Path):
    # Open the string.xml file
    with open(xml_filepath, "r", encoding="utf-8") as file:
        xml_data = file.read()

    # Extract the "name" attribute and content of the tag
    pattern = r'<string name="(.*?)">(.*?)</string>'
    data = re.findall(pattern, xml_data)

    return data


def to_google_sheets(xml_filepath: Path, sheet_name: str):
    data = get_xml_data(xml_filepath)

    # Authenticate with Google Sheets API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "path/to/service_account.json", scope
    )
    client = gspread.authorize(credentials)

    # Open a new sheet or an existing one
    sheet = client.open(sheet_name).sheet1

    # Clear the existing data in the sheet
    sheet.clear()

    # Write the data to the sheet
    for row in data:
        sheet.append_row(row)


def to_csv(xml_filepath: Path, csv_filepath: Path):
    data = get_xml_data(xml_filepath)

    # Create a CSV file
    with open(csv_filepath, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        header = ["name", "value"]
        writer.writerow(header)

        # Write the data to the file
        for name, value in data:
            writer.writerow([name, value])


def to_xlsx(xml_filepath: Path, xlsx_filepath: Path):
    data = get_xml_data(xml_filepath)

    # Create an Excel .xlsx file
    workbook = xlsxwriter.Workbook(xlsx_filepath)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({"bold": True})

    # Write the header row
    worksheet.write(0, 0, "NAME", bold)
    worksheet.write(0, 1, "VALUE", bold)

    # Write the data to the sheet
    row = 1
    for name, value in data:
        worksheet.write(row, 0, name)
        worksheet.write(row, 1, value)
        row += 1

    workbook.close()


def to_json(xml_filepath: Path, json_filepath: Path):
    data = get_xml_data(xml_filepath)

    # Create a list of dictionaries to store the data
    data_list = []
    for name, value in data:
        data_list.append({"name": name, "value": value})

    # Write the data to the JSON file
    with open(json_filepath, "w", encoding="utf-8") as file:
        json.dump(data_list, file, ensure_ascii=False, indent=2)


def to_ods(xml_filepath: Path, ods_filepath: Path):
    data = get_xml_data(xml_filepath)

    # Create an ODS file
    doc = ezodf.newdoc(doctype="ods", filename=ods_filepath)
    sheet = doc.sheets[0]

    # Write the header row
    sheet["A1"].value = "NAME"
    sheet["B1"].value = "VALUE"

    # Write the data to the sheet
    row = 2
    for name, value in data:
        sheet["A" + str(row)].value = name
        sheet["B" + str(row)].value = value
        row += 1

    # Save the file
    doc.save()


def to_yaml(xml_filepath: Path, yaml_filepath: Path):
    data = get_xml_data(xml_filepath)

    # Convert the data to a dictionary
    data_dict = {name: value for name, value in data}

    # Write the data to the YAML file
    with open(yaml_filepath, "w", encoding="utf-8") as file:
        yaml.dump(data_dict, file, default_flow_style=False, allow_unicode=True)


def to_html(xml_filepath: Path, html_filepath: Path):
    data = get_xml_data(xml_filepath)

    # Create an HTML file
    with open(html_filepath, "w", encoding="utf-8") as file:
        file.write("<table>\n")
        file.write("\t<thead>\n")
        file.write("\t\t<tr>\n")
        file.write("\t\t\t<th>NAME</th>\n")
        file.write("\t\t\t<th>VALUE</th>\n")
        file.write("\t\t</tr>\n")
        file.write("\t</thead>\n")
        file.write("\t<tbody>\n")

        # Write the data to the HTML file
        for name, value in data:
            file.write("\t\t<tr>\n")
            file.write(f"\t\t\t<td>{name}</td>\n")
            file.write(f"\t\t\t<td>{value}</td>\n")
            file.write("\t\t</tr>\n")

        file.write("\t</tbody>\n")
        file.write("</table>\n")


if __name__ == "__main__":
    main()
