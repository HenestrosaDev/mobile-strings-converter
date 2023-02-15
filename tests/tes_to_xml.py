import unittest
from pathlib import Path

from android_strings_converter.converter import get_xml_data


class TestXml(unittest.TestCase):
    def setUp(self):
        self.xml_filepath = Path("tests/files/strings.xml")

    def tearDown(self):
        if self.xml_filepath.exists():
            self.xml_filepath.unlink()

    def test_get_xml_data(self):
        xml_filepath = Path("../examples/android-en.xml")
        data = get_xml_data(xml_filepath)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0][0], "app_name")
        self.assertEqual(data[0][1], "Test App")
        self.assertEqual(data[1][0], "hello_world")
        self.assertEqual(data[1][1], "Hello World!")


if __name__ == "__main__":
    unittest.main()
