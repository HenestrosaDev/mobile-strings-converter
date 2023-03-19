from pathlib import Path
from unittest import main

from base_tests import BaseTests
from mobile_strings_converter.converter import convert_strings


class TestToPdf(BaseTests.BaseConverterTest):
    def setUp(self):
        super().setUp()
        self.file_name = "strings.pdf"

    def tearDown(self):
        super().tearDown()
        strings_errors_path = self.output_filepath.parent / "strings-errors.txt"
        if strings_errors_path.exists():
            strings_errors_path.unlink()

    # Overriding abstract method
    def _converter_writes_correct_data(
        self,
        template_filepath: Path,
        input_filepath: Path,
        should_print_comments: bool,
    ):
        convert_strings(input_filepath, self.output_filepath, should_print_comments)

        with open(self.output_filepath, "rb") as test_file, open(
            template_filepath, "rb"
        ) as template_file:
            test_size = len(test_file.read())
            template_size = len(template_file.read())

            # Error margin: 10% of the total size in bytes of both files. PDF is a
            # very complex file format and, even if we write the exact same content
            # in two files, there will be lots of differences between both. Through
            # tests, I've come to realize that there is a 10% difference between two
            # files with the same content, so I'll leave it at that. However,
            # if you manage to find a package that compares the content of two PDFs,
            # please do let me know.
            size_delta = max(test_size, template_size) * 0.1

            self.assertAlmostEqual(
                test_size,
                template_size,
                delta=size_delta,
                msg="File size does not match",
            )


if __name__ == "__main__":
    main()
