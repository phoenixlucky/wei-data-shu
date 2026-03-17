import types
import unittest
from unittest.mock import patch

import wei_data_shu.database as database


class TestDatabaseDomain(unittest.TestCase):
    def test_database_package_is_importable(self):
        self.assertEqual(database.__all__, ["MySQLDatabase"])

    def test_database_lazy_import_targets_mysql_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(MySQLDatabase=sentinel)
        with patch("wei_data_shu.database.import_module", return_value=fake_module) as mock_import:
            self.assertIs(database.MySQLDatabase, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.database.mysql")


if __name__ == "__main__":
    unittest.main()
