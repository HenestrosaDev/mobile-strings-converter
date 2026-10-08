import io
import os
import unittest
from unittest import mock

from mobile_strings_converter.console_style import ConsoleStyle, colorize


class _Terminal(io.StringIO):
    def isatty(self):
        return True


class TestColorize(unittest.TestCase):
    def setUp(self):
        # Ignore the variables of the environment that runs the tests
        patcher = mock.patch.dict(os.environ, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_terminal(self):
        self.assertEqual(
            f"{ConsoleStyle.GREEN}Done{ConsoleStyle.END}",
            colorize("Done", ConsoleStyle.GREEN, _Terminal()),
        )

    def test_redirected_output(self):
        self.assertEqual("Done", colorize("Done", ConsoleStyle.GREEN, io.StringIO()))

    def test_no_color(self):
        os.environ["NO_COLOR"] = "1"

        self.assertEqual("Done", colorize("Done", ConsoleStyle.GREEN, _Terminal()))

    def test_dumb_terminal(self):
        os.environ["TERM"] = "dumb"

        self.assertEqual("Done", colorize("Done", ConsoleStyle.GREEN, _Terminal()))

    def test_force_color(self):
        os.environ["FORCE_COLOR"] = "1"

        self.assertEqual(
            f"{ConsoleStyle.RED}Done{ConsoleStyle.END}",
            colorize("Done", ConsoleStyle.RED, io.StringIO()),
        )

    def test_no_color_wins_over_force_color(self):
        os.environ["NO_COLOR"] = "1"
        os.environ["FORCE_COLOR"] = "1"

        self.assertEqual("Done", colorize("Done", ConsoleStyle.RED, _Terminal()))


if __name__ == "__main__":
    unittest.main()
