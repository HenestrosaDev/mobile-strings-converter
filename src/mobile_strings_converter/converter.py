import csv
import json
import os
import re
import warnings
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import List

import gspread
import openpyxl
import yaml
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from fpdf import FPDF
from google.oauth2.credentials import Credentials
from lingua import LanguageDetectorBuilder

from .console_style import ConsoleStyle


def convert_strings(
    input_filepath: Path, output_filepath: Path, should_print_comments: bool
):
    """
    Extracts strings from the input file in either .xml or .strings format and converts
    them to the desired output file format. The output file format can be any of the
    following:

    - Android strings format (*.xml)
    - CSV
    - HTML
    - iOS strings format (*.strings)
    - JSON
    - MD
    - ODS
    - PDF
    - XLSX
    - YAML

    :param input_filepath: .strings or .xml file to extract the strings
    :type input_filepath: Path
    :param output_filepath: Name of the sheet to be generated
    :type output_filepath: Path
    :param should_print_comments: True if the user wants to print comments from
        .strings/.xml to the output file
    :type should_print_comments: bool
    """

    strings = get_strings(input_filepath, should_print_comments)

    if output_filepath:
        conversion_functions = {
            ".csv": to_csv,
            ".xlsx": to_sheet,
            ".ods": to_sheet,
            ".md": to_md,
            ".json": to_json,
            ".yaml": to_yaml,
            ".html": to_html,
            ".strings": to_ios,
            ".xml": to_android,
            ".pdf": to_pdf,
        }

        if output_filepath.suffix in conversion_functions:
            conversion_functions[output_filepath.suffix](strings, output_filepath)

            print(
                f"{ConsoleStyle.GREEN}Data successfully written to {output_filepath}"
                f"{ConsoleStyle.END}"
            )
        else:
            raise ValueError(
                f"{ConsoleStyle.YELLOW}File type not supported. Feel free to create "
                f"an issue here (https://github.com/HenestrosaConH/mobile-strings"
                f"-converter/issues) if you want the file type to be supported by the "
                f"package.{ConsoleStyle.END}"
            )


def get_strings(input_filepath: Path, should_print_comments: bool):
    """
    Creates a Google spreadsheet with the extracted strings from the input filepath

    :param input_filepath: .strings or .xml file to extract the strings
    :type input_filepath: Path
    :param should_print_comments: True if the user wants to print comments from
        .strings/.xml to the file
    :type should_print_comments: bool
    """

    if input_filepath.suffix == ".strings":
        if should_print_comments:
            pattern = r'"(.*?)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;'
        else:
            pattern = r'^(?!\s*//)\s*"(.+?)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;'
    elif input_filepath.suffix == ".xml":
        if should_print_comments:
            pattern = r'<string name="(.*?)">(.*?)</string>'
        else:
            pattern = r'^(?!\s*<!--)\s*<string name="(.*?)">(.*?)</string>(?!\s*-->)'
    else:
        raise ValueError(
            "The extension of the provided file must be .strings for iOS or .xml "
            "Android"
        )

    # Open the Localizable.strings file
    with open(input_filepath, "r", encoding="utf-8") as file:
        strings_data = file.read()

    # Extract the strings using a regular expression
    strings = re.findall(pattern, strings_data, re.MULTILINE)

    if len(strings) >= 1:
        return strings
    else:
        raise ValueError(
            "The file provided is not a valid Localizable.strings nor strings.xml file."
        )


def to_google_sheets(
    input_filepath: Path,
    sheet_name: str,
    credentials_filepath: Path,
    should_print_comments: bool,
):
    """
    Creates a Google spreadsheet with the extracted strings from the input filepath

    :param input_filepath: .strings or .xml file to extract the strings
    :type input_filepath: Path
    :param sheet_name: Name of the sheet to be generated
    :type sheet_name: str
    :param credentials_filepath: Path to the service_account.json in order to be able
        to create the sheet in the user's Google account
    :type credentials_filepath: Path
    :param should_print_comments: True if the user wants to print comments from
        .strings/.xml to the sheet
    :type should_print_comments: bool
    """

    strings = get_strings(input_filepath, should_print_comments)

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
    for string in strings:
        sheet.append_row(string)


