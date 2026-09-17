"""Tests for the shared optional-dependency core."""

import unittest
from unittest.mock import patch

from wei_data_shu import _deps


class TestSharedDependencyGuard(unittest.TestCase):
    def test_missing_dependency_reports_install_hint(self):
        message = _deps.missing_message(["pandas"], "excel", installed=lambda name: False)
        self.assertIn("pandas 未安装", message)
        self.assertIn("pip install wei-data-shu[excel]", message)

    def test_broken_install_is_distinguished_from_missing(self):
        message = _deps.missing_message(
            ["pandas"],
            "excel",
            import_errors={"pandas": "ImportError: boom"},
            installed=lambda name: True,
        )
        self.assertIn("已安装但无法导入", message)
        self.assertIn("ImportError: boom", message)

    def test_require_deps_raises_with_extra_hint(self):
        with self.assertRaises(ImportError) as ctx:
            _deps.require_deps("pandas", extra="excel", installed=lambda name: False)
        self.assertIn("wei-data-shu[excel]", str(ctx.exception))

    def test_require_deps_is_silent_when_available(self):
        _deps.require_deps("pandas", extra="excel", installed=lambda name: True)

    def test_module_name_maps_logical_names(self):
        self.assertEqual(_deps.module_name("mysql"), "mysql.connector")
        self.assertEqual(_deps.module_name("unknown"), "unknown")


class TestExcelDependencyGuard(unittest.TestCase):
    def test_require_excel_deps_uses_excel_extra(self):
        from wei_data_shu.excel import _deps as excel_deps

        with patch("wei_data_shu.excel._deps._require") as mocked:
            excel_deps.require_excel_deps("openpyxl")
        mocked.assert_called_once_with("openpyxl", extra="excel")


if __name__ == "__main__":
    unittest.main()
