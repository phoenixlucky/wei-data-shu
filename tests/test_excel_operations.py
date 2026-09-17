import tempfile
import unittest
from pathlib import Path

try:
    import pandas as pd

    from wei_data_shu.excel import ExcelOperation

    _EXCEL_OK = True
except ImportError:  # pragma: no cover - 依赖缺失时整体跳过
    _EXCEL_OK = False

_SKIP_REASON = "excel extras 未安装或不可用（pip install wei-data-shu[excel]）"


@unittest.skipUnless(_EXCEL_OK, _SKIP_REASON)
class TestExcelOperation(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.root = Path(self.tmpdir.name)
        self.source = self.root / "book.xlsx"
        with pd.ExcelWriter(self.source, engine="openpyxl") as writer:
            pd.DataFrame({"a": [1, 2]}).to_excel(writer, sheet_name="S1", index=False)
            pd.DataFrame({"a": [3, 4]}).to_excel(writer, sheet_name="S2", index=False)

    def test_split_table_creates_one_file_per_sheet(self):
        files = ExcelOperation(self.source, self.root / "split").split_table()
        self.assertEqual(sorted(path.stem for path in files), ["S1", "S2"])
        self.assertTrue(all(path.exists() for path in files))

    def test_split_table_skips_unknown_sheets(self):
        files = ExcelOperation(self.source, self.root / "split").split_table(["S1", "missing"])
        self.assertEqual([path.stem for path in files], ["S1"])

    def test_merge_tables_concatenates_rows(self):
        operation = ExcelOperation(self.source, self.root / "split")
        files = operation.split_table()
        merged = operation.merge_tables(files, self.root / "merged.xlsx")
        frame = pd.read_excel(merged)
        self.assertEqual(len(frame), 4)

    def test_convert_to_csv_writes_utf8_sig(self):
        source = self.root / "中文.xlsx"
        pd.DataFrame({"城市": ["北京"]}).to_excel(source, index=False)
        output = ExcelOperation(source, self.root / "csv").convert_to_csv()
        self.assertTrue(output.exists())
        self.assertEqual(output.read_text(encoding="utf-8-sig").splitlines()[0], "城市")


if __name__ == "__main__":
    unittest.main()
