import tempfile
import unittest
from pathlib import Path

try:
    import pandas as pd  # noqa: F401

    from wei_data_shu.excel import ExcelManager

    _EXCEL_OK = True
except ImportError:
    _EXCEL_OK = False


@unittest.skipUnless(_EXCEL_OK, "pandas 不可用（excel extras 未安装或环境损坏）")
class TestExcelIO(unittest.TestCase):
    def test_write_and_read_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.write_sheet("sheet1", [["a", "b"], [1, 2]], 1, 1, 2, 2)

            with ExcelManager(path) as manager:
                data = manager.read_sheet("sheet1", 1, 1, 2, 2)

            self.assertEqual(data, [["a", "b"], [1, 2]])

    def test_context_manager_saves_on_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.write_sheet("sheet1", [["x"]], 1, 1, 1, 1)
            self.assertTrue(path.exists())

    def test_create_sheet_duplicate_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                with self.assertRaises(ValueError):
                    manager.create_sheet("sheet1")

    def test_sheet_names_are_case_insensitive(self):
        """工作表名不区分大小写：复用已有表，且不应抛 KeyError。"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.write_sheet("Sheet1", [["a"]], 1, 1, 1, 1)

                self.assertEqual(manager.sheet_names, ["sheet1"])
                self.assertEqual(manager.read_sheet("SHEET1", 1, 1, 1, 1), [["a"]])
                self.assertEqual(manager.get_sheet_info("Sheet1")["name"], "sheet1")

    def test_create_sheet_conflicting_case_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                with self.assertRaises(ValueError):
                    manager.create_sheet("Sheet1")

    def test_delete_sheet_is_case_insensitive(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.create_sheet("extra")
                manager.delete_sheet("EXTRA")
                self.assertEqual(manager.sheet_names, ["sheet1"])


if __name__ == "__main__":
    unittest.main()
