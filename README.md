<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I am using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img 
        src="docs/icon.png" 
        alt="Logo" 
        width="156" 
        height="156"
    >
    <h1 align="center">Mobile Strings Converter</h1>
    <p align="center">
        A Python package that converts Android & iOS strings files to any supported file type, and vice versa.
    </p>
    <p>
        <a href="https://pypi.org/project/mobile-strings-converter/">
          <img alt="PyPI version" src="https://img.shields.io/pypi/v/mobile-strings-converter" />
        </a>
        <a href="https://pypi.org/project/mobile-strings-converter/">
          <img alt="Python versions support" src="https://img.shields.io/pypi/pyversions/mobile-strings-converter" />
        </a>
        <br />
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/actions/workflows/build.yaml">
          <img alt="GitHub action: Build" src="https://github.com/HenestrosaDev/mobile-strings-converter/actions/workflows/build.yaml/badge.svg" />
        </a>
        <a href="https://codecov.io/gh/HenestrosaDev/mobile-strings-converter/">
          <img alt="Codecov" src="https://codecov.io/gh/HenestrosaDev/mobile-strings-converter/branch/main/graph/badge.svg" />
        </a>
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/blob/main/LICENSE">
          <img alt="License" src="https://img.shields.io/github/license/HenestrosaDev/mobile-strings-converter" />
        </a>
        <br />
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/graphs/contributors">
          <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/HenestrosaDev/mobile-strings-converter" />
        </a>
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/HenestrosaDev/mobile-strings-converter" />
        </a>
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/pulls">
          <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/HenestrosaDev/mobile-strings-converter" />
        </a>
    </p>
    <p>
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/issues/new/choose">
            Report Bug
        </a> 
        · 
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/issues/new/choose">
            Request Feature
        </a> 
        · 
        <a href="https://github.com/HenestrosaDev/mobile-strings-converter/discussions">
            Ask Question
        </a>
    </p>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [File Types Supported](#file-types-supported) 
  - [Project Structure](#project-structure)
  - [Built With](#built-with)
- [Release Files](#release-files)
- [Getting Started](#getting-started)
  - [Script Installation](#script-installation)
  - [Package Installation](#package-installation)
- [Usage](#usage)
  - [Running the Program](#running-the-program)
    - [Script Flags](#script-flags)
  - [Using the Package in Your Project](#using-the-package-in-your-project)
  - [Generating a Spreadsheet in Google Sheets](#generating-a-spreadsheet-in-google-sheets)
    - [Setting Up a Google Account](#setting-up-a-google-account)
    - [Using the `to_google_sheets` Function in Your Project](#using-the-to_google_sheets-function-in-your-project)
- [Notes](#notes)
  - [Indic Languages Supported by PDF Files](#indic-languages-supported-by-pdf-files)
  - [Languages Not Supported by PDF Files](#languages-not-supported-by-pdf-files)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)
- [Support](#support)

<!-- ABOUT THE PROJECT -->

## About the Project

I have tried to do the whole process of converting a strings resource file into a spreadsheet in Google Sheets by hand, and although you can do it with the **Data > Split text to columns** option, 
it is a waste of time to generate the spreadsheet manually. Also, you are limited to spreadsheet files only. For this reason, I decided to create a time-efficient solution that consists of running 
a Python script in order to do this that with any file type.

In addition to being able to run this script on its own, it can also be installed as a package via **PyPI** (more information on how to install it [here](#use-the-package-in-your-project)).

<!-- FILE TYPES SUPPORTED -->

### File Types Supported

- Android strings format (`*.xml`)
- CSV
- Google Sheets support
- HTML
- iOS strings format (`*.strings`)
- JSON
- MD
- ODS
- PDF
- XLSX
- YAML

<!-- PROJECT STRUCTURE -->

### Project Structure

<details>
  <summary>ASCII folder structure</summary>

```
│   .gitignore
│   .pre-commit-config.yaml
│   LICENSE
│   poetry.lock 
│   pyproject.toml
│   README.md
│   requirements.txt
│   requirements-dev.txt
│
├───.github
│   │   CONTRIBUTING.md
│   │
│   ├───ISSUE_TEMPLATE
│   │       bug_report_template.md
│   │       feature_request_template.md
│   │
│   └───PULL_REQUEST_TEMPLATE
│           pull_request_template.md
│
├───docs
│       icon.png
│
├───src
│   ├───mobile_strings_converter
│   │       console_style.py
│   │       converter.py
│   │       __init__.py
│   │       __main__.py
│   │
│   ├───assets
│   │       └───fonts
│   │               Aakar.ttf
│   │               AnekTelugu-VariableFont_wdth,wght.ttf
│   │               DejaVuSansCondensed.ttf
│   │               Eunjin.ttf
│   │               fireflysung.ttf
│   │               gargi.ttf
│   │               Gurvetica_a8_Heavy.ttf
│   │               Latha.ttf
│   │               Waree.ttf
│   │
│   ├───controller
│   │       main_controller.py
│   │       __init__.py
│   │
│   ├───model
│   │       transcription.py
│   │       __init__.py
│   │
│   ├───utils
│   │       constants.py
│   │       i18n.py
│   │       path_helper.py
│   │       __init__.py
│   │
│   └───view
│           main_window.py
│           __init__.py
│
└───tests   
    │   base_tests.py
    │   test_get_strings.py
    │   test_android.py
    │   test_csv.py
    │   test_html.py
    │   test_ios.py
    │   test_json.py
    │   test_md.py
    │   test_ods.py
    │   test_pdf.py
    │   test_xlsx.py
    │   test_yaml.py
    │
    └───files
        ├───input
        │       Localizable.strings
        │       strings.xml
        │
        ├───template-with-comments
        │       Localizable.strings
        │       strings.csv
        │       strings.html
        │       strings.json
        │       strings.md
        │       strings.ods
        │       strings.pdf
        │       strings.xlsx
        │       strings.xml
        │       strings.yaml
        │
        └───template-without-comments
                Localizable.strings
                strings.csv
                strings.html
                strings.json
                strings.md
                strings.ods
                strings.pdf
                strings.xlsx
                strings.xml
                strings.yaml
```
</details>

<!-- BUILT WITH -->

### Built With

- [openpyxl](https://pypi.org/project/openpyxl/) to generate ODS and XLSX files.
- [gspread](https://pypi.org/project/gspread/) to generate spreadsheets in Google Sheets.
- [protobuf](https://pypi.org/project/oauth2client/) is used by `google.oauth2.credentials` to authenticate to the user's Google account in order to create the spreadsheet in Google Sheets. 
- [PyYAML](https://pypi.org/project/PyYAML/) to generate YAML files.
- [arabic-reshaper](https://pypi.org/project/arabic-reshaper/) and [python-bidi](https://pypi.org/project/python-bidi/) to add arabic characters support for PDF files.
- [fpdf2](https://pypi.org/project/fpdf2/) to generate PDF files.
- [lingua-language-detector](https://pypi.org/project/lingua-language-detector/) to recognize the **value** language when writing a PDF in order to know what font to use.  

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- RELEASE FILES -->

## Release Files

| File                                                                                                                                            | Description                                                                                         | Size    |
|:------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|:--------|
| [mobile-strings-converter.zip](https://github.com/HenestrosaDev/mobile-strings-converter/releases/latest/download/mobile-strings-converter.zip) | PDF file support for almost all languages ([see exceptions](#languages-not-supported-by-pdf-files)) | 8.43 MB |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Script Installation

1. Download the `.zip` file from the [latest release](#release-files).
2. (Optional but recommended) Create a Python virtual environment in the project root. If you're using `virtualenv`, you would run `virtualenv venv`.
3. (Optional but recommended) Activate the virtual environment:
   ```bash
   # on Windows
   . venv/Scripts/activate
   # if you get the error `FullyQualifiedErrorId : UnauthorizedAccess`, run this:
   Set-ExecutionPolicy Unrestricted -Scope Process
   # and then . venv/Scripts/activate
   
   # on macOS and Linux
   source venv/Scripts/activate
   ```
4. Open the command line and run `pip install -r path/to/requirements.txt` to install the required packages to run the script.

### Package Installation

Install the PyPI package by running `pip install mobile-strings-converter`.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->

## Usage

### Running the Program

For basic use, you can run the following command:

```bash
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -o *.[SUPPORTED_FILE_TYPE]
```

To include the comments of the `.xml`/`.strings` file in the output file, add the `-p` (also `--print-comments`) flag:

```bash
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -o *.[SUPPORTED_FILE_TYPE] -p
```

See the [Generating a Spreadsheet in Google Sheets](#generating-a-spreadsheet-in-google-sheets) section to create a spreadsheet in your Google account.

#### Script Flags

| Flag                        | Description                                                                                                                                                                                 |
|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h` or `--help`            | Displays help text for the program                                                                                                                                                          |
| `-o` or `--output-filepath` | Specifies the filepath for storing the converted file. The file extension can be chosen from the list of supported file types mentioned [here](#about-the-project).                         |
| `-g` or `--google-sheets`   | Followed by the name of the sheet, creates a new Google Sheets spreadsheet with the specified name.                                                                                         |
| `-c` or `--credentials`     | Followed by the path to your `service_account.json` file is mandatory if you want to generate a spreadsheet in your Google account.                                                         |
| `-p` or `--print-comments`  | The output file will contain all commented strings that were present in the original file (only applicable if the input file is a `.xml` or `.strings` file). Otherwise it will be ignored. |

<p align="right">(<a href="#top">back to top</a>)</p>

### Using the Package in Your Project

After following the steps in the [Getting Started](#getting-started) section, import the package and the wrapper function(s) you want to use: 

```python
# Using the `get_strings` function
from mobile_strings_converter import get_strings  

get_strings(
   input_filepath=Path("strings.xml"), 
   with_comments=True
)
```

### Generating a Spreadsheet in Google Sheets

#### Setting Up a Google Account

Before going further into running the commands to do this, note that you need to generate a `service_account.json` file. Follow these steps to get one:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Go to the **APIs & Services** page, click on **Dashboard** and then click on **Enable APIs and Services**.
4. Search for **Google Sheets API** and enable it.
5. Go to the **Credentials** page, click on **Create credentials**, and then choose **Service account**.
6. Give your service account a name and select a role. For this purpose, you can select **Project -> Editor**.
7. Click on the **Create key** button, select the JSON format and download the `service_account.json` file.
8. Share your Google Sheets file with the email address that is specified in the **client_email** field in the `service_account.json` file.

Alternatively, you can create an `.xlsx` file and open it in Google Sheets if you do not want to go through the hassle of generating the `service_account.json` file.

Once you have the `service_account.json` file, you can create a spreadsheet in Google Sheets by running the following command:

```bash
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -g [SHEET_NAME] -c path/to/service_account.json 
```

If you want to generate an output file along with the spreadsheet, run this:

```bash
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -g [SHEET_NAME] -c path/to/service_account.json -o *.[SUPPORTED_FILE_TYPE]
```

#### Using the `to_google_sheets` Function in Your Project

```python
from mobile_strings_converter import to_google_sheets

to_google_sheets(
    input_filepath=Path("path/to/strings-file"),
    sheet_name="MyProject strings",
    credentials_filepath=Path("path/to/service_account.json"),
    with_comments=True,
)
```

<!-- NOTES -->

## Notes

### Indic Languages Supported by PDF Files

- Hindi
- Marathu
- Oriya
- Tibetan
- Gujarati
- Telugu
- Tamil
- Punjabi

### Languages Not Supported by PDF Files

- Bengali <sub>(not possible to print correctly using [fpdf2](https://pypi.org/project/fpdf2/))</sub>
- Dhivehi <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>
- Kannada <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>
- Khmer <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>
- Lao <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>
- Malayalam <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>
- Meiteilon (manipuri) <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>
- Myanmar burmese <sub>(not possible to print correctly using [fpdf2](https://pypi.org/project/fpdf2/))</sub>
- Odia (Oriya) <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub></sub>
- Sinhala <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>
- Tigrinya <sub>(not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))</sub>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Add support for converting a file (not `.xml` or `.strings`) into a strings resource file (`.xml` or `.strings`).
- [ ] Add support for multiple files input.
- [ ] Add support for accepting the path to a folder as input.
- [ ] Make a web version.

You can propose a new feature creating an [issue](https://github.com/HenestrosaDev/mobile-strings-converter/new/choose).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
Please, read the [CONTRIBUTING.md](https://github.com/HenestrosaDev/mobile-strings-converter/blob/main/.github/CONTRIBUTING.md) file, where you can find more detailed information about how to contribute to the project.

<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/HenestrosaDev/mobile-strings-converter/blob/main/LICENSE) for more information.

<!-- AUTHORS -->

## Authors

- HenestrosaDev <henestrosadev@gmail.com> (José Carlos López Henestrosa)

See also the list of [contributors](https://github.com/HenestrosaDev/mobile-strings-converter/contributors) who participated in this project.

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

I have made use of the following resources to make this project:

- [How to create a Python package](https://mathspp.com/blog/how-to-create-a-python-package-in-2022#how-to-create-a-python-package)

<!-- SUPPORT -->

## Support

Would you like to support the project? That's very kind of you! You can go to my Ko-Fi profile by clicking on the button down below.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/henestrosadev)

<p align="right">(<a href="#top">back to top</a>)</p>
