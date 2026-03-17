import types
import unittest
from unittest.mock import patch

import wei_data_shu.excel as excel


class TestExcelDomain(unittest.TestCase):
    def test_excel_package_exposes_expected_names(self):
        self.assertIn("ExcelManager", excel.__all__)
        self.assertIn("quick_excel", excel.__all__)

    def test_excel_manager_lazy_import_targets_split_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(ExcelManager=sentinel)
        with patch("wei_data_shu.excel.import_module", return_value=fake_module) as mock_import:
            self.assertIs(excel.ExcelManager, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.excel.manager")

    def test_quick_excel_lazy_import_targets_quick_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(quick_excel=sentinel)
        with patch("wei_data_shu.excel.import_module", return_value=fake_module) as mock_import:
            self.assertIs(excel.quick_excel, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.excel.quick")


if __name__ == "__main__":
    unittest.main()
