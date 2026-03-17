import types
import unittest
from unittest.mock import patch

import wei_data_shu.ai as ai


class TestAiDomain(unittest.TestCase):
    def test_ai_package_is_importable(self):
        self.assertEqual(ai.__all__, ["ChatBot"])

    def test_ai_lazy_import_targets_chatbot_module(self):
        sentinel = object()
        fake_module = types.SimpleNamespace(ChatBot=sentinel)
        with patch("wei_data_shu.ai.import_module", return_value=fake_module) as mock_import:
            self.assertIs(ai.ChatBot, sentinel)
        mock_import.assert_called_once_with("wei_data_shu.ai.chatbot")


if __name__ == "__main__":
    unittest.main()
