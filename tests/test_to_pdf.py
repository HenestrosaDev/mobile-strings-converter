from io import StringIO
from pathlib import Path
from unittest import main
from unittest.mock import patch

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
        super().converter_writes_correct_data_helper(to_pdf)

    def test_handles_unsupported_language(self):
        with patch("builtins.print") as mock_print:
            to_pdf(self.input_filepath, self.output_filepath)

        mock_print.assert_called_with("ມ່ວນກັບແອັບຯຂອງຂ້ອຍ not supported")  # Lao
        mock_print.assert_called_with(
            # Khmer
            "រីករាយជាមួយកម្មវិធីរបស់ខ្ញុំ not supported"
        )
        mock_print.assert_called_with(
            # Kannada
            "ನನ್ನ ಅಪ್ಲಿಕೇಶನ್ ಅನ್ನು ಆನಂದಿಸಿ not supported"
        )
        mock_print.assert_called_with(
            # Malayalam
            "എന്റെ ആപ്പ് ആസ്വദിക്കൂ not supported"
        )
        mock_print.assert_called_with(
            # Meiteilon
            "ꯑꯩꯒꯤ ꯑꯦꯞ ꯑꯁꯤ ꯅꯨꯡꯉꯥꯏꯕꯤꯌꯨ꯫ not supported"
        )
        mock_print.assert_called_with(
            # Odia (Oriya)
            "ମୋର ଆପ୍ ଉପଭୋଗ କରନ୍ତୁ | not supported"
        )
        mock_print.assert_called_with("ኣፕ ናተይ ኣስተማቕሩ not supported")  # Tigrinya
        mock_print.assert_called_with(
            # Sinhala
            "මගේ යෙදුම භුක්ති විඳින්න not supported"
        )


if __name__ == "__main__":
    main()
