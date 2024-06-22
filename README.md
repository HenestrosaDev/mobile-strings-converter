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
			Convert Android & iOS string files to any supported file type, and vice versa.
		</p>
		<p>
			<a href="https://pypi.org/project/mobile-strings-converter/">
				<img 
					alt="PyPI version" 
					src="https://img.shields.io/pypi/v/mobile-strings-converter" 
				/>
			</a>
			<a href="https://pypi.org/project/mobile-strings-converter/">
				<img 
					alt="Python versions support" 
					src="https://img.shields.io/pypi/pyversions/mobile-strings-converter" 
				/>
			</a>
			<br />
			<a href="https://github.com/HenestrosaDev/mobile-strings-converter/actions/workflows/build.yaml">
				<img 
					alt="GitHub action: Build" 
					src="https://github.com/HenestrosaDev/mobile-strings-converter/actions/workflows/build.yaml/badge.svg" 
				/>
			</a>
			<a href="https://codecov.io/gh/HenestrosaDev/mobile-strings-converter/">
				<img 
					alt="Codecov" 
					src="https://codecov.io/gh/HenestrosaDev/mobile-strings-converter/branch/main/graph/badge.svg" 
				/>
			</a>
			<a href="https://github.com/HenestrosaDev/mobile-strings-converter/blob/main/LICENSE">
				<img 
					alt="License" 
					src="https://img.shields.io/github/license/HenestrosaDev/mobile-strings-converter" 
				/>
			</a>
			<br />
			<a href="https://github.com/HenestrosaDev/mobile-strings-converter/graphs/contributors">
				<img 
					alt="GitHub Contributors" 
					src="https://img.shields.io/github/contributors/HenestrosaDev/mobile-strings-converter" 
				/>
			</a>
			<a href="https://github.com/HenestrosaDev/mobile-strings-converter/issues">
				<img 
					alt="Issues" 
					src="https://img.shields.io/github/issues/HenestrosaDev/mobile-strings-converter" 
				/>
			</a>
			<a href="https://github.com/HenestrosaDev/mobile-strings-converter/pulls">
				<img 
					alt="GitHub pull requests" 
					src="https://img.shields.io/github/issues-pr/HenestrosaDev/mobile-strings-converter" 
				/>
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
- [Troubleshooting](#troubleshooting)
	- [iOS](#ios)
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
a Python script to do this with any file type.

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
	<summary>ASCII directory structure</summary>

```
/
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
│   │   dependabot.yml
│   │
│   ├───ISSUE_TEMPLATE
│   │       bug_report_template.md
│   │       feature_request_template.md
│   │
│   ├───PULL_REQUEST_TEMPLATE
│   │       pull_request_template.md
│   │
│   └───workflows
│           build.yaml
│           publish.yaml
│
├───docs
│       icon.png
│
├───src
│   └───mobile_strings_converter
│       │   console_style.py
│       │   converter.py
│       │   __init__.py
│       │   __main__.py
│       │
│       └───assets
│           └───fonts
│                   Aakar.ttf
│                   AnekTelugu-VariableFont_wdth,wght.ttf
│                   DejaVuSansCondensed.ttf
│                   Eunjin.ttf
│                   fireflysung.ttf
│                   gargi.ttf
│                   Gurvetica_a8_Heavy.ttf
│                   Latha.ttf
│                   Waree.ttf
│
└───tests
    │   base_tests.py
    │   test_android.py
    │   test_csv.py
    │   test_get_strings.py
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
| :---------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- | :------ |
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

To convert one file to another file:

```
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -f *.[SUPPORTED_FILE_TYPE]
```

---

To include the comments of the `.xml`/`.strings` input file in the output file, add the `-p` (also `--print-comments`) flag. Note that it will be ignored for other input file types.

```
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -f *.[SUPPORTED_FILE_TYPE] -p
```

---

To convert multiple files at once and save them to the specified directory passed in the `-d` flag, use the`-t` flag followed by the desired file type extension (e.g., `.json`). Note that the program will create the directory if it doesn't exist.

```
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] *.[SUPPORTED_FILE_TYPE] *.[SUPPORTED_FILE_TYPE] -d [DIR_PATH] -t [TARGET_TYPE]
```

---

To convert supported files in a directory and its subdirectories and save them to a directory:

```
python path/to/mobile_strings_converter.py [INPUT_DIR_PATH] -d [OUTPUT_DIR_PATH] -t [TARGET_TYPE]
```

---

To convert supported files in multiple directories and their subdirectories and save them to a directory:

```
python path/to/mobile_strings_converter.py [INPUT_DIR_PATH_1] [INPUT_DIR_PATH_2] [INPUT_DIR_PATH_3] -d [OUTPUT_DIR_PATH] -t [TARGET_TYPE]
```

---

For multiple file inputs and directories, the name of the files will be the same as the input file. For example, if there is a file named `spanish.xml` in a directory, the output file name will be `spanish.[TARGET_TYPE]`

See the [Generating a Spreadsheet in Google Sheets](#generating-a-spreadsheet-in-google-sheets) section to create a spreadsheet in your Google account.

---

#### Script Flags

| Flag                        | Description                                                                                                                                                                                                                                       |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-h` or `--help`            | Displays help text for the program.                                                                                                                                                                                                               |
| `-f` or `--output-filepath` | Path to save the converted file. Only works if only one input file is provided. The file extension can be chosen from [the list of supported file types](#file-types-supported).                                                                  |
| `-d` or `--output-dir`      | Directory where the converted files will be saved. Compatible with single and multiple input files as well as directories. The specified directory will be created if it does not already exist.                                                  |
| `-t` or `--target-type`     | Target file type to convert the files (e.g., .pdf, .json). Required if multiple file paths or the `--output-dir` is specified.                                                                                                                    |
| `-g` or `--google-sheets`   | If provided, a Google spreadsheet will be created in your Google account. You must pass the `service_account.json` with the `-c` flag.                                                                                                            |
| `-c` or `--credentials`     | `service_account.json` filepath. Mandatory if you want to generate a spreadsheet in your Google account. You can learn how to generate it in the [Generating a Spreadsheet in Google Sheets](#generating-a-spreadsheet-in-google-sheets) section. |
| `-p` or `--print-comments`  | If provided, the commented strings will be printed in the output file. Only valid for input files of type `.xml` or `.strings`. Otherwise it is ignored.                                                                                          |

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

```
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -g -c path/to/service_account.json
```

If you want to generate an output file along with the spreadsheet, run this:

```
python path/to/mobile_strings_converter.py *.[SUPPORTED_FILE_TYPE] -g -c path/to/service_account.json -o *.[SUPPORTED_FILE_TYPE]
```

The name of the sheet will be the same as the name of the input file.

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

## Troubleshooting

### iOS

You may encounter this error on iOS when using a generated `.strings` file:

```
validation failed: Couldn't parse property list because the input data was in an invalid format
```

This is because the input file has double quotes in some NAME or VALUE. To identify the line with the error, you have to do the following on macOS:

1. `cd` into your project root.
2. `cd [LANGUAGE_CODE].lproj` (e.g., `cd es.lproj`)
3. `plutil -lint Localizable.strings`

When you run step 3, you will either get an error telling you what is wrong with your file, or you will be told that the file is correct.

✅ Success output example:

```
╰─➤  plutil -lint Localizable.strings
Localizable.strings: OK
```

❌ Error output example:

```
╰─➤  plutil -lint Localizable.strings
2024-06-05 11:04:08.614 plutil[86874:16115488] CFPropertyListCreateFromXMLData(): Old-style plist parser: missing semicolon in dictionary on line 293. Parsing will be abandoned. Break on _CFPropertyListMissingSemicolon to debug.
Localizable.strings: Unexpected character " at line 1
```

> [!NOTE]
> The last line of the `plutil` output on error will always be `Unexpected character at line 1`. However, the real error is in the line above, where it says that the error is on line 293 due to a missing semicolon.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Add support for converting a file (not `.xml` or `.strings`) into a strings resource file (`.xml` or `.strings`).
- [x] Add support for multiple files input.
- [x] Add support for accepting the path to a directory as input.
- [x] Add support for accepting the path to a directory as output.
- [ ] Make brew (macOS) formula.
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
