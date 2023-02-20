import unittest
from abc import abstractmethod
from pathlib import Path


class BaseConverterTest(unittest.TestCase):
    def setUp(self):
        self.input_filepath = Path(__file__).parent / "files/strings.xml"
        self.template_filepath: Path | None = None
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
        to_converter_func(self.input_filepath, self.output_filepath)
        self.assertTrue(self.output_filepath.exists())

    def converter_writes_correct_data_helper(self, to_converter_func):
        to_converter_func(self.input_filepath, self.output_filepath)

        with open(self.output_filepath, "rb") as test_file, open(
            self.template_filepath, "rb"
        ) as template_file:
            self.assertEqual(
                test_file.read(),
                template_file.read(),
            )
