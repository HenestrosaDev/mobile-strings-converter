from pathlib import Path
from unittest import main

from android_strings_converter import to_pdf
from base_converter_test import BaseConverterTest


class TestToPdf(BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.template_filepath = Path(__file__).parent / "files/strings.pdf"
        self.output_filepath = Path("strings.pdf")

    # Overriding abstract method
    def test_converter_creates_file(self):
        super().converter_creates_file_helper(to_pdf)

    # Overriding abstract method
    def test_converter_writes_correct_data(self):
        to_pdf(self.input_filepath, self.output_filepath)

        with open(self.output_filepath, "rb") as test_file, open(
            self.template_filepath, "rb"
        ) as template_file:
            test_size = len(test_file.read())
            template_size = len(template_file.read())

            # Error margin: 1% of the total size in bytes of both files
            size_delta = max(test_size, template_size) * 0.1

            self.assertAlmostEqual(
                test_size,
                template_size,
                delta=size_delta,
                msg="File size does not match",
            )


if __name__ == "__main__":
    main()
