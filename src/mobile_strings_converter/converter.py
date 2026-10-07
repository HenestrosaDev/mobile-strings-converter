import csv
import html
import json
import os
import re
import warnings
from contextlib import redirect_stderr, redirect_stdout
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Tuple

import ezodf
import gspread
import openpyxl
import yaml
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from fpdf import FPDF
from lingua import LanguageDetectorBuilder
from lxml import etree
from pypdf import PdfReader

from .console_style import ConsoleStyle

SUPPORTED_FILE_TYPES = [
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

# Name of the JSON file embedded in the generated PDFs. It holds the exact strings
# written to the PDF so they can be read back losslessly.
PDF_EMBEDDED_FILENAME = "strings.json"


def convert_strings(
    input_filepath: Path, output_filepath: Path, with_comments: bool = False
):
    """
    Extracts strings from the input file in either .xml or .strings format and converts
    them to the desired output file format. The output file format can be any of the
    following:

    Supported formats and corresponding extraction functions:
    - .csv: to_csv
    - .xlsx: to_xlsx
    - .ods: to_ods
    - .md: to_md
    - .json: to_json
    - .yaml: to_yaml
    - .html: to_html
    - .strings: to_ios
    - .xml: to_android
    - .pdf: to_pdf

    :param input_filepath: .strings or .xml file to extract the strings
    :type input_filepath: Path
    :param output_filepath: Name of the sheet to be generated
    :type output_filepath: Path
    :param with_comments: True if the user wants to include comments from
        .strings/.xml to the output file
    :type with_comments: bool
    """

    strings = get_strings(input_filepath, with_comments)

    if output_filepath:
        conversion_functions = {
            ".csv": to_csv,
            ".xlsx": to_xlsx,
            ".ods": to_ods,
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
                f"an issue here (https://github.com/HenestrosaDev/mobile-strings"
                f"-converter/issues) if you want the file type to be supported by the "
                f"package.{ConsoleStyle.END}"
            )


def get_strings(
    input_filepath: Path, with_comments: bool = False
) -> List[Tuple[str, str]]:
    """
    Extracts strings from various file formats based on the file extension.

    Supported formats and corresponding extraction functions:
    - .csv: get_strings_from_csv
    - .xlsx: get_strings_from_xlsx
    - .ods: get_strings_from_ods
    - .md: get_strings_from_md
    - .json: get_strings_from_json
    - .yaml: get_strings_from_yaml
    - .html: get_strings_from_html
    - .strings: get_strings_from_ios
    - .xml: get_strings_from_xml
    - .pdf: get_strings_from_pdf

    If the input file format is .strings or .xml, additional options are available:
    - with_comments: If True, includes comments in the extracted strings.

    :param input_filepath: Path to the input file.
    :type input_filepath: Path
    :param with_comments: True if comments should be included (for .strings and
        .xml files), False otherwise.
    :type with_comments: bool
    :return: A list of tuples containing extracted strings and their corresponding values.
    :rtype: List[Tuple[str, str]]
    """

    conversion_functions = {
        ".csv": get_strings_from_csv,
        ".xlsx": get_strings_from_xlsx,
        ".ods": get_strings_from_ods,
        ".md": get_strings_from_md,
        ".json": get_strings_from_json,
        ".yaml": get_strings_from_yaml,
        ".html": get_strings_from_html,
        ".strings": get_strings_from_ios,
        ".xml": get_strings_from_xml,
        ".pdf": get_strings_from_pdf,
    }

    if input_filepath.suffix in [".strings", ".xml"]:
        return conversion_functions[input_filepath.suffix](
            input_filepath, with_comments
        )
    else:
        return conversion_functions[input_filepath.suffix](input_filepath)


def to_google_sheets(
    input_filepath: Path,
    sheet_name: str,
    credentials_filepath: Path,
    with_comments: bool = False,
):
    """
    Writes the extracted strings from the input filepath to an existing Google
    spreadsheet. The spreadsheet must be shared with the service account's email.

    :param input_filepath: File to extract the strings from
    :type input_filepath: Path
    :param sheet_name: Name of the spreadsheet to write to
    :type sheet_name: str
    :param credentials_filepath: Path to the service_account.json in order to be able
        to access the sheet in the user's Google account
    :type credentials_filepath: Path
    :param with_comments: True if the user wants to include comments from
        .strings/.xml to the sheet
    :type with_comments: bool
    """

    strings = get_strings(input_filepath, with_comments)

    client = gspread.service_account(filename=credentials_filepath)

    try:
        spreadsheet = client.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        raise ValueError(
            f"Spreadsheet '{sheet_name}' not found. Create it in Google Sheets and "
            f"share it with the `client_email` from your `service_account.json`."
        ) from None

    sheet = spreadsheet.sheet1

    # Replace the existing data with the strings in a single request
    sheet.clear()
    sheet.update([["NAME", "VALUE"], *[[name, value] for name, value in strings]])


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


def to_xlsx(strings: List[Tuple[str, str]], output_filepath: Path):
    """
    Formats strings to a .xlsx file

    :param strings: Strings extracted from a supported file
    :type strings: List[Tuple[str, str]]
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


def to_ods(strings: List[Tuple[str, str]], output_filepath: Path):
    """
    Formats strings to a .ods file

    :param strings: Strings extracted from a supported file
    :type strings: List[Tuple[str, str]]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    doc = ezodf.newdoc(doctype="ods", filename=str(output_filepath))
    # Don't create a `.bak` file when overwriting an existing file
    doc.backup = False
    sheet = ezodf.Sheet("Sheet1", size=(len(strings) + 1, 2))
    doc.sheets += sheet

    # Write the header row
    sheet[0, 0].set_value("NAME")
    sheet[0, 1].set_value("VALUE")

    # Write the data to the sheet
    for i, (name, value) in enumerate(strings, start=1):
        sheet[i, 0].set_value(name)
        sheet[i, 1].set_value(value)

    doc.save()


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
        file.write("\n")


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


def to_html(strings: List[Tuple[str, str]], output_filepath: Path):
    """
    Formats strings to a .html file

    :param strings: Strings extracted from a supported file
    :type strings: List[Tuple[str, str]]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    # Create an HTML file
    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html>\n")
        file.write("<head>\n")
        file.write('\t<meta charset="UTF-8">\n')
        file.write("</head>\n")
        file.write("<body>\n")
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
            file.write(f"\t\t\t<td>{html.escape(name, quote=False)}</td>\n")
            file.write(f"\t\t\t<td>{html.escape(value, quote=False)}</td>\n")
            file.write("\t\t</tr>\n")

        file.write("\t</tbody>\n")
        file.write("</table>\n")
        file.write("</body>\n")
        file.write("</html>\n")


def to_ios(strings: List[Tuple[str, str]], output_filepath: Path):
    """
    Formats strings to a .strings file

    :param strings: Strings extracted from a supported file
    :type strings: List[Tuple[str, str]]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    with open(output_filepath, "w", encoding="utf-8") as file:
        for name, value in strings:
            file.write(f'"{_escape_ios(name)}" = "{_escape_ios(value)}";\n')


def to_android(strings: List[Tuple[str, str]], output_filepath: Path):
    """
    Formats strings to a .xml file

    :param strings: Strings extracted from a supported file
    :type strings: List[Tuple[str, str]]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        file.write("<resources>\n")
        for name, value in strings:
            file.write(
                f'\t<string name="{html.escape(name)}">'
                f"{_to_android_value(value)}</string>\n"
            )

        file.write("</resources>\n")


def to_pdf(strings: List[Tuple[str, str]], output_filepath: Path):
    """
    Formats strings to a .pdf file

    :param strings: Strings extracted from a supported file
    :type strings: List[Tuple[str, str]]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    def add_font(font_name, size=12):
        root_dir = Path(__file__).parent
        # Ignore the following warning when adding a font already added:
        # UserWarning: Core font or font already added 'dejavusanscondensed': doing
        # nothing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            pdf.add_font(fname=str(root_dir / f"assets/fonts/{font_name}.ttf"))
        pdf.set_font(font_name, size=size)

    # Create a new PDF file
    pdf = FPDF(orientation="P", format="A4")
    pdf.add_page()
    pdf.set_font("helvetica", "B", 12)

    # Embed the strings so they can be read back losslessly by get_strings_from_pdf
    pdf.embed_file(
        bytes=json.dumps(
            [{"name": name, "value": value} for name, value in strings],
            ensure_ascii=False,
        ).encode("utf-8"),
        basename=PDF_EMBEDDED_FILENAME,
        mime_type="application/json",
    )

    # Cell properties
    c_width = 95
    c_height = 10

    # Add headers to table
    pdf.cell(c_width, c_height, "NAME", border=1)
    pdf.cell(c_width, c_height, "VALUE", border=1)
    pdf.ln()

    detector = _get_language_detector()
    unsupported_values = []

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
                    language = detector.detect_language_of(string[j])
                    if language is not None:
                        language_code = language.iso_code_639_1.name.lower()

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
                        add_font("Latha")
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

                # The font has no glyphs for some characters of the string
                if any(
                    ord(char) not in pdf.current_font.cmap
                    for char in string[j]
                    if not char.isspace()
                ):
                    unsupported_values.append(string[j])

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
                unsupported_values.append(string[j])

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

    if unsupported_values:
        errors_filepath = output_filepath.parent / f"{output_filepath.stem}-errors.txt"
        with open(errors_filepath, "w", encoding="utf-8") as f:
            for value in unsupported_values:
                f.write(f"{value} not supported\n")

        print(
            f"{ConsoleStyle.YELLOW}{len(unsupported_values)} string(s) could not be "
            f"rendered in the PDF. See {errors_filepath}{ConsoleStyle.END}"
        )


def to_md(strings: List[Tuple[str, str]], output_filepath: Path):
    """
    Formats strings to a .md file

    :param strings: Strings extracted from a supported file
    :type strings: List[Tuple[str, str]]
    :param output_filepath: The path where the generated file will be saved.
    :type output_filepath: Path
    """

    with open(output_filepath, "w", encoding="utf-8") as f:
        # Write each string to the Markdown file in a table format
        f.write("| NAME | VALUE |\n")
        f.write("| ----------- | ----------- |\n")
        for name, value in strings:
            f.write(f"| {_escape_md(name)} | {_escape_md(value)} |\n")


# GET STRINGS FROM


def get_strings_from_csv(csv_filepath: Path):
    """
    Extract data from a CSV file with NAME and VALUE columns and return it as a
    list of tuples.

    :param csv_filepath: The path to the input CSV file.
    :type csv_filepath: Path
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Initialize a list to hold the tuples
    data = []

    # Open the CSV file and read its contents
    with open(csv_filepath, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        # Iterate over the rows in the CSV file
        for row in csv_reader:
            name, value = row
            data.append((name, value))

    return data


def get_strings_from_xlsx(sheet_filepath: Path):
    """
    Extract data from an Excel file with NAME and VALUE columns and return it as a list
    of tuples.

    :param sheet_filepath: The path to the input Excel file.
    :type sheet_filepath: str
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Load the workbook and select the active sheet
    workbook = openpyxl.load_workbook(sheet_filepath)
    sheet = workbook.active

    # Initialize a list to hold the tuples
    data = []

    # Iterate over the rows in the sheet starting from the second row to skip the header
    for row in sheet.iter_rows(min_row=2, values_only=True):
        name, value = row
        data.append((name, value))

    return data


def get_strings_from_ods(ods_filepath: Path) -> List[Tuple[str, str]]:
    """
    Extract data from an OpenDocument Spreadsheet (ODS) file with NAME and VALUE columns
    and return it as a list of tuples.

    :param ods_filepath: The path to the input ODS file.
    :type ods_filepath: str
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Initialize a list to hold the tuples
    data = []

    # Load the ODS file
    doc = ezodf.opendoc(str(ods_filepath))

    # Get the first sheet
    sheet = doc.sheets[0]

    # Iterate over the rows in the sheet, skipping the header
    for i, row in enumerate(sheet.rows()):
        if i == 0:
            continue

        # Extract NAME and VALUE from each row
        name, value = [cell.value for cell in row[:2]]
        data.append((name, value))

    return data


def get_strings_from_md(
    md_filepath: Path, delimiter: str = "|"
) -> List[Tuple[str, str]]:
    """
    Extract data from a Markdown file with a table containing NAME and VALUE columns and
    return it as a list of tuples.

    :param md_filepath: The path to the input Markdown file.
    :type md_filepath: Path
    :param delimiter: The delimiter used in the Markdown table, defaults to '|'.
    :type delimiter: str, optional
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Initialize a list to hold the tuples
    data = []

    # Open the Markdown file and read its contents
    with open(md_filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Find the start and end indices of the table
    start_index = None
    end_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith(delimiter):
            start_index = i
            break
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip().startswith(delimiter):
            end_index = i
            break

    # Split on delimiters that are not escaped with a backslash
    split_pattern = rf"(?<!\\){re.escape(delimiter)}"

    # Extract data from the table, skipping the first two lines (header)
    if start_index is not None and end_index is not None:
        for row in lines[start_index + 2 : end_index + 1]:
            # Split the line by the delimiter and extract NAME and VALUE
            parts = re.split(split_pattern, row.strip())[1:-1]
            if len(parts) >= 2:
                name, value = parts[:2]
                data.append((_unescape_md(name.strip()), _unescape_md(value.strip())))

    return data


def get_strings_from_json(json_filepath: Path) -> List[Tuple[str, str]]:
    """
    Extract data from a JSON file with objects containing NAME and VALUE fields and
    return it as a list of tuples.

    :param json_filepath: The path to the input JSON file.
    :type json_filepath: Path
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Initialize a list to hold the tuples
    data = []

    # Open the JSON file and load its contents
    with open(json_filepath, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Iterate over each object in the JSON data
    for record in json_data:
        if "name" in record and "value" in record:
            data.append((record["name"], record["value"]))

    return data


def get_strings_from_yaml(yaml_filepath: Path) -> List[Tuple[str, str]]:
    """
    Extract data from a YAML file with objects containing NAME and VALUE fields and
    return it as a list of tuples.

    :param yaml_filepath: The path to the input YAML file.
    :type yaml_filepath: Path
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Initialize a list to hold the tuples
    data = []

    # Open the YAML file and load its contents
    with open(yaml_filepath, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    # Iterate over each key-value pair in the YAML data
    for key, value in yaml_data.items():
        data.append((key, value))

    return data


def get_strings_from_html(html_filepath: Path) -> List[Tuple[str, str]]:
    """
    Extract data from an HTML file with a table containing NAME and VALUE columns and
    return it as a list of tuples.

    :param html_filepath: The path to the input HTML file.
    :type html_filepath: Path
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Open the HTML file and read its contents
    with open(html_filepath, "r", encoding="utf-8") as file:
        html_content = file.read()

    parser = _HTMLTableParser()
    parser.feed(html_content)
    parser.close()

    # Rows with fewer than two cells (e.g. the header row) are skipped
    return [(row[0], row[1]) for row in parser.rows if len(row) >= 2]


def get_strings_from_ios(
    ios_filepath: Path, with_comments: bool = False
) -> List[Tuple[str, str]]:
    """
    Get strings from the .strings file.

    :param ios_filepath: .strings file to extract the strings
    :type ios_filepath: Path
    :param with_comments: True if the user wants to include comments from
        the .strings to the output file
    :type with_comments: bool
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Open the strings file
    with open(ios_filepath, "r", encoding="utf-8") as file:
        strings_data = file.read()

    strings = _parse_ios_strings(strings_data, with_comments)

    if len(strings) >= 1:
        return strings
    else:
        raise ValueError("The file provided is not a valid .strings file.")


def get_strings_from_xml(
    xml_filepath: Path, with_comments: bool = False
) -> List[Tuple[str, str]]:
    """
    Get strings from the Android .xml file.

    `<plurals>` and `<string-array>` resources are not supported and are skipped.

    :param xml_filepath: .xml file to extract the strings
    :type xml_filepath: Path
    :param with_comments: True if the user wants to include comments from
        the .xml to the output file
    :type with_comments: bool
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """

    # Open the strings file
    with open(xml_filepath, "rb") as file:
        strings_data = file.read()

    try:
        root = etree.fromstring(strings_data.strip())
    except etree.XMLSyntaxError:
        raise ValueError("The file provided is not a valid .xml file.") from None

    strings = []
    skipped_resources = 0

    if root.tag == "resources":
        for node in root:
            if node.tag is etree.Comment:
                if with_comments:
                    strings.extend(_parse_commented_android_strings(node.text or ""))
            elif node.tag == "string" and node.get("name") is not None:
                strings.append((node.get("name"), _get_android_value(node)))
            elif node.tag in ["plurals", "string-array"]:
                skipped_resources += 1

    if skipped_resources:
        print(
            f"{ConsoleStyle.YELLOW}Skipped {skipped_resources} <plurals>/"
            f"<string-array> resource(s) in {xml_filepath} because they are not "
            f"supported.{ConsoleStyle.END}"
        )

    if len(strings) >= 1:
        return strings
    else:
        raise ValueError("The file provided is not a valid .xml file.")


def get_strings_from_pdf(pdf_filepath: Path) -> List[Tuple[str, str]]:
    """
    Extract data from a PDF file with a table containing NAME and VALUE columns and
    return it as a list of tuples.

    PDFs generated by this package embed the original strings, which are read
    losslessly. For any other PDF, the strings are extracted from the text of the
    table, which only works for single-line values.

    :param pdf_filepath: The path to the input PDF file.
    :type pdf_filepath: Path
    :return: A list of tuples where each tuple contains a NAME and VALUE.
    :rtype: List[Tuple[str, str]]
    """
    # Initialize a list to hold the tuples
    data = []

    # Create a PdfReader object
    pdf_reader = PdfReader(pdf_filepath)

    embedded_files = pdf_reader.attachments.get(PDF_EMBEDDED_FILENAME)
    if embedded_files:
        records = json.loads(embedded_files[0].decode("utf-8"))
        return [(r["name"], r["value"]) for r in records]

    # Extract text from each page
    for page_number, page in enumerate(pdf_reader.pages):
        text = page.extract_text()

        # Find patterns for table rows
        rows = text.split("\n")

        # Skip the header
        if page_number == 0:
            rows = rows[1:]

        for row in rows:
            match = re.match(r"(\S+)\s+(.*)", row.strip())
            if match:
                name, value = match.groups()
                data.append((name.strip(), value.strip()))

    return data


# HELPERS


@lru_cache(maxsize=1)
def _get_language_detector():
    return (
        LanguageDetectorBuilder.from_all_languages()
        .with_preloaded_language_models()
        .build()
    )


# iOS

# Matches, in order of appearance, block comments, line comments and
# `"name" = "value";` entries.
_IOS_TOKEN_PATTERN = re.compile(
    r"/\*(?P<block>.*?)\*/"
    r"|//(?P<line>[^\n]*)"
    r'|"(?P<name>(?:[^"\\]|\\.)*)"\s*=\s*"(?P<value>(?:[^"\\]|\\.)*)"\s*;',
    re.DOTALL,
)

_IOS_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "0": "\0"}


def _parse_ios_strings(data: str, with_comments: bool) -> List[Tuple[str, str]]:
    strings = []

    for match in _IOS_TOKEN_PATTERN.finditer(data):
        if match.group("name") is not None:
            strings.append(
                (
                    _unescape_ios(match.group("name")),
                    _unescape_ios(match.group("value")),
                )
            )
        elif with_comments:
            comment = match.group("block") or match.group("line") or ""
            strings.extend(_parse_ios_strings(comment, with_comments=False))

    return strings


def _unescape_ios(value: str) -> str:
    def replace(match):
        escaped = match.group(1)
        if escaped[0] in "uU" and len(escaped) > 1:
            return chr(int(escaped[1:], 16))
        return _IOS_ESCAPES.get(escaped, escaped)

    return re.sub(r"\\([uU][0-9a-fA-F]{4}|.)", replace, value, flags=re.DOTALL)


def _escape_ios(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )


# Android

_ANDROID_ESCAPES = {"n": "\n", "t": "\t"}


def _get_android_value(element) -> str:
    """
    Returns the value of a `<string>` element. Values with inline markup (e.g.
    `<b>bold</b>`) are returned verbatim, as they appear in the file. Otherwise, the
    XML entities and Android escape sequences are decoded.
    """

    if len(element):
        inner_xml = element.text and html.escape(element.text, quote=False) or ""
        for child in element:
            inner_xml += etree.tostring(child, encoding="unicode", with_tail=True)
        return inner_xml

    return _unescape_android(element.text or "")


def _parse_commented_android_strings(comment: str) -> List[Tuple[str, str]]:
    try:
        root = etree.fromstring(f"<resources>{comment}</resources>")
    except etree.XMLSyntaxError:
        # The comment is not a commented out string
        return []

    return [
        (node.get("name"), _get_android_value(node))
        for node in root
        if node.tag == "string" and node.get("name") is not None
    ]


def _unescape_android(value: str) -> str:
    # Values wrapped in unescaped double quotes are taken literally
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"' and value[-2] != "\\":
        value = value[1:-1]

    def replace(match):
        escaped = match.group(1)
        if escaped[0] == "u" and len(escaped) > 1:
            return chr(int(escaped[1:], 16))
        return _ANDROID_ESCAPES.get(escaped, escaped)

    return re.sub(r"\\(u[0-9a-fA-F]{4}|.)", replace, value, flags=re.DOTALL)


def _escape_android(value: str) -> str:
    value = (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )

    # `@` and `?` at the start of a value are resource references
    if value.startswith(("@", "?")):
        value = "\\" + value

    return html.escape(value, quote=False)


def _to_android_value(value: str) -> str:
    """
    Returns the value ready to be written inside a `<string>` element. Values with
    well-formed inline markup (as returned by `_get_android_value`) are written
    verbatim.
    """

    if "<" in value:
        try:
            if len(etree.fromstring(f"<string>{value}</string>")):
                return value
        except etree.XMLSyntaxError:
            pass

    return _escape_android(value)


# Markdown


def _escape_md(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r\n", "<br>")
        .replace("\n", "<br>")
    )


def _unescape_md(value: str) -> str:
    return re.sub(r"\\(.)|<br>", lambda m: m.group(1) or "\n", value, flags=re.DOTALL)


# HTML


class _HTMLTableParser(HTMLParser):
    """Collects the text of the `<td>` cells of every `<tr>` row."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: List[List[str]] = []
        self._row = None
        self._cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag == "td" and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag):
        if tag == "td" and self._cell is not None:
            self._row.append("".join(self._cell))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)
