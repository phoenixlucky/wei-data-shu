import types
import unittest
from unittest.mock import patch

import wei_data_shu.docs as docs


class TestDocsDomain(unittest.TestCase):
    def test_docs_package_exposes_workflow_names(self):
        self.assertIn("ExcelHandler", docs.__all__)
        self.assertIn("FileManagement", docs.__all__)

    def test_docs_lazy_import_targets_workflow_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(FileManagement=sentinel)
        with patch("wei_data_shu.docs.import_module", return_value=fake_module) as mock_import:
            self.assertIs(docs.FileManagement, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.docs.workflow")


if __name__ == "__main__":
    unittest.main()
