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
    <h2 align="center">Mobile strings converter</h2>
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
- [Usage](#usage)
  - [To Execute the Script](#to-execute-the-script)
  - [To Import the Package Into Your Project](#to-import-the-package-into-your-project)
  - [To Open the Code](#to-open-the-code)
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

#### Root directories:

- `.github/workflows`: GitHub workflows. It also includes the templates for issues and pull requests, as well as the `depandabot.yml` file for Dependabot configuration.
- `docs`: Contains files related to the documentation of the project.
- `src/mobile_strings_converter`:  Contains the source code files.
- `tests`: Contains unit tests to ensure the correct functionality of the package. It also includes the `files` directory, which contains a few demo files in different formats to use in the unit tests.

#### Root files:

- `.gitignore`: File used by the version control system Git to specify files or directories that should be ignored by Git when tracking changes to a project.
- `.pre-commit-config.yaml`: Configuration file used by **pre-commit**, a tool that runs checks (such as linting, testing, or formatting) on the code before you commit changes to version control. The file specifies which checks pre-commit should run and how it should run them.
- `LICENSE`: Project license, which is [MIT](https://opensource.org/license/mit/).
- `poetry.lock`: File generated by **Poetry**, a package manager for Python, that contains the exact versions of all packages used by a project. The file is used to ensure that all members of a development team are using the same versions of packages, even if different versions are available in the package repository.
- `pyproject.toml`: Configuration file used by **Poetry**. It specifies the metadata for a Python project, including the project name, version, description, author, license and dependencies.
- `README.md`: What you are reading right now.
- `requirements.txt`: Lists the names and versions of each package used to build this project. To install the requirements, execute `pip install -r requirements.txt`.
- `requirements-dev.txt`: Lists the names and versions of each package used in the development stage of this project. To install the requirements, execute `pip install -r requirements-dev.txt`.


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

<!-- USAGE -->

## Usage

### To Execute The Script

1. Download the [release](#release-files) that is best suited to your needs.
2. Open the command line and run `pip install -r path/to/requirements.txt` to install the required packages to execute the script.
3. Example of a basic command to convert a `.xml` or `.strings` file to another file type: 
    ```
    path/to/python path/to/mobile_strings_converter.py path/to/<*.xml | *.strings> -o path/to/*.<SUPPORTED FILE TYPE EXTENSION>
    ```

#### To Generate a Spreadsheet in Google Sheets

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
path/to/python path/to/mobile_strings_converter.py path/to/<strings.xml | Localizable.strings> -gs <SHEET NAME> -c path/to/service_account.json 
```

If you want to generate an output file along with the spreadsheet, run this:
```
path/to/python path/to/mobile_strings_converter.py path/to/<strings.xml | Localizable.strings> -gs <SHEET NAME> -c path/to/service_account.json -o path/to/strings.<SUPPORTED FILE TYPE EXTENSION>
```

#### Script flags

- `-h`, `--help`: Show help
- `-o`, `--output-filepath`: Output filepath where you want to store the converted file. Its extension can be any of the file types listed [here](#about-the-project).
- `-g`, `--google-sheets` <spreadsheet name>: Creates a spreadsheet in Google Sheets with the name passed as argument.
- `-c`, `--credentials` <`service_account.json` filepath>: Mandatory if you want to generate a spreadsheet in your Google account.
- `-p`, `--print-comments`: If present, indicates that commented strings will be printed in the output file.

### To Import the Package Into Your Project

1. Run `pip install mobile-strings-converter`
2. Import the package and the wrapper function with this line of code: `from mobile_strings_converter import convert_strings`.

### To Open the Code

1. Clone the project with the `git clone https://github.com/HenestrosaConH/mobile-strings-converter.git` command.
2. Open it in your favourite IDE (mine is [PyCharm](https://www.jetbrains.com/pycharm/))

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

- **Bengali** (not possible to print correctly using [fpdf2](https://pypi.org/project/fpdf2/))
- **Dhivehi** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Kannada** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Khmer** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Lao** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Malayalam** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Meiteilon (manipuri)** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Myanmar burmese** (not possible to print correctly using [fpdf2](https://pypi.org/project/fpdf2/))
- **Odia (Oriya)** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Sinhala** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))
- **Tigrinya** (not recognized by [lingua-language-detector](https://pypi.org/project/lingua-language-detector/))

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [ ] Add support for multiple `.xml`/`.strings` files input.
- [ ] Add support for converting a file (not `.xml` nor `.strings`) to a strings resource file.
- [ ] Make a web version.

You can propose a new feature creating an [issue](https://github.com/HenestrosaConH/mobile-strings-converter/new/choose).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
Please, read the [CONTRIBUTING.md](https://github.com/HenestrosaConH/mobile-strings-converter/blob/main/.github/CONTRIBUTING.md) file, where you can find more detailed information about how to contribute to the project.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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
