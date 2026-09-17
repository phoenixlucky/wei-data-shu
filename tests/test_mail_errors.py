import unittest

from wei_data_shu.mail import DailyEmailReport, MailError


class TestMailErrors(unittest.TestCase):
    def test_send_without_receivers_raises(self):
        reporter = DailyEmailReport("smtp.example.com", 465, "u", "p")
        with self.assertRaises(MailError):
            reporter.send_email()

    def test_attachment_missing_file_raises(self):
        reporter = DailyEmailReport("smtp.example.com", 465, "u", "p")
        reporter.add_receiver("a@example.com")
        with self.assertRaises(FileNotFoundError):
            reporter.set_email_content("subject", "body", file_paths=["/nonexistent"], file_names=["a.txt"])

    def test_attachment_length_mismatch_raises(self):
        reporter = DailyEmailReport("smtp.example.com", 465, "u", "p")
        with self.assertRaises(ValueError):
            reporter.set_email_content("subject", "body", file_paths=["/a", "/b"], file_names=["only-one.txt"])

    def test_missing_body_raises(self):
        reporter = DailyEmailReport("smtp.example.com", 465, "u", "p")
        with self.assertRaises(ValueError):
            reporter.set_email_content("subject", None)

    def test_daily_report_without_body_raises_before_sending(self):
        reporter = DailyEmailReport("smtp.example.com", 465, "u", "p")
        reporter.add_receiver("a@example.com")
        with self.assertRaises(ValueError):
            reporter.send_daily_report("日报")


if __name__ == "__main__":
    unittest.main()
