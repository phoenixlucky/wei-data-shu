import types
import unittest
from unittest.mock import patch

import wei_data_shu.utils as utils


class TestUtilsDomain(unittest.TestCase):
    def test_utils_package_exposes_expected_names(self):
        self.assertEqual(
            set(utils.__all__),
            {"fn_timer", "mav_colors", "color_records", "search_colors", "generate_password"},
        )

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
