import unittest
from abc import abstractmethod

from constants import XML_FILEPATHS


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.xml_filepaths = XML_FILEPATHS
        self.output_filepath = None

    def tearDown(self):
        if self.output_filepath and self.output_filepath.exists():
            self.output_filepath.unlink()

    @abstractmethod
    def test_converter_creates_file(self):
        pass

    @abstractmethod
    def test_converter_writes_correct_data(self):
        pass
