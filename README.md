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
- [Getting Started](#getting-started)
	- [Script Installation](#script-installation)
	- [Package Installation](#package-installation)
- [Usage](#usage)
	- [Running the Program](#running-the-program)
		- [Script Arguments](#script-arguments)
			- [Positional Arguments](#positional-arguments)
            - [Options](#options)
	- [Working With Several Languages](#working-with-several-languages)
	- [Checking Translations](#checking-translations)
	- [Using the Package in Your Project](#using-the-package-in-your-project)
	- [Google Sheets](#google-sheets)
		- [Setting Up a Google Account](#setting-up-a-google-account)
		- [Writing to and Reading From a Spreadsheet](#writing-to-and-reading-from-a-spreadsheet)
		- [Using Google Sheets in Your Project](#using-google-sheets-in-your-project)
- [Notes](#notes)
	- [Android Resources](#android-resources)
	- [Plurals and Arrays](#plurals-and-arrays)
	- [Placeholders](#placeholders)
	- [String Catalogs](#string-catalogs)
	- [PDF Files](#pdf-files)
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

In addition to being able to run this script on its own, it can also be installed as a package via **PyPI** (more information on how to install it [here](#package-installation)).

<!-- FILE TYPES SUPPORTED -->

### File Types Supported

- Android strings format (`*.xml`)
- CSV
- Google Sheets (read and write, requires the `sheets` extra)
- HTML
- iOS strings format (`*.strings`)
- iOS plurals format (`*.stringsdict`)
- Xcode String Catalogs (`*.xcstrings`)
- JSON
- MD
- ODS
- PDF (output only, requires the `pdf` extra)
- XLSX
- YAML

Every file type except `.xml`, `.strings` and `.stringsdict` can hold several languages at once (e.g., a spreadsheet with a column per language). See [Working With Several Languages](#working-with-several-languages).

<!-- PROJECT STRUCTURE -->

### Project Structure

<details>
	<summary>ASCII directory structure</summary>

```
/
│   .gitignore
│   .pre-commit-config.yaml
│   LICENSE
│   pyproject.toml
│   README.md
│   uv.lock
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
│       │   check.py
│       │   console_style.py
│       │   exceptions.py
│       │   files.py
│       │   google_sheets.py
│       │   model.py
│       │   placeholders.py
│       │   py.typed
│       │   __init__.py
│       │   __main__.py
│       │
│       ├───formats
│       │       android.py
│       │       csvfile.py
│       │       html_table.py
│       │       ios.py
│       │       jsonfile.py
│       │       markdown.py
│       │       ods.py
│       │       pdf.py
│       │       stringsdict.py
│       │       table.py
│       │       text.py
│       │       xcstrings.py
│       │       xlsx.py
│       │       yamlfile.py
│       │       __init__.py
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
    │   test_check.py
    │   test_csv.py
    │   test_cli.py
    │   test_files.py
    │   test_formats.py
    │   test_google_sheets.py
    │   test_html.py
    │   test_ios.py
    │   test_json.py
    │   test_md.py
    │   test_ods.py
    │   test_parsing.py
    │   test_pdf.py
    │   test_placeholders.py
    │   test_round_trip.py
    │   test_stringsdict.py
    │   test_xcstrings.py
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
                strings.xlsx
                strings.xml
                strings.yaml
```

</details>

<!-- BUILT WITH -->

### Built With

- [openpyxl](https://pypi.org/project/openpyxl/) to generate XLSX files.
- [ezodf](https://pypi.org/project/ezodf/) to generate ODS files.
- [lxml](https://pypi.org/project/lxml/) to parse Android `.xml` files.
- [PyYAML](https://pypi.org/project/PyYAML/) to generate YAML files.
- [gspread](https://pypi.org/project/gspread/) to read and write spreadsheets in Google Sheets (`sheets` extra).
- [fpdf2](https://pypi.org/project/fpdf2/) to generate PDF files (`pdf` extra).
- [arabic-reshaper](https://pypi.org/project/arabic-reshaper/) and [python-bidi](https://pypi.org/project/python-bidi/) to add arabic characters support for PDF files (`pdf` extra).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Script Installation

1. Download the `.zip` file from the [latest release](https://github.com/HenestrosaDev/mobile-strings-converter/releases/latest/).
2. (Optional but recommended) Create a Python virtual environment in the project root. If you're using `virtualenv`, you would run `virtualenv venv`.
3. (Optional but recommended) Activate the virtual environment:

	 ```bash
	 # on Windows
	 . venv/Scripts/activate
	 # if you get the error `FullyQualifiedErrorId : UnauthorizedAccess`, run this:
	 Set-ExecutionPolicy Unrestricted -Scope Process
	 # and then . venv/Scripts/activate

	 # on macOS and Linux
	 source venv/bin/activate
	 ```

4. Open the command line and run `pip install "path/to/project/root[all]"` to install the required packages and the `mobile-strings-converter` command.

### Package Installation

Install the PyPI package by running `pip install mobile-strings-converter`. It requires Python 3.10 or later and installs the `mobile-strings-converter` command.

Writing PDF files and using Google Sheets need optional dependencies, which you can install as extras:

| EXTRA    | ENABLES                                          | COMMAND                                           |
|:---------|:-------------------------------------------------|:--------------------------------------------------|
| `pdf`    | Writing `.pdf` files                             | `pip install "mobile-strings-converter[pdf]"`     |
| `sheets` | Reading and writing Google Sheets (`-g` and `-G`) | `pip install "mobile-strings-converter[sheets]"`  |
| `all`    | Both of the above                                | `pip install "mobile-strings-converter[all]"`     |

If you use a feature without its extra, the program tells you which one to install.

To install the command in its own environment, use [`uv tool`](https://docs.astral.sh/uv/concepts/tools/) or [`pipx`](https://pipx.pypa.io/), e.g. `uv tool install "mobile-strings-converter[all]"`.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->

## Usage

### Running the Program

To convert one file to another file:

```
mobile-strings-converter *.[SUPPORTED_FILE_TYPE] -f *.[SUPPORTED_FILE_TYPE]
```

---

To include the comments of the `.xml`/`.strings` input file in the output file, add the `-p` (or `--print-comments`) option. Note that it will be ignored for other input file types.

```
mobile-strings-converter *.[SUPPORTED_FILE_TYPE] -f *.[SUPPORTED_FILE_TYPE] -p
```

---

To convert multiple files at once and save them in the specified directory specified with the `-d` option, use the `-t` option followed by the desired file type extension (e.g., `json` or `.json`). Note that the program will create the directory if it doesn't exist.

```
mobile-strings-converter *.[SUPPORTED_FILE_TYPE] *.[SUPPORTED_FILE_TYPE] *.[SUPPORTED_FILE_TYPE] -d [DIR_PATH] -t [TARGET_TYPE]
```

---

To convert supported files in a directory and its subdirectories and save them to a directory:

```
mobile-strings-converter [INPUT_DIR_PATH] -d [OUTPUT_DIR_PATH] -t [TARGET_TYPE]
```

---

To convert supported files in multiple directories and their subdirectories and save them to a directory:

```
mobile-strings-converter [INPUT_DIR_PATH_1] [INPUT_DIR_PATH_2] [INPUT_DIR_PATH_3] -d [OUTPUT_DIR_PATH] -t [TARGET_TYPE]
```

---

For multiple file inputs and directories, the name of the files will be the same as the input file. For example, if there is a file named `spanish.xml` in a directory, the output file name will be `spanish.[TARGET_TYPE]`. When converting a directory, its subdirectory structure is kept in the output directory, so `res/values-es/strings.xml` and `res/values-fr/strings.xml` become `[OUTPUT_DIR_PATH]/values-es/strings.[TARGET_TYPE]` and `[OUTPUT_DIR_PATH]/values-fr/strings.[TARGET_TYPE]`.

See the [Google Sheets](#google-sheets) section to read and write spreadsheets in your Google account, and [Checking Translations](#checking-translations) to find missing translations and mismatched placeholders.

---

#### Script Arguments

A full list of the program command's options are as follows:

##### Positional Arguments

| POSITIONAL ARGUMENT | DESCRIPTION                                                                                                            |
|:--------------------|:-----------------------------------------------------------------------------------------------------------------------|
| `input_paths`       | Files or directory paths of supported files to convert. See [the list of supported file types](#file-types-supported). Not needed with `-G`. |

##### Options

| OPTION                                                  | DESCRIPTION                                                                                                                                                                                                                                                    |
|:--------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h, --help`                                            | Show the help text and exit.                                                                                                                                                                                                                                   |
| `-v, --version`                                         | Show script version info and exit.                                                                                                                                                                                                                             |
| `-f FILE_PATH, --output-file FILE_PATH`                 | File path to save the converted file. Only works if only one input file is provided. See [the list of supported file types](#file-types-supported).                                                                                                            |
| `-d DIR_PATH, --output-dir DIR_PATH`                    | Directory path where the converted files will be saved. Compatible with single and multiple input files as well as directories. The specified directory will be created if it does not already exist.                                                          |
| `-t FILE_TYPE, --target-type FILE_TYPE`                 | Target file type to convert the files (e.g. `json` or `.json`). Required when using `--output-dir`. See [the list of supported file types](#file-types-supported).                                                                                          |
| `-g SPREADSHEET_NAME, --to-google-sheets SPREADSHEET_NAME` | Write the strings to the first sheet of a Google spreadsheet, replacing its content. Only works if only one input file is provided, or with `-m`. See [Google Sheets](#google-sheets). |
| `-G SPREADSHEET_NAME, --from-google-sheets SPREADSHEET_NAME` | Read the strings from the first sheet of a Google spreadsheet instead of input files. See [Google Sheets](#google-sheets). |
| `-c CREDENTIALS_PATH, --credentials CREDENTIALS_PATH`   | Path of the `service_account.json` file used to access Google Sheets. Defaults to `~/.config/gspread/service_account.json`. See [Setting Up a Google Account](#setting-up-a-google-account). |
| `--check`                                               | Check the translations instead of converting them. Exits with code 1 if any issue is found. See [Checking Translations](#checking-translations). |
| `-p, --print-comments`                                  | Print commented strings from the input file to the output file. Only valid for `.xml` or `.strings` input file types, otherwise it is ignored.                                                                                                                 |
| `-s LANGUAGE_CODE, --source-language LANGUAGE_CODE`     | Code of the language of the default strings (e.g., `en`), such as the ones in Android's `values` directory or iOS' `Base.lproj` directory. Required to write `.xcstrings` files. See [String Catalogs](#string-catalogs). |
| `-m, --merge`                                           | Merge the input files into a single output with a column per language. The language of each file is taken from its directory (e.g., `values-es` or `es.lproj`). Use it with `-f` or `-g`. See [Working With Several Languages](#working-with-several-languages). |

<p align="right">(<a href="#top">back to top</a>)</p>

### Working With Several Languages

To put all the languages of your app in one file to send to translators, pass the resources directory and the `-m` (or `--merge`) option:

```
mobile-strings-converter app/src/main/res -m -f translations.xlsx
```

The language of each file is taken from its directory:

| DIRECTORY                                       | LANGUAGE COLUMN |
|:------------------------------------------------|:----------------|
| `values` or `Base.lproj`                        | `VALUE`         |
| `values-es` or `es.lproj`                       | `es`            |
| `values-pt-rBR` or `pt-BR.lproj`                | `pt-BR`         |
| `values-b+sr+Latn` or `sr-Latn.lproj`           | `sr-Latn`       |

Comments written right before a string (e.g., `<!-- Title of the home screen -->` or `/* Title of the home screen */`) go to the `COMMENT` column so translators can read them.

To convert the translated file back, use `-d` with `.xml`, `.strings` or `.stringsdict` as the target type. A file is written for each language:

```
mobile-strings-converter translations.xlsx -d app/src/main/res -t xml
mobile-strings-converter translations.xlsx -d MyApp -t strings
mobile-strings-converter translations.xlsx -d MyApp -t stringsdict
```

This writes `values/strings.xml`, `values-es/strings.xml`... or `Base.lproj/Localizable.strings`, `es.lproj/Localizable.strings`... respectively. Strings with no translation are left out of the file of that language. iOS plurals go to `.stringsdict` files, so run both of the last two commands to get every string.

If your iOS app uses a [String Catalog](#string-catalogs), all the languages go to a single file instead:

```
mobile-strings-converter translations.xlsx -f MyApp/Localizable.xcstrings -s en
```

The `-s` (or `--source-language`) option sets the language of the `VALUE` column, as String Catalogs need its code. See [String Catalogs](#string-catalogs).

### Checking Translations

To check the translations of your app, pass its files with the `--check` option. Nothing is written:

```
mobile-strings-converter app/src/main/res --check
mobile-strings-converter translations.xlsx --check
```

Every language is compared with the default strings (`values`, `Base.lproj` or the `VALUE` column), or with the first language if there are no default strings. These issues are reported:

- **Missing translations**: strings that have no value in a language. Strings with `translatable="false"` are skipped.
- **Obsolete translations**: strings that have a value in a language, but no default value.
- **Placeholders that differ from the default value**, e.g. `Hello, %s` translated as `Hola, %d`. Android and iOS placeholders are compared as equivalent (e.g. `%s` and `%@`), and positional placeholders can be reordered (e.g. `%1$s has %2$d` and `%2$d %1$s`). The number of a plural can be left out of some quantities (e.g. `One song`).
- **Plurals, arrays and strings that are a different kind of value** than the default value, and arrays with a different number of items.
- **Names defined more than once** in the same file.

The command exits with code 1 if any issue is found, so you can use it in your CI pipeline:

```
[es] greeting: has the placeholders %1$d, but the default value has %1$s
[es] bye: missing translation
[fr] songs: is a string, but the default value is a plural
3 issue(s) found
```

### Using the Package in Your Project

After following the steps in the [Getting Started](#getting-started) section, import the package and the function(s) you want to use.

The strings are read into a `Catalog`, which holds the value of each string in each language. `load` and `save` work with files, while `parse` and `serialize` work with their content, so you don't need a file system:

```python
from pathlib import Path

from mobile_strings_converter import Catalog, load, parse, save, save_split, serialize

# Read a file, including its commented out strings
catalog = load(Path("strings.xml"), with_comments=True)

# Merge the languages of an Android project into a single spreadsheet
catalog = Catalog.merge(
    load(path) for path in sorted(Path("app/src/main/res").glob("values*/strings.xml"))
)
save(catalog, Path("translations.xlsx"))

# Write an iOS `.strings` file for each language
save_split(load(Path("translations.xlsx")), Path("MyApp"), ".strings")

# Convert the content of a file without touching the disk
data = serialize(parse(b'"hello" = "Hello";', ".strings"), ".json")
```

To check the translations, use `check`, and `find_duplicates` for the strings of a single file:

```python
from pathlib import Path

from mobile_strings_converter import check, load

for issue in check(load(Path("translations.xlsx"))):
    print(issue.locale, issue.name, issue.message)
```

The package ships type hints, so type checkers such as mypy can check your code against it.

### Google Sheets

Google Sheets support requires the `sheets` extra (see [Package Installation](#package-installation)).

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

Pass the path of the `service_account.json` file with the `-c` (or `--credentials`) option, or save it as `~/.config/gspread/service_account.json` to leave the option out.

#### Writing to and Reading From a Spreadsheet

Create an empty spreadsheet in Google Sheets, share it with the `client_email` as described in step 8, and write your strings to it with the `-g` (or `--to-google-sheets`) option followed by the name of the spreadsheet. The content of its first sheet is replaced by the strings:

```
mobile-strings-converter app/src/main/res -m -g "MyApp translations" -c path/to/service_account.json
```

Once the translators have filled in the spreadsheet, read it back with the `-G` (or `--from-google-sheets`) option instead of input files:

```
mobile-strings-converter -G "MyApp translations" -d app/src/main/res -t xml -c path/to/service_account.json
```

The spreadsheet is read like any other table, so the `VALUE` column holds the default strings and the other columns are named after their language (see [Working With Several Languages](#working-with-several-languages)). You can also generate an output file along with the spreadsheet by adding `-f`, or check the translations of the spreadsheet with `--check`.

#### Using Google Sheets in Your Project

```python
from pathlib import Path

from mobile_strings_converter import (
    load,
    read_google_sheets,
    save_split,
    write_google_sheets,
)

credentials_filepath = Path("path/to/service_account.json")

write_google_sheets(
    load(Path("strings.xml")), "MyApp translations", credentials_filepath
)

catalog = read_google_sheets("MyApp translations", credentials_filepath)
save_split(catalog, Path("app/src/main/res"), ".xml")
```

<!-- NOTES -->

## Notes

### Android Resources

- `<string>`, `<plurals>` and `<string-array>` resources are converted. See [Plurals and Arrays](#plurals-and-arrays).
- `translatable="false"` is kept when converting `.xml` files to `.xml` files, but other file types don't hold it.
- XML entities (e.g., `&amp;`) and Android escape sequences (e.g., `\'` or `\n`) are decoded when reading `.xml` files and encoded when writing them, so other file types contain the actual text (e.g., `I'm` instead of `I\'m`).
- Whitespace is read as Android does: outside double quotes, spaces, tabs and line breaks are collapsed into a single space, and the whitespace at the start and end of the string is removed. Strings whose whitespace would be lost (e.g., `"  indented"`) are written in double quotes.
- Strings with inline markup (e.g., `Hello <b>World</b>`) are kept verbatim.

### Plurals and Arrays

Spreadsheets and other tables have a row for each item of a plural or array, named after the item:

| NAME           | VALUE      |
|:---------------|:-----------|
| `songs[one]`   | `%d song`  |
| `songs[other]` | `%d songs` |
| `planets[0]`   | `Mercury`  |
| `planets[1]`   | `Venus`    |

These rows are grouped back into a plural or array when converting the table to an `.xml` file. JSON and YAML files hold them as objects and lists instead.

On iOS, plurals go to `.stringsdict` or `.xcstrings` files, and strings go to `.strings` or `.xcstrings` files. iOS has no arrays. Whatever a file type can't hold is skipped with a warning. Only plurals with a single number (`%#@variable@`) are read from `.stringsdict` and `.xcstrings` files.

### Placeholders

Placeholders are converted when writing Android and iOS files, so the strings work on the other platform:

| ANDROID         | IOS                         |
|:----------------|:----------------------------|
| `%s`, `%1$s`    | `%@`, `%1$@`                |
| `%d`, `%1$d`    | `%d`, `%ld`, `%lld`, `%1$d` |
| `%.2f`          | `%.2f`, `%.2lf`             |

Other file types keep the placeholders of the input file.

### String Catalogs

Xcode String Catalogs (`.xcstrings`) hold every language of the app in a single file, with each language under its own code (e.g., `en` or `es`).

The source language of a catalog is read as the default strings, like the ones in Android's `values` directory or iOS' `Base.lproj` directory, so it goes to the `VALUE` column of a spreadsheet and to `values/strings.xml` or `Base.lproj/Localizable.strings`. The other languages keep their code.

When writing a catalog, pass the code of its source language with `-s` (or `--source-language`), as the default strings don't have one:

```
mobile-strings-converter app/src/main/res -m -f Localizable.xcstrings -s en
```

Strings, plurals, comments and `shouldTranslate` are converted. Device variations (e.g., a different string for Mac) and strings with several plurals (substitutions) are skipped with a warning.

### PDF Files

Writing PDF files requires the `pdf` extra (see [Package Installation](#package-installation)). PDF files can only be written, as they are meant to be read by people. Convert your strings to another file type (e.g., `.xlsx`) if you need to convert them back later.

Each cell is written with the first bundled font that has all of its characters. The strings that no font can render are listed in a `[FILE_NAME]-errors.txt` file next to the PDF.

### Indic Languages Supported by PDF Files

- Hindi
- Marathi
- Tibetan
- Gujarati
- Telugu
- Tamil
- Punjabi

### Languages Not Supported by PDF Files

None of the bundled fonts has the characters of these languages:

- Bengali
- Dhivehi
- Japanese <sub>(some kanji, such as 楽, are missing from the font)</sub>
- Kannada
- Khmer
- Malayalam
- Meiteilon (manipuri)
- Myanmar burmese
- Odia (Oriya)
- Sinhala
- Tigrinya

## Troubleshooting

### iOS

You may encounter this error on iOS when using a generated `.strings` file:

```
validation failed: Couldn't parse property list because the input data was in an invalid format
```

Generated `.strings` files escape double quotes and backslashes, but this error can still happen with files edited by hand, for example due to an unescaped double quote in some NAME or VALUE. To identify the line with the error, you have to do the following on macOS:

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

The project uses [uv](https://docs.astral.sh/uv/). To set up your environment and run the checks of the CI:

```bash
uv sync                          # Install the package with every extra and the dev tools
uv run pre-commit install        # Run Ruff and mypy before each commit
uv run python -m unittest discover tests
uv run ruff check && uv run ruff format --check
uv run mypy
```

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
