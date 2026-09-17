import base64
import json
import os
import tempfile
import unittest

from wei_data_shu.text import DateFormat, StringBaba, textCombing
from wei_data_shu.text import _deps as text_deps

try:
    import jieba  # noqa: F401
    import matplotlib  # noqa: F401
    import numpy  # noqa: F401
    import pandas  # noqa: F401
    import statsmodels  # noqa: F401
    import wordcloud  # noqa: F401

    _ANALYSIS_DEPS_OK = True
except ImportError:  # pragma: no cover - 依赖缺失时跳过，而非报错
    _ANALYSIS_DEPS_OK = False

_SKIP_REASON = "analysis extras 未安装或不可用（pip install wei-data-shu[analysis]）"


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


class TestTextDepsAreLazy(unittest.TestCase):
    def test_heavy_dependencies_are_not_imported_by_deps_module(self):
        for name in ("jieba", "np", "pd", "plt", "ARIMA", "WordCloud"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(text_deps, name))


class TestTextCombingSeparators(unittest.TestCase):
    def test_missing_config_means_no_punctuation(self):
        self.assertEqual(textCombing()._separators, "")

    def test_unreadable_config_is_tolerated(self):
        combiner = textCombing(separator_config=os.path.join("does", "not", "exist.json"))
        self.assertEqual(combiner._separators, "")

    def test_separators_are_loaded_once_from_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = os.path.join(tmp, "character.json")
            with open(config, "w", encoding="utf-8") as handle:
                json.dump({"separator": ["。", "，", "！"]}, handle)
            combiner = textCombing(separator_config=config)
            self.assertEqual(combiner._separators, "。，！")

    def test_process_text_adds_punctuation_when_configured(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = os.path.join(tmp, "character.json")
            with open(config, "w", encoding="utf-8") as handle:
                json.dump({"separator": ["。", "，"]}, handle)
            combiner = textCombing(separator_config=config)
            self.assertEqual(combiner.process_text("第一行\n第二行"), "第一行，第二行。")

    def test_process_text_without_config_still_terminates(self):
        result = textCombing().process_text("第一行\n第二行")
        self.assertTrue(result.endswith("。"))


class TestCoreHelpers(unittest.TestCase):
    def test_decrypt_reverses_the_sampling_scheme(self):
        from wei_data_shu.text import decrypt

        plain = "AAAAAA1200"
        encoded = base64.b64encode(plain.encode("utf-8")).decode("ascii")
        self.assertEqual(decrypt(encoded), plain)

    def test_decrypt_returns_none_for_garbage(self):
        from wei_data_shu.text import decrypt

        with self.assertLogs("wei_data_shu.text.core", level="WARNING"):
            self.assertIsNone(decrypt("not-base64!!"))

    def test_eformat_tuple_sql(self):
        from wei_data_shu.text import eFormat

        self.assertEqual(eFormat([("a",), ("b",)]).toTuple(), b"(binary('a'),binary('b'))")

    def test_eformat_empty_returns_none(self):
        from wei_data_shu.text import eFormat

        self.assertIsNone(eFormat([]).toTuple())


@unittest.skipUnless(_ANALYSIS_DEPS_OK, _SKIP_REASON)
class TestTextAnalysisDeps(unittest.TestCase):
    def test_compute_word_freq_counts_tokens(self):
        from wei_data_shu.text import TextAnalysis

        counter = TextAnalysis(None).compute_word_freq("北京 北京 上海")
        self.assertGreaterEqual(counter["北京"], 2)


@unittest.skipUnless(_ANALYSIS_DEPS_OK, _SKIP_REASON)
class TestTrendPredictor(unittest.TestCase):
    def _frame(self):
        import numpy as np
        import pandas as pd

        dates = pd.date_range("2026-01-01", periods=40, freq="B").strftime("%Y-%m-%d")
        values = np.linspace(10.0, 60.0, 40) + np.sin(np.arange(40))
        return pd.DataFrame({"日期": dates, "均值": values})

    def test_forecast_data_returns_future_rows(self):
        from wei_data_shu.text import TrendPredictor

        predictor = TrendPredictor(self._frame(), "日期", "均值", steps=5)
        future, _forecast, _strings, _dates = predictor.forecast_data()
        self.assertEqual(len(future), 5)
        self.assertIn("预测值", future.columns)

    def test_multiple_trend_predictor_returns_requested_steps(self):
        import numpy as np
        import pandas as pd

        from wei_data_shu.text import MultipleTrendPredictor

        index = pd.date_range("2026-01-01", periods=40, freq="B")
        frame = pd.DataFrame({"a": np.arange(40) + 10.0, "b": np.arange(40) + 20.0}, index=index)
        result = MultipleTrendPredictor(frame, steps=3).predict()
        self.assertEqual(len(result), 3)
        self.assertEqual(list(result.columns), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
