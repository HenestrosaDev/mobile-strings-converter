<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="docs/icon.png" alt="Logo" width="156" height="156" style="margin-bottom:-40px">
    <h2 align="center">Android strings converter</h2>
    <p align="center">
        A Python package that converts Android strings.xml file to any file type supported by the package.
        <br />
        <br />
        <a href="https://pypi.org/project/android-strings-converter/">
          <img alt="PyPI version" src="https://img.shields.io/pypi/v/android-strings-converter" />
        </a>
        <a href="https://pypi.org/project/android-strings-converter/">
          <img alt="Python versions support" src="https://img.shields.io/pypi/pyversions/android-strings-converter" />
        </a>
        <br />
        <a href="https://github.com/HenestrosaConH/android-strings-converter/actions/workflows/main-branch-build.yaml">
          <img alt="GitHub action: Main branch build" src="https://github.com/HenestrosaConH/android-strings-converter/actions/workflows/main-branch-build.yaml/badge.svg" />
        </a>
        <a href="https://codecov.io/gh/HenestrosaConH/android-strings-converter/">
          <img alt="Codecov" src="https://codecov.io/gh/HenestrosaConH/android-strings-converter/branch/main/graph/badge.svg" />
        </a>
        <br />
        <a href="https://github.com/HenestrosaConH/android-strings-converter/graphs/contributors">
          <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/HenestrosaConH/android-strings-converter" />
        </a>
        <a href="https://github.com/HenestrosaConH/android-strings-converter/blob/main/LICENSE">
          <img alt="License" src="https://img.shields.io/github/license/HenestrosaConH/android-strings-converter" />
        </a>
        <a href="https://github.com/HenestrosaConH/android-strings-converter/android-strings-converter">
          <img alt="Issues" src="https://img.shields.io/github/issues/HenestrosaConH/android-strings-converter" />
        </a>
        <a href="https://github.com/HenestrosaConH/android-strings-converter/pulls">
          <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/HenestrosaConH/android-strings-converter" />
        </a>
        <br />
        <br />
        <a href="https://github.com/HenestrosaConH/android-strings-converter/issues">Report Bug</a> · <a href="https://github.com/HenestrosaConH/android-strings-converter/issues">Request Feature</a> · <a href="https://github.com/HenestrosaConH/android-strings-converter/discussions">Ask Question</a>
    </p>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About The Project](#about-the-project)
    - [Project Structure](#project-structure)
    - [Built With](#built-with)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

<!-- ABOUT THE PROJECT -->

## About The Project

I tried to do the whole process of converting a **strings.xml** into a spreadsheet in Google Sheets by hand and, even though you can do it with the option **Data > Split text to columns**, 
it involves wasting your time generating the spreadsheet manually instead of the more time-efficient solution of running a Python script to achieve that with any file format supported by the package

Moreover, not only this program can be executed on its own, it also can be installed as a package via **PyPI**.

The file types supported by the package are the following:
- XLSX
- ODS
- HTML
- CSV
- YAML
- JSON

<!-- PROJECT STRUCTURE -->

### Project Structure

Directories:

- `.github/workflows`: GitHub workflows. It also includes the templates for issues and pull requests, as well as the `depandabot.yml` file for Dependabot configuration.
- `docs`: Contains files related to the documentation of the project.
- `src/android_strings_converter`:  Contains the source code files.
- `tests`: Contains unit tests to ensure the correct functionality of the package. It also includes the `files` directory, which contains a few demo files in different languages to use in the unit tests.

Besides those directories, there are also these files in the root (apart from the .gitignore, README.md and LICENSE):

- `.pre-commit-config.yaml`: Configuration file used by **pre-commit**, a tool that runs checks (such as linting, testing, or formatting) on the code before you commit changes to version control. The file specifies which checks pre-commit should run and how it should run them.
- `poetry.lock`: File generated by **Poetry**, a package manager for Python, that contains the exact versions of all packages used by a project. The file is used to ensure that all members of a development team are using the same versions of packages, even if different versions are available in the package repository.
- `pyproject.toml`: Configuration file used by **Poetry**. It specifies the metadata for a Python project, including the project name, version, description, author, license and dependencies.
- `requirements.txt`: Lists the names and versions of each package used to build this project. To install the requirements, execute `pip install -r requirements.txt`.
- `requirements-dev.txt`: Lists the names and versions of each package used in the development stage of this project. To install the requirements, execute `pip install -r requirements-dev.txt`.


<!-- BUILT WITH -->

### Built With

- [openpyxl](https://pypi.org/project/openpyxl/): To generate ODS and XLSX files.
- [gspread](https://pypi.org/project/gspread/): To generate Google Spreadsheets.
- [protobuf](https://pypi.org/project/oauth2client/): Used by `google.oauth2.credentials` to authenticate to the user's Google account in order to create the spreadsheet, 
- [PyYAML](https://pypi.org/project/PyYAML/): To generate YAML files.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

If you want to execute the script:
- Go to [releases](https://github.com/HenestrosaConH/android-strings-converter/releases) and download the latest one.

If you want to import the package into your project:
1. Run `pip install android-strings-converter`
2. Import the package with this line of code: `from android_strings_converter import <FUNCTION>`
- For example, if you were to import the `to_xlsx` function: `from android_strings_converter import to_xlsx`

If you want to open the code:
- Clone the project with the `git clone https://github.com/HenestrosaConH/android-strings-converter.git` command and then open it with your favourite IDE (mine is [PyCharm](https://www.jetbrains.com/pycharm/)).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->

## Usage

To execute the script, you can follow these steps:
1. Make sure you have the [latest version](https://github.com/HenestrosaConH/android-strings-converter/releases) of the script installed.
2. Open the command line and run the following command: 
    ```
    path/to/python path/to/android_strings_converter.py path/to/strings.xml -o path/to/strings.<FILE TYPE EXTENSION SUPPORTED>
    ```
    This will generate a file named `strings` in the desired path.  
    <br>

If you want to generate a Google Sheet, run the following command:
```
path/to/python path/to/android_strings_converter.py path/to/strings.xml -gs <SHEET NAME> -c path/to/service_account.json
```
Please note that you will have to generate the `service_account.json` yourself. To do it, you can do the following:

1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select an existing project.
3. Go to the **APIs & Services** page, click on **Dashboard** and then click on **Enable APIs and Services**.
4. Search for **Google Sheets API** and enable it.
5. Go to the **Credentials** page, click on **Create credentials**, and then choose **Service account**.
6. Give your service account a name and select a role. For this purpose, you can select **Project -> Editor**.
7. Click on the "Create key" button, select the JSON format and download the `service_account.json` file.
8. Share your Google Sheets file with the email address that is specified in the **client_email** field in the `service_account.json` file.

Alternatively, you can create an XLSX file and open it in Google Sheets if you don't want to go through the hassle of generating the `service_account.json` file.

<p align="right">(<a href="#top">back to top</a>)</p>

## Roadmap

- [ ] Try to lower Python version to make it compatible with Python 3.8
- [ ] Make an iOS version.
- [ ] Make a web version with Django/Flask.

You can propose a new feature creating an [issue](https://github.com/HenestrosaConH/android-strings-converter/issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
Please, read the [CONTRIBUTING.md](https://github.com/HenestrosaConH/android-strings-converter/blob/main/.github/CONTRIBUTING.md) file, where you can find more detailed information about how to contribute to the project.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

[![LinkedIn][linkedin-shield]][linkedin-url]
[![henestrosaconh@gmail.com][gmail-shield]][gmail-url]

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

I've made use of the following resources to make this project:

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
- [Img Shields](https://shields.io)
- [How to create a Python package](https://mathspp.com/blog/how-to-create-a-python-package-in-2022#how-to-create-a-python-package)
- [Icon created by Midjourney](https://www.midjourney.com/app/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- BADGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://linkedin.com/in/henestrosaconh
[gmail-shield]: https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white
[gmail-url]: mailto:henestrosaconh@gmail.com