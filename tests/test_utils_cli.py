import io
import string
import types
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from wei_data_shu.cli import main
from wei_data_shu.utils import generate_password, search_colors


class TestUtilsCli(unittest.TestCase):
    def test_generate_password_uses_filtered_charset(self):
        password = generate_password(50)
        self.assertEqual(len(password), 50)
        self.assertTrue(set(password) <= set(string.ascii_letters + string.digits + "!@#$%^&*"))
        self.assertTrue(set("iIl1o0O").isdisjoint(password))

    def test_search_colors_supports_chinese_queries(self):
        results = search_colors("薄荷")
        self.assertTrue(results)
        self.assertEqual(results[0]["hex"], "#5BC49F")
        self.assertEqual(results[0]["name_zh"], "薄荷绿")

    def test_colors_command_outputs_chinese_name(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["colors", "mint"])
        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("#5BC49F", output)
        self.assertIn("mint green", output)
        self.assertIn("薄荷绿", output)

    def test_password_command_supports_count_and_length(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["password", "--length", "8", "--count", "3"])
        self.assertEqual(exit_code, 0)
        lines = [line for line in stdout.getvalue().splitlines() if line]
        self.assertEqual(len(lines), 3)
        self.assertTrue(all(len(line) == 8 for line in lines))

    def test_date_command_prints_formatted_date(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["date", "--days", "1", "--format", "%Y-%m-%d"])
        self.assertEqual(exit_code, 0)
        self.assertRegex(stdout.getvalue().strip(), r"^\d{4}-\d{2}-\d{2}$")

    def test_excel_info_without_openpyxl_prints_install_hint(self):
        fake_openpyxl = types.ModuleType("openpyxl")

        def _raise_import_error():
            raise ImportError("No module named 'openpyxl'")

        fake_openpyxl.load_workbook = lambda *a, **kw: _raise_import_error()
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch.dict("sys.modules", {"openpyxl": fake_openpyxl}):
            exit_code = main(["excel", "info", "book.xlsx"])
        self.assertEqual(exit_code, 1)
        self.assertIn("wei-data-shu[excel]", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
