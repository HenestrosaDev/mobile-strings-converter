import csv
import json
import re
from pathlib import Path

import gspread
import openpyxl
import yaml
from google.oauth2.credentials import Credentials


def get_xml_data(xml_filepath: Path):
    # Open the string.xml file
    with open(xml_filepath, "r", encoding="utf-8") as file:
        xml_data = file.read()

    # Extract the "name" attribute and content of the tag
    pattern = r'<string name="(.*?)">(.*?)</string>'
    data = re.findall(pattern, xml_data)

    if len(data) >= 1:
        return data
    else:
        raise ValueError("The XML file provided is not a valid Android strings file.")


def to_google_sheets(xml_filepath: Path, sheet_name: str, credentials_filepath: Path):
    data = get_xml_data(xml_filepath)

    # Authenticate with Google Sheets API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_file(credentials_filepath, scope)
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

    # Create a new workbook
    workbook = openpyxl.Workbook()

    # Create a new sheet
    sheet = workbook.active

    # Write the header row
    sheet.cell(row=1, column=1, value="NAME")
    sheet.cell(row=1, column=2, value="VALUE")

    # Write the data to the sheet
    for i, (name, value) in enumerate(data, start=2):
        sheet.cell(row=i, column=1, value=name)
        sheet.cell(row=i, column=2, value=value)

    # Save the file
    workbook.save(xlsx_filepath)


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

    # Create a new workbook
    workbook = openpyxl.Workbook()

    # Create a new sheet
    sheet = workbook.active

    # Write the header row
    sheet.cell(row=1, column=1, value="NAME")
    sheet.cell(row=1, column=2, value="VALUE")

    # Write the data to the sheet
    for i, (name, value) in enumerate(data, start=2):
        sheet.cell(row=i, column=1, value=name)
        sheet.cell(row=i, column=2, value=value)

    # Save the file
    workbook.save(ods_filepath)


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
        file.write("<head>\n")
        file.write('\t<meta charset="UTF-8">\n')
        file.write("</head>\n")
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
