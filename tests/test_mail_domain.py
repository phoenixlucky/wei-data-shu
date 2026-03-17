import types
import unittest
from unittest.mock import patch

import wei_data_shu.mail as mail


class TestMailDomain(unittest.TestCase):
    def test_mail_package_is_importable(self):
        self.assertEqual(mail.__all__, ["DailyEmailReport"])

    def test_mail_lazy_import_targets_report_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(DailyEmailReport=sentinel)
        with patch("wei_data_shu.mail.import_module", return_value=fake_module) as mock_import:
            self.assertIs(mail.DailyEmailReport, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.mail.report")


if __name__ == "__main__":
    unittest.main()
