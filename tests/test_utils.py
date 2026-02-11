import unittest

from wei_office_simptool import DateFormat, FileManagement, StringBaba, textCombing


class TestStringBaba(unittest.TestCase):
    def test_format_string_sql(self):
        data = "\napple\nbanana\n"
        self.assertEqual(StringBaba(data).format_string_sql(), '"apple","banana"')


class TestDateFormat(unittest.TestCase):
    def test_get_timeparameter_date_format(self):
        value = DateFormat(interval_day=0, timeclass="date").get_timeparameter(Format="%Y-%m-%d")
        self.assertRegex(str(value), r"^\d{4}-\d{2}-\d{2}$")


class TestFileManagement(unittest.TestCase):
    def test_add_prefix_uses_stem_when_no_chinese(self):
        manager = FileManagement()
        self.assertEqual(manager.add_prefix("report_2026.xlsx", "xls"), "report_2026.xls")


class TestTextCombing(unittest.TestCase):
    def test_remove_leading_spaces(self):
        combiner = textCombing()
        cleaned = combiner.remove_leading_spaces("   a\n    b")
        self.assertEqual(cleaned, "a\nb")


if __name__ == "__main__":
    unittest.main()
