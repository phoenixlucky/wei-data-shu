import unittest

from wei_data_shu.files import FileManagement


class TestFilesDomain(unittest.TestCase):
    def test_add_prefix_uses_stem_when_no_chinese(self):
        manager = FileManagement()
        self.assertEqual(manager.add_prefix("report_2026.xlsx", "xls"), "report_2026.xls")


if __name__ == "__main__":
    unittest.main()
