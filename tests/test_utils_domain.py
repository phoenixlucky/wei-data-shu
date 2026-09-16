import types
import unittest
from unittest.mock import patch

import wei_data_shu.utils as utils


class TestUtilsDomain(unittest.TestCase):
    def test_utils_package_exposes_expected_names(self):
        self.assertEqual(
            set(utils.__all__),
            {
                "fn_timer",
                "mav_colors",
                "color_records",
                "search_colors",
                "generate_password",
                "in_notebook",
                "read_text",
                "bom_tolerant_encoding",
            },
        )

    def test_utils_lazy_import_targets_textio_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(read_text=sentinel)
        with patch("wei_data_shu.utils.import_module", return_value=fake_module) as mock_import:
            self.assertIs(utils.read_text, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.utils.textio")

    def test_read_text_is_importable_from_utils_package(self):
        from wei_data_shu.utils import bom_tolerant_encoding, read_text

        self.assertTrue(callable(read_text))
        self.assertEqual(bom_tolerant_encoding("utf-8"), "utf-8-sig")
        self.assertEqual(bom_tolerant_encoding("gbk"), "gbk")

    def test_utils_lazy_import_targets_notebook_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(in_notebook=sentinel)
        with patch("wei_data_shu.utils.import_module", return_value=fake_module) as mock_import:
            self.assertIs(utils.in_notebook, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.utils.notebook")

    def test_utils_lazy_import_targets_colors_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(mav_colors=sentinel)
        with patch("wei_data_shu.utils.import_module", return_value=fake_module) as mock_import:
            self.assertIs(utils.mav_colors, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.utils.colors")

    def test_utils_lazy_import_targets_timing_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(fn_timer=sentinel)
        with patch("wei_data_shu.utils.import_module", return_value=fake_module) as mock_import:
            self.assertIs(utils.fn_timer, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.utils.timing")

    def test_utils_lazy_import_targets_password_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(generate_password=sentinel)
        with patch("wei_data_shu.utils.import_module", return_value=fake_module) as mock_import:
            self.assertIs(utils.generate_password, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.utils.passwords")


if __name__ == "__main__":
    unittest.main()
