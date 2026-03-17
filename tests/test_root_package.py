import unittest

import wei_data_shu
from wei_data_shu._api import ROOT_EXPORTS


class TestRootPackage(unittest.TestCase):
    def test_root_exports_include_only_domains(self):
        expected = {"ai", "database", "docs", "excel", "files", "mail", "text", "utils", "__version__"}
        self.assertEqual(set(wei_data_shu.__all__), expected)

    def test_root_export_map_contains_domain_packages_only(self):
        self.assertEqual(ROOT_EXPORTS["files"], ("wei_data_shu.files", None))
        self.assertEqual(ROOT_EXPORTS["utils"], ("wei_data_shu.utils", None))
        self.assertNotIn("FileManagement", ROOT_EXPORTS)
        self.assertNotIn("DateFormat", ROOT_EXPORTS)


if __name__ == "__main__":
    unittest.main()
