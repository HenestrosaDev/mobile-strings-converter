import sys
import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile


class TestXml(unittest.TestCase):
    def test_valid_xml_file(self):
        # Create a temporary file with valid XML data
        xml_data = """
        <?xml version="1.0" encoding="UTF-8"?>
        <resources>
            <string name="app_name">MyApp</string>
        </resources>
        """
        with NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(xml_data)
            xml_filepath = Path(f.name)

        # Call the function and check the output
        expected_output = [("app_name", "MyApp")]
        self.assertEqual(get_xml_data(xml_filepath), expected_output)

        # Clean up the temporary file
        xml_filepath.unlink()

    def test_invalid_xml_file(self):
        # Create a temporary file with invalid XML data
        xml_data = """
        <?xml version="1.0" encoding="UTF-8"?>
        <bookstore>
          <book category="fiction">
            <title>The Great Gatsby</title>
            <author>F. Scott Fitzgerald</author>
            <year>1925</year>
            <price>10.99</price>
          </book>
          <book category="non-fiction">
            <title>The Elements of Style</title>
            <author>William Strunk Jr.</author>
            <author>E. B. White</author>
            <year>1918</year>
            <price>9.99</price>
          </book>
        </bookstore>
        """
        with NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(xml_data)
            xml_filepath = Path(f.name)

        # Call the function and check that it raises a ValueError
        with self.assertRaises(ValueError):
            get_xml_data(xml_filepath)

        # Clean up the temporary file
        xml_filepath.unlink()


if __name__ == "__main__":
    unittest.main()
