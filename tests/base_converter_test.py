import unittest
from abc import abstractmethod
from pathlib import Path


class BaseConverterTest(unittest.TestCase):
    def setUp(self):
        self.input_filepaths = [
            Path(__file__).parent / "files/xml/strings-en.xml",
            Path(__file__).parent / "files/xml/strings-es.xml",
            Path(__file__).parent / "files/xml/strings-zh.xml",
        ]
        self.template_filepaths: Path | None = None
        self.output_filepath: Path | None = None

    def tearDown(self):
        if self.output_filepath and self.output_filepath.exists():
            self.output_filepath.unlink()

    @abstractmethod
    def test_converter_creates_file(self):
        pass

    @abstractmethod
    def test_converter_writes_correct_data(self):
        pass

    def converter_creates_file_helper(self, to_converter_func):
        for xml_filepath in self.input_filepaths:
            to_converter_func(xml_filepath, self.output_filepath)
            self.assertTrue(self.output_filepath.exists())

    def converter_writes_correct_data_helper(self, to_converter_func):
        for input_filepath in self.input_filepaths:
            to_converter_func(input_filepath, self.output_filepath)

            language_code = input_filepath.stem[-2:]  # strings-zh
            extension = self.output_filepath.suffix
            template_filepath = [
                template_filepath
                for template_filepath in self.template_filepaths
                if f"strings-{language_code}{extension}" in template_filepath.name
            ][0]

            with open(self.output_filepath, "rb") as test_file, open(
                template_filepath, "rb"
            ) as template_file:
                self.assertEqual(
                    test_file.read().decode("utf-8").replace("\r\n", "\n"),
                    template_file.read().decode("utf-8").replace("\r\n", "\n"),
                )
