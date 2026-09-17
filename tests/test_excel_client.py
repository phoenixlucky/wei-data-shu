import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

try:
    from wei_data_shu.excel.client import OpenExcel
    from wei_data_shu.excel.manager import ExcelManager

    _EXCEL_CLIENT_OK = True
except ImportError:  # pragma: no cover - pandas / xlwings 缺失时整体跳过，而非报错
    _EXCEL_CLIENT_OK = False


class _FakeApi:
    def __init__(self):
        self.AutomationSecurity = None
        self.refresh_count = 0

    def RefreshAll(self):
        self.refresh_count += 1


class _FakeWorkbook:
    def __init__(self):
        self.api = _FakeApi()
        self.saved_to = None
        self.closed = False
        self.macro_calls = []

    def macro(self, name):
        def invoke(*args):
            self.macro_calls.append((name, args))
            return "ok"

        return invoke

    def save(self, path):
        self.saved_to = path

    def close(self):
        self.closed = True


class _FakeBooks:
    def __init__(self, workbook):
        self.workbook = workbook

    def open(self, path):
        return self.workbook


class _FakeApp:
    def __init__(self, workbook):
        self.api = workbook.api
        self.books = _FakeBooks(workbook)
        self.quit_called = False

    def quit(self):
        self.quit_called = True


class _FakeXlwings:
    def __init__(self, app):
        self.app = app

    def App(self, visible=False):
        return self.app


@unittest.skipUnless(_EXCEL_CLIENT_OK, "excel extras 未安装或不可用（pip install wei-data-shu[excel]）")
class TestOpenExcelMacros(unittest.TestCase):
    def test_run_macro_enables_macros_and_saves_result(self):
        workbook = _FakeWorkbook()
        app = _FakeApp(workbook)
        xlwings = _FakeXlwings(app)

        with patch("wei_data_shu.excel.client._require_xlwings", return_value=xlwings):
            result = OpenExcel("report.xlsm", "result.xlsm").run_macro("Module1.RefreshReport", args=[2026, "09"])

        self.assertEqual(result, "ok")
        self.assertEqual(workbook.api.AutomationSecurity, 1)
        self.assertEqual(workbook.macro_calls, [("Module1.RefreshReport", (2026, "09"))])
        self.assertEqual(workbook.saved_to.name, "result.xlsm")
        self.assertTrue(workbook.closed)
        self.assertTrue(app.quit_called)

    def test_macro_security_shortcuts_set_expected_level(self):
        for method_name, expected_level in (
            ("open_with_macros_enabled", 1),
            ("open_with_macros_disabled", 3),
        ):
            with self.subTest(method_name=method_name):
                workbook = _FakeWorkbook()
                app = _FakeApp(workbook)
                xlwings = _FakeXlwings(app)
                with patch("wei_data_shu.excel.client._require_xlwings", return_value=xlwings):
                    with getattr(OpenExcel("report.xlsm"), method_name)():
                        pass
                self.assertEqual(workbook.api.AutomationSecurity, expected_level)

    def test_excel_manager_preserves_vba_for_macro_enabled_files(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "report.xlsm"
            path.touch()
            workbook = _FakeWorkbook()
            workbook.sheetnames = ["Sheet1"]

            with patch("wei_data_shu.excel.manager.load_workbook", return_value=workbook) as load:
                manager = ExcelManager(path)

            load.assert_called_once_with(str(path), keep_vba=True)
            self.assertTrue(manager.macro_enabled)
            manager.save(path)
            self.assertEqual(workbook.saved_to, path)
            manager.close()


if __name__ == "__main__":
    unittest.main()
