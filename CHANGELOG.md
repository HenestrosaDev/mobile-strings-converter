# Changelog

All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - Unreleased

### Breaking Changes

- Python 3.10 or later is required.
- Writing PDF files and using Google Sheets need the `pdf` and `sheets` extras (`pip install "mobile-strings-converter[all]"` installs both). Using them without the extra raises a `MissingDependencyError` that names the extra to install.
- The fonts of the PDF files are in the `mobile-strings-converter-fonts` package, which the `pdf` extra installs.
- PDF files can only be written. They no longer embed the strings, and reading them fails with an error.
- The `converter` module is removed. Use `load` and `save` to read and write files, and the `google_sheets` module for Google Sheets.

### Added

- Files are converted through a `Catalog` that holds every language, so a single file can hold several languages (a column per language in tables). `parse` and `serialize` convert files without a file system.
- `-m/--merge` merges the input files into one output file, and `-d` writes a file per language when converting to `.xml`, `.strings` or `.stringsdict`.
- Android plurals and string arrays, comments for translators and `translatable="false"` are converted.
- `.stringsdict` files and Xcode String Catalogs (`.xcstrings`), with `-s/--source-language` to set the source language of a catalog.
- Placeholders are converted between Android and iOS (e.g. `%1$s` and `%1$@`).
- `-G/--from-google-sheets` reads a spreadsheet, and `-c/--credentials` sets the path of the `service_account.json` file.
- `--check` reports missing, obsolete and untranslated strings, mismatched placeholders, values of a different kind and duplicated names, with `--reference-locale`, `--check-untranslated` and `--check-format` (`text`, `json` or `github`).
- A GitHub Action and a pre-commit hook to check the translations of a project.
- Type hints for the package (`py.typed`).
- The `mobile-strings-converter` command.

### Fixed

- The CLI crashed on every run.
- `.ods` files were XLSX files with an `.ods` extension.
- Android strings with extra attributes, several lines, whitespace, escape sequences, Unicode escapes or `<xliff:g>` tags were read wrong or skipped, and directories without strings failed.
- `.strings` files with `/* */` comments, URLs, unquoted names and values, or UTF-16 encoding were read wrong.
- Values with special characters broke HTML and Markdown files.
- Google Sheets authentication failed.
- Input directories with files of the same name overwrote each other's output.
- Colors are printed only to terminals, and warnings go to stderr.

## [0.1.4] - 2024-05-29

See the [releases](https://github.com/HenestrosaDev/mobile-strings-converter/releases) for the changes of 0.1.4 and earlier versions.

[0.2.0]: https://github.com/HenestrosaDev/mobile-strings-converter/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/HenestrosaDev/mobile-strings-converter/releases/tag/v0.1.4
