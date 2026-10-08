# Changelog

All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/).

## [0.2.0] - Unreleased

This release rewrites the converter around a catalog of strings that keeps plurals, arrays, comments and every language, so files are converted without losing them. Read the breaking changes before upgrading.

### Breaking changes

- Python 3.10 or newer is required.
- The PDF and Google Sheets dependencies are optional. Install them with `pip install 'mobile-strings-converter[pdf]'`, `[sheets]` or `[all]`.
- PDF files can only be written, not read.
- `-f/--output-filepath` is now `-f/--output-file`.
- `-g/--google-sheets` takes the name of the spreadsheet (`-g SPREADSHEET_NAME`, or `--to-google-sheets`), and `-c/--credentials` defaults to `~/.config/gspread/service_account.json`.
- The Python API has changed: `convert_strings` and `to_google_sheets` are replaced by `load`, `save`, `parse`, `serialize`, `write_google_sheets` and the `Catalog` class. See [Using the Package in Your Project](README.md#using-the-package-in-your-project).
- Warnings and errors are printed to stderr instead of stdout.

### Added

- iOS `.stringsdict` files and Xcode String Catalogs (`.xcstrings`).
- Android plurals (`<plurals>`) and string arrays (`<string-array>`).
- Several languages in one file: `-m/--merge` puts the languages of a project into a single spreadsheet with a column per language, and `-d/--output-dir` writes a file per language back (e.g., `values-es/strings.xml`).
- `-s/--source-language` sets the language of the default strings, which String Catalogs need.
- `-G/--from-google-sheets` reads the strings from a Google spreadsheet.
- `--check` finds missing, obsolete and empty translations, placeholders that differ from the default strings, and names defined more than once. It exits with code 1 if any issue is found, and takes these options:
  - `--reference-locale` compares the languages with another one than the default strings.
  - `--check-untranslated` also reports translations that are the same as the default strings.
  - `--check-format json` prints the issues as JSON, and `--check-format github` as annotations of GitHub Actions.
- A GitHub Action and a pre-commit hook that check the translations of a project. See [Checking Translations](README.md#checking-translations).
- Placeholders are converted between Android and iOS (e.g., `%s` and `%@`). Android strings with several placeholders get positions (e.g., `%1$s has %2$d`), as Android doesn't build them otherwise.
- `-v/--version` prints the version.
- UTF-16 `.strings` files, and `.strings` files with unquoted names and values (e.g., `title = "Home";`).
- Type hints for the package.

### Changed

- Comments for translators are kept in a `COMMENT` column of spreadsheets and tables.
- Android strings are read as Android reads them: whitespace is collapsed, escape sequences are decoded, and `<xliff:g>` tags are removed, keeping their content.
- PDF fonts are chosen by the characters of each string, so more languages are rendered.
- Directories keep their structure in the output directory.
- When a directory is passed, its Android files without strings (e.g., layouts or `colors.xml`) are skipped.
- Messages are only colored in a terminal. Set `NO_COLOR` to disable colors, or `FORCE_COLOR` to use them anyway.

### Fixed

- The Tamil font is loaded on case-sensitive file systems.
- Generated JSON and Android XML files end with a newline.

## [0.1.4] and earlier

See the [GitHub releases](https://github.com/HenestrosaDev/mobile-strings-converter/releases).

[0.2.0]: https://github.com/HenestrosaDev/mobile-strings-converter/compare/v0.1.4...HEAD
[0.1.4]: https://github.com/HenestrosaDev/mobile-strings-converter/releases/tag/v0.1.4
