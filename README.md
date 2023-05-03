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
    <img src="docs/icon.png" alt="Logo" width="156" height="156" style="margin-bottom:-40px">
    <h1 align="center">Mobile Strings Converter</h1>
    <p align="center">
        A Python package that converts Android & iOS strings files to any supported file type.
        <br />
        <br />
        <a href="https://pypi.org/project/mobile-strings-converter/">
          <img alt="PyPI version" src="https://img.shields.io/pypi/v/mobile-strings-converter" />
        </a>
        <a href="https://pypi.org/project/mobile-strings-converter/">
          <img alt="Python versions support" src="https://img.shields.io/pypi/pyversions/mobile-strings-converter" />
        </a>
        <br />
        <a href="https://github.com/HenestrosaConH/mobile-strings-converter/actions/workflows/build.yaml">
          <img alt="GitHub action: Build" src="https://github.com/HenestrosaConH/mobile-strings-converter/actions/workflows/build.yaml/badge.svg" />
        </a>
        <a href="https://codecov.io/gh/HenestrosaConH/mobile-strings-converter/">
          <img alt="Codecov" src="https://codecov.io/gh/HenestrosaConH/mobile-strings-converter/branch/main/graph/badge.svg" />
        </a>
        <a href="https://github.com/HenestrosaConH/mobile-strings-converter/blob/main/LICENSE">
          <img alt="License" src="https://img.shields.io/github/license/HenestrosaConH/mobile-strings-converter" />
        </a>
        <br />
        <a href="https://github.com/HenestrosaConH/mobile-strings-converter/graphs/contributors">
          <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/HenestrosaConH/mobile-strings-converter" />
        </a>
        <a href="https://github.com/HenestrosaConH/mobile-strings-converter/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/HenestrosaConH/mobile-strings-converter" />
        </a>
        <a href="https://github.com/HenestrosaConH/mobile-strings-converter/pulls">
          <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/HenestrosaConH/mobile-strings-converter" />
        </a>
        <br />
        <br />
        <a href="https://github.com/HenestrosaConH/mobile-strings-converter/issues/new/choose">Report Bug</a> · <a href="https://github.com/HenestrosaConH/mobile-strings-converter/issues/new/choose">Request Feature</a> · <a href="https://github.com/HenestrosaConH/mobile-strings-converter/discussions">Ask Question</a>
    </p>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Project Structure](#project-structure)
  - [Built With](#built-with)
- [Release Files](#release-files)
- [Getting Started](#getting-started)
  - [To Download the Program](#to-download-the-program) 
  - [To Import the Package Into Your Project](#to-import-the-package-into-your-project)
  - [To Open the Code](#to-open-the-code)
- [Usage](#usage)
  - [To Run the Program](#to-run-the-program)
  - [To Use the Package in Your Project](#to-use-the-package-in-your-project)
  - [To Generate a Spreadsheet in Google Sheets](#to-generate-a-spreadsheet-in-google-sheets)
  - [Script Flags](#script-flags)
- [Notes](#notes)
  - [List of Indic Languages Supported by PDF files](#list-of-indic-languages-supported-by-pdf-files)
  - [List of Languages Not Supported by PDF files](#list-of-languages-not-supported-by-pdf-files)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)
- [Support](#support)

<!-- ABOUT THE PROJECT -->

## About the Project

I tried to do the whole process of converting a strings resource file into a spreadsheet in Google Sheets by hand and, even though you can do it with the option **Data > Split text to columns**, 
it involves wasting your time generating the spreadsheet manually. Due to that, I decided to build a time-efficient solution, which consists on running a Python script in order to achieve that with any file type.

Moreover, not only this script can be executed on its own, it also can be installed as a package via **PyPI** (more information [here](#to-import-the-package-into-your-project) about how to install it).

The file types supported by the package are the following:
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
    │   test_to_android.py
    │   test_to_csv.py
    │   test_to_html.py
    │   test_to_ios.py
    │   test_to_json.py
    │   test_to_md.py
    │   test_to_ods.py
    │   test_to_pdf.py
    │   test_to_xlsx.py
    │   test_to_yaml.py
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

- [openpyxl](https://pypi.org/project/openpyxl/): To generate ODS and XLSX files.
- [gspread](https://pypi.org/project/gspread/): To generate spreadsheets in Google Sheets.
- [protobuf](https://pypi.org/project/oauth2client/): Used by `google.oauth2.credentials` to authenticate to the user's Google account in order to create the spreadsheet in Google Sheets. 
- [PyYAML](https://pypi.org/project/PyYAML/): To generate YAML files.
- [arabic-reshaper](https://pypi.org/project/arabic-reshaper/) and [python-bidi](https://pypi.org/project/python-bidi/): To add arabic characters support for PDF files.
- [fpdf2](https://pypi.org/project/fpdf2/): To generate PDF files.
- [lingua-language-detector](https://pypi.org/project/lingua-language-detector/): To recognize the **value** language when writing a PDF in order to know what font to use.  

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- RELEASE FILES -->

## Release Files

| File                                                                                                                                                         | Description                                                                                                 | Size      |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|:----------|
| [mobile-strings-converter.zip](https://github.com/HenestrosaConH/mobile-strings-converter/releases/latest/download/mobile-strings-converter.zip)             | Standard language support for PDF files (over 100 languages, including RTL)                                 | 0.32 MB   |
| [mobile-strings-converter-indic.zip](https://github.com/HenestrosaConH/mobile-strings-converter/releases/latest/download/mobile-strings-converter-indic.zip) | PDF file support for Indic languages ([see list](#list-of-indic-languages-supported-by-pdf-files))          | 1.40 MB   |
| [mobile-strings-converter-zh-ja.zip](https://github.com/HenestrosaConH/mobile-strings-converter/releases/latest/download/mobile-strings-converter-zh-ja.zip) | PDF file support for Japanese and Chinese (simplified and traditional)                                      | 7.17 MB   |
| [mobile-strings-converter-ko.zip](https://github.com/HenestrosaConH/mobile-strings-converter/releases/latest/download/mobile-strings-converter-ko.zip)       | PDF file support for Korean                                                                                 | 0.46 MB   |
| [mobile-strings-converter-th.zip](https://github.com/HenestrosaConH/mobile-strings-converter/releases/latest/download/mobile-strings-converter-th.zip)       | PDF file support for Thai                                                                                   | 0.37 MB   |
| [mobile-strings-converter-all.zip](https://github.com/HenestrosaConH/mobile-strings-converter/releases/latest/download/mobile-strings-converter-all.zip)     | PDF file support for almost all languages ([see exceptions](#list-of-languages-not-supported-by-pdf-files)) | 8.43 MB   |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### To Download the Program

1. Download the [release](#release-files) that is best suited to your needs.
2. Open the command line and run `pip install -r path/to/requirements.txt` to install the required packages to execute the script.

### To Import the Package Into Your Project

1. Run `pip install mobile-strings-converter`
2. Import the package and the wrapper function with this line of code: `from mobile_strings_converter import convert_strings`.

### To Open the Code

1. Clone the project with the `git clone https://github.com/HenestrosaConH/mobile-strings-converter.git` command.
2. Open it in your favourite IDE (mine is [PyCharm](https://www.jetbrains.com/pycharm/))

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->

## Usage

### To Run the Program

Run the program
 
```
python path/to/mobile_strings_converter.py <*.xml | *.strings> -o <*.SUPPORTED FILE TYPE EXTENSION>
```

### To Use the Package in Your Project

Once you have followed the steps indicated in the [Getting Started](#getting-started) section, you just have to use the `convert_strings` function. Here is an example:

```python
convert_strings(
    input_filepath=Path("strings.xml"), 
    output_filepath=Path("strings-en.xlsx"), 
    should_print_comments=True
)
```

### To Generate a Spreadsheet in Google Sheets

#### Running the program

Before going further into running the commands to do so, please note that you will have to generate a `service_account.json` file. You can do the following to get one:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Go to the **APIs & Services** page, click on **Dashboard** and then click on **Enable APIs and Services**.
4. Search for **Google Sheets API** and enable it.
5. Go to the **Credentials** page, click on **Create credentials**, and then choose **Service account**.
6. Give your service account a name and select a role. For this purpose, you can select **Project -> Editor**.
7. Click on the **Create key** button, select the JSON format and download the `service_account.json` file.
8. Share your Google Sheets file with the email address that is specified in the **client_email** field in the `service_account.json` file.

Alternatively, you can create an XLSX file and open it in Google Sheets if you do not want to go through the hassle of generating the `service_account.json` file.

Once you have generated the `service_account.json` file, you can generate a spreadsheet in Google Sheets by running the following command:
```
python path/to/mobile_strings_converter.py <*.xml | *.strings> -g <SHEET NAME> -c path/to/service_account.json 
```

If you want to generate an output file along with the spreadsheet, run this:
```
python path/to/mobile_strings_converter.py <*.xml | *.strings> -g <SHEET NAME> -c path/to/service_account.json -o <*.SUPPORTED FILE TYPE EXTENSION>
```

#### Using the Package in Your Project

If you are using the package in your project, here is an example of how to use the `to_google_sheets` function:

```python
from mobile_strings_converter import to_google_sheets

to_google_sheets(
    input_filepath=Path("path/to/strings-file"),
    sheet_name="MyProject strings",
    credentials_filepath=Path("path/to/service_account.json"),
    should_print_comments=True,
)
```

### Script flags

| Flag                        | Description                                                                                                                                                         |
|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h` or `--help`            | Displays help text for the program                                                                                                                                  |
| `-o` or `--output-filepath` | Specifies the filepath for storing the converted file. The file extension can be chosen from the list of supported file types mentioned [here](#about-the-project). |
| `-g` or `--google-sheets`   | Followed by the name of the sheet, creates a new Google Sheets spreadsheet with the specified name.                                                                 |
| `-c` or `--credentials`     | Followed by the path to your `service_account.json` file is mandatory if you want to generate a spreadsheet in your Google account.                                 |
| `-p` or `--print-comments`  | The output file will include any commented strings present in the original file.                                                                                    |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- NOTES -->

## Notes

### List of Indic Languages Supported by PDF files

- Hindi
- Marathu
- Oriya
- Tibetan
- Gujarati
- Telugu
- Tamil
- Punjabi

### List of Languages Not Supported by PDF files

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

- [ ] Add support for multiple `.xml`/`.strings` files input.
- [ ] Add support for converting a file (not `.xml` nor `.strings`) to a strings resource file.
- [ ] Make a web version.

You can propose a new feature creating an [issue](https://github.com/HenestrosaConH/mobile-strings-converter/new/choose).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
Please, read the [CONTRIBUTING.md](https://github.com/HenestrosaConH/mobile-strings-converter/blob/main/.github/CONTRIBUTING.md) file, where you can find more detailed information about how to contribute to the project.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- AUTHORS -->

## Authors

- HenestrosaConH <henestrosaconh@gmail.com> (José Carlos López Henestrosa)

See also the list of [contributors](https://github.com/HenestrosaConH/mobile-strings-converter/contributors) who participated in this project.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

I have made use of the following resources to make this project:

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
- [Img Shields](https://shields.io)
- [How to create a Python package](https://mathspp.com/blog/how-to-create-a-python-package-in-2022#how-to-create-a-python-package)
- [Icon created by Midjourney](https://www.midjourney.com/app/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- SUPPORT -->

## Support

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U5J6COZ)

<p align="right">(<a href="#top">back to top</a>)</p>