def to_csv(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .csv file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    with open(output_filepath, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        header = ["name", "value"]
        writer.writerow(header)

        # Write the data to the file
        for name, value in strings:
            writer.writerow([name, value])


def to_sheet(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .xlsx / .ods file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    # Create a new workbook
    workbook = openpyxl.Workbook()

    # Create a new sheet
    sheet = workbook.active

    # Write the header row
    sheet.cell(row=1, column=1, value="NAME")
    sheet.cell(row=1, column=2, value="VALUE")

    # Write the data to the sheet
    for i, (name, value) in enumerate(strings, start=2):
        sheet.cell(row=i, column=1, value=name)
        sheet.cell(row=i, column=2, value=value)

    # Save the file
    workbook.save(output_filepath)


def to_json(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .json file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    # Create a list of dictionaries to store the data
    data_list = []
    for name, value in strings:
        data_list.append({"name": name, "value": value})

    # Write the data to the JSON file
    with open(output_filepath, "w", encoding="utf-8") as file:
        json.dump(data_list, file, ensure_ascii=False, indent=2)


def to_yaml(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .yaml file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    # Convert the data to a dictionary
    strings_dict = {name: value for name, value in strings}

    # Write the data to the YAML file
    with open(output_filepath, "w", encoding="utf-8") as file:
        yaml.dump(strings_dict, file, default_flow_style=False, allow_unicode=True)


def to_html(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .html file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    # Create an HTML file
    with open(output_filepath, "w", encoding="utf-8") as file:
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
        for name, value in strings:
            file.write("\t\t<tr>\n")
            file.write(f"\t\t\t<td>{name}</td>\n")
            file.write(f"\t\t\t<td>{value}</td>\n")
            file.write("\t\t</tr>\n")

        file.write("\t</tbody>\n")
        file.write("</table>\n")


def to_ios(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .strings file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    with open(output_filepath, "w", encoding="utf-8") as file:
        for string in strings:
            file.write(f'"{string[0]}" = "{string[1]}";\n')


def to_android(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .xml file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write("<resources>\n")
        for string in strings:
            file.write(f'\t<string name="{string[0]}">{string[1]}</string>\n')

        file.write("</resources>")


def to_pdf(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .pdf file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    # Ignore the following warning when adding a font already added:
    # UserWarning: Core font or font already added 'dejavusanscondensed': doing nothing
    warnings.filterwarnings("ignore", category=UserWarning)

    def add_font(font_name, size=12):
        root_dir = Path(__file__).parent
        pdf.add_font(fname=str(root_dir / f"assets/fonts/{font_name}.ttf"))
        pdf.set_font(font_name, size=size)

    # Create a new PDF file
    pdf = FPDF(orientation="P", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    # Cell properties
    c_width = 95
    c_height = 10

    # Add headers to table
    pdf.cell(c_width, c_height, "NAME", border=1)
    pdf.cell(c_width, c_height, "VALUE", border=1)
    pdf.ln()

    detector = (
        LanguageDetectorBuilder.from_all_languages()
        .with_preloaded_language_models()
        .build()
    )

    # Add table data
    # https://stackoverflow.com/questions/53526311/fpdf-multicell-same-height
    for i, string in enumerate(strings):
        x = pdf.get_x()
        y = pdf.get_y()

        max_height = 0
        cells_in_row = 2

        for j in range(cells_in_row):
            language_code = None
            try:
                if j % 2 == 0:  # Prevents 'name' language detection
                    add_font("DejaVuSansCondensed")
                else:
                    language_code = detector.detect_language_of(
                        string[j]
                    ).iso_code_639_1.name.lower()

                    if language_code in [
                        "bn",  # Bengali
                        "hi",  # Hindi
                        "kn",  # Kannada
                        "ml",  # Malayalam
                        "mr",  # Marathi
                        "or",  # Oriya
                        "bo",  # Tibetan
                    ]:
                        add_font("gargi")
                    elif language_code == "gu":  # Gujarati
                        add_font("Aakar")
                    elif language_code == "te":  # Telugu
                        add_font("AnekTelugu-VariableFont_wdth,wght")
                    elif language_code == "ta":  # Tamil
                        add_font("latha")
                    elif language_code == "pa":  # Punjabi, Panjabi
                        add_font("Gurvetica_a8_Heavy")
                    elif language_code == "zh" or language_code == "ja":
                        # Chinese or Japanese
                        add_font("fireflysung")
                    elif language_code == "ko":  # Korean
                        add_font("Eunjin")
                    elif language_code == "th":  # Thai
                        add_font("Waree")
                    else:
                        add_font("DejaVuSansCondensed")

                if language_code in [
                    # RTL languages
                    "ar",  # Arabic
                    "he",  # Hebrew
                    "dv",  # Dhivehi
                    "ku",  # Kurdish (sorani)
                    "ps",  # Pashto
                    "fa",  # Persian
                    "sd",  # Sindhi
                    "ur",  # Urdu
                    "ug",  # Uyghur
                    "yi",  # Yiddish
                ]:
                    pdf.multi_cell(c_width, c_height, get_display(reshape(string[j])))
                else:
                    pdf.multi_cell(c_width, c_height, string[j])

                if pdf.get_y() - y > max_height:
                    max_height = pdf.get_y() - y

                pdf.set_xy(x + (c_width * (j + 1)), y)
            except (Exception,):
                with open(
                    output_filepath.parent / f"{output_filepath.stem}-errors.txt",
                    "a",
                    encoding="utf-8",
                ) as f:
                    f.write(f"{string[1]} not supported\n")

        for j in range(cells_in_row + 1):
            pdf.line(x + c_width * j, y, x + c_width * j, y + max_height)

        pdf.line(x, y, x + c_width * cells_in_row, y)
        pdf.line(x, y + max_height, x + c_width * cells_in_row, y + max_height)

        pdf.ln()

        if (
            i < len(strings) - 1
            and pdf.get_y() + (max_height * cells_in_row) > pdf.h - 10
        ):
            pdf.add_page()

    # Inside this context manager, all output to stdout and stderr will be suppressed
    # This is done because in Windows, the following exception is raised if the
    # strings.xml file contains unsupported characters:
    #
    # UnicodeEncodeError: 'charmap'
    # codec can't encode characters in position 0-9: character maps to <undefined>
    with open(os.devnull, "w") as devnull:
        with redirect_stdout(devnull), redirect_stderr(devnull):
            # Save the PDF file
            pdf.output(str(output_filepath))


def to_md(strings: List[str], output_filepath: Path):
    """
    Formats strings to a .md file

    :param strings: Strings extracted from a .strings or .xml file
    :type strings: List[str]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    with open(output_filepath, "w", encoding="utf-8") as f:
        # Write each string to the Markdown file in a table format
        f.write("| NAME | VALUE |\n")
        f.write("| ----------- | ----------- |\n")
        for name, translation in strings:
            f.write(f"| {name} | {translation} |\n")
