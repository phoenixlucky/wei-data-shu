import unittest

from wei_data_shu.text import DateFormat, StringBaba, textCombing


class TestTextDomain(unittest.TestCase):
    def test_string_baba_formats_sql_list(self):
        data = "\napple\nbanana\n"
        self.assertEqual(StringBaba(data).format_string_sql(), '"apple","banana"')

    def test_date_format_returns_date_string(self):
        value = DateFormat(interval_day=0, timeclass="date").get_timeparameter(Format="%Y-%m-%d")
        self.assertRegex(str(value), r"^\d{4}-\d{2}-\d{2}$")

    def test_text_combing_removes_leading_spaces(self):
        combiner = textCombing()
        self.assertEqual(combiner.remove_leading_spaces("   a\n    b"), "a\nb")


if __name__ == "__main__":
    unittest.main()
