import tempfile
import unittest
from pathlib import Path

try:
    import numpy as np
    import pandas as pd  # noqa: F401 - 仅用于探测 excel extras 是否可用

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

    def test_read_dataframe_defaults_first_row_to_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.write_sheet("sheet1", [["a", "b"], [1, 2]], 1, 1, 2, 2, apply_styles=False)
                frame = manager.read_dataframe("sheet1")
        self.assertEqual(list(frame.columns), ["a", "b"])
        self.assertEqual(frame.shape, (1, 2))

    def test_read_dataframe_honours_header_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.write_sheet(
                    "sheet1",
                    [["月报", ""], ["a", "b"], [1, 2]],
                    1,
                    1,
                    3,
                    2,
                    apply_styles=False,
                )
                frame = manager.read_dataframe("sheet1", start_row=1, header_row=2)
        self.assertEqual(list(frame.columns), ["a", "b"])
        self.assertEqual(frame.shape, (2, 2))

    def test_read_dataframe_rejects_header_outside_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.write_sheet("sheet1", [["a"], [1]], 1, 1, 2, 1, apply_styles=False)
                with self.assertRaises(ValueError):
                    manager.read_dataframe("sheet1", start_row=1, header_row=99)

    def test_write_accepts_numpy_array_without_ambiguous_truth_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.xlsx"
            with ExcelManager(path) as manager:
                manager.write_sheet("sheet1", np.array([[1, 2], [3, 4]]), 1, 1, apply_styles=False)
                data = manager.read_sheet("sheet1", 1, 1, 2, 2)
        self.assertEqual(data, [[1, 2], [3, 4]])


if __name__ == "__main__":
    unittest.main()
