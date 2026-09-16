"""Tests for the analysis domain (data loading, cleaning, visualization)."""

import os
import tempfile
import unittest
import warnings

warnings.filterwarnings("ignore", message="Glyph .* missing from font")
warnings.filterwarnings("ignore", message="Could not infer format")

try:
    import matplotlib

    matplotlib.use("Agg")  # headless backend, must be set before pyplot import

    import numpy as np  # noqa: E402
    import pandas as pd  # noqa: E402

    from wei_data_shu import analysis  # noqa: E402
    from wei_data_shu.analysis import (  # noqa: E402
        DataCleaner,
        plot_bar,
        plot_box,
        plot_corr_heatmap,
        plot_hist,
        plot_line,
        plot_pie,
        plot_scatter,
        read_any,
        read_csv,
        read_excel,
        read_json,
        setup_chinese_font,
    )

    _ANALYSIS_OK = True
except ImportError:  # pragma: no cover - 依赖缺失时整体跳过，而非报错
    _ANALYSIS_OK = False

_ANALYSIS_SKIP_REASON = "analysis extras 未安装或不可用（pip install wei-data-shu[analysis]）"


def _sample_df():
    return pd.DataFrame(
        {
            "城市": ["北京", "上海", "北京", "深圳", "上海"],
            "销售额": [100.0, 200.0, 150.0, 300.0, 50.0],
            "成本": [60.0, 120.0, 90.0, 180.0, 30.0],
        }
    )


@unittest.skipUnless(_ANALYSIS_OK, _ANALYSIS_SKIP_REASON)
class TestAnalysisDomainExport(unittest.TestCase):
    def test_root_package_lazy_exports_analysis(self):
        import wei_data_shu

        self.assertIn("analysis", dir(wei_data_shu))
        self.assertIs(wei_data_shu.analysis, analysis)

    def test_analysis_all_exports(self):
        for name in ("read_csv", "DataCleaner", "plot_line", "plot_corr_heatmap"):
            self.assertIn(name, analysis.__all__)


@unittest.skipUnless(_ANALYSIS_OK, _ANALYSIS_SKIP_REASON)
class TestReadIO(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def _write(self, name, content, encoding="utf-8"):
        path = os.path.join(self.tmpdir.name, name)
        with open(path, "w", encoding=encoding) as fh:
            fh.write(content)
        return path

    def test_read_csv(self):
        path = self._write("data.csv", "a,b\n1,2\n3,4\n")
        df = read_csv(path)
        self.assertEqual(df.shape, (2, 2))
        self.assertEqual(df["b"].tolist(), [2, 4])

    def test_read_json(self):
        path = self._write("data.json", '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]')
        df = read_json(path)
        self.assertEqual(df.shape, (2, 2))

    def test_read_excel(self):
        path = os.path.join(self.tmpdir.name, "data.xlsx")
        _sample_df().to_excel(path, index=False)
        df = read_excel(path)
        self.assertEqual(list(df.columns), ["城市", "销售额", "成本"])

    def test_read_any_dispatches_by_extension(self):
        csv_path = self._write("x.csv", "a\n1\n")
        json_path = self._write("y.json", '[{"a": 1}]')
        self.assertEqual(read_any(csv_path).shape, (1, 1))
        self.assertEqual(read_any(json_path).shape, (1, 1))
        with self.assertRaises(ValueError):
            read_any("unknown.parquet")


@unittest.skipUnless(_ANALYSIS_OK, _ANALYSIS_SKIP_REASON)
class TestDataCleaner(unittest.TestCase):
    def test_fill_missing_const(self):
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
        cleaned = DataCleaner(df).fill_missing(value=-1).get()
        self.assertEqual(cleaned["a"].tolist(), [1.0, -1.0, 3.0])

    def test_fill_missing_strategies(self):
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0, 100.0]})
        mean = DataCleaner(df).fill_missing(strategy="mean").get()
        self.assertAlmostEqual(mean["a"].iloc[1], 34.6666667, places=3)
        median = DataCleaner(df).fill_missing(strategy="median").get()
        self.assertEqual(median["a"].iloc[1], 3.0)
        ffill = DataCleaner(df).fill_missing(strategy="ffill").get()
        self.assertEqual(ffill["a"].iloc[1], 1.0)

    def test_fill_missing_invalid_strategy(self):
        with self.assertRaises(ValueError):
            DataCleaner(pd.DataFrame({"a": [1.0]})).fill_missing(strategy="bogus")

    def test_missing_summary(self):
        df = pd.DataFrame({"a": [1.0, np.nan, np.nan], "b": [1, 2, 3]})
        summary = DataCleaner(df).missing_summary()
        self.assertEqual(summary.loc["a", "缺失数量"], 2)
        self.assertAlmostEqual(summary.loc["a", "缺失比例"], 2 / 3)

    def test_drop_missing(self):
        df = pd.DataFrame({"a": [1.0, np.nan], "b": [1, 2]})
        cleaned = DataCleaner(df).drop_missing(subset=["a"]).get()
        self.assertEqual(len(cleaned), 1)

    def test_interpolate_missing(self):
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
        cleaned = DataCleaner(df).interpolate_missing().get()
        self.assertEqual(cleaned["a"].tolist(), [1.0, 2.0, 3.0])

    def test_remove_duplicates(self):
        df = pd.DataFrame({"a": [1, 1, 2]})
        cleaned = DataCleaner(df).remove_duplicates().get()
        self.assertEqual(len(cleaned), 2)

    def test_detect_outliers_iqr(self):
        df = pd.DataFrame({"v": [1, 2, 3, 4, 100]})
        mask = DataCleaner(df).detect_outliers(cols=["v"], method="iqr")
        self.assertEqual(mask["v"].sum(), 1)
        self.assertTrue(mask.loc[4, "v"])

    def test_detect_outliers_zscore(self):
        rng = np.random.default_rng(42)
        v = rng.normal(0, 1, 100).tolist()
        v[0] = 50.0
        df = pd.DataFrame({"v": v})
        mask = DataCleaner(df).detect_outliers(cols=["v"], method="zscore", threshold=3)
        self.assertEqual(mask["v"].sum(), 1)

    def test_remove_outliers(self):
        df = pd.DataFrame({"v": [1, 2, 3, 4, 100]})
        cleaned = DataCleaner(df).remove_outliers(cols=["v"]).get()
        self.assertEqual(cleaned["v"].max(), 4)

    def test_clip_outliers(self):
        df = pd.DataFrame({"v": [1, 2, 3, 4, 100]})
        cleaned = DataCleaner(df).clip_outliers(cols=["v"]).get()
        self.assertLessEqual(cleaned["v"].max(), 10)

    def test_normalize_minmax(self):
        df = pd.DataFrame({"v": [10.0, 20.0, 30.0]})
        cleaned = DataCleaner(df).normalize(cols=["v"], method="minmax").get()
        self.assertEqual(cleaned["v"].min(), 0.0)
        self.assertEqual(cleaned["v"].max(), 1.0)

    def test_normalize_zscore(self):
        df = pd.DataFrame({"v": [1.0, 2.0, 3.0]})
        cleaned = DataCleaner(df).normalize(cols=["v"], method="zscore").get()
        self.assertAlmostEqual(cleaned["v"].mean(), 0.0, places=6)
        self.assertAlmostEqual(cleaned["v"].std(ddof=0), 1.0, places=6)

    def test_encode_onehot(self):
        df = pd.DataFrame({"城市": ["北京", "上海", "北京"]})
        cleaned = DataCleaner(df).encode_categorical(cols=["城市"], method="onehot").get()
        self.assertIn("城市_北京", cleaned.columns)
        self.assertNotIn("城市", cleaned.columns)

    def test_encode_label(self):
        df = pd.DataFrame({"城市": ["北京", "上海", "北京"]})
        cleaned = DataCleaner(df).encode_categorical(cols=["城市"], method="label").get()
        self.assertEqual(cleaned["城市"].tolist(), [0, 1, 0])

    def test_to_datetime_and_numeric(self):
        df = pd.DataFrame({"日期": ["2026-01-01"], "金额": ["100"]})
        cleaned = DataCleaner(df).to_datetime(["日期"]).to_numeric(["金额"]).get()
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned["日期"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned["金额"]))

    def test_infer_types(self):
        df = pd.DataFrame(
            {"数值": [1, 2], "日期": ["2026-01-01", "2026-01-02"], "文本": ["a", "b"]}
        )
        types = DataCleaner(df).infer_types()
        self.assertEqual(types["数值"], "数值")
        self.assertEqual(types["日期"], "日期")
        self.assertEqual(types["文本"], "文本")

    def test_chainable_pipeline(self):
        df = _sample_df()
        cleaned = (
            DataCleaner(df)
            .remove_duplicates()
            .normalize(cols=["销售额", "成本"])
            .encode_categorical(cols=["城市"], method="onehot")
            .get()
        )
        self.assertAlmostEqual(cleaned["销售额"].max(), 1.0)
        self.assertIn("城市_北京", cleaned.columns)


@unittest.skipUnless(_ANALYSIS_OK, _ANALYSIS_SKIP_REASON)
class TestCharts(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.df = _sample_df()

    def test_setup_chinese_font_returns_name_or_none(self):
        result = setup_chinese_font()
        self.assertIsInstance(result, (str, type(None)))
        if result is not None:
            self.assertIs(matplotlib.rcParams["axes.unicode_minus"], False)

    def test_setup_chinese_font_preferred_priority(self):
        # 指定不存在的字体应返回 None 且不抛错
        self.assertIsNone(setup_chinese_font(["No Such Font ABC"]))
        # 指定存在的字体应命中
        matched = setup_chinese_font(["Microsoft YaHei", "SimHei"])
        if matched is not None:
            self.assertEqual(matched, "Microsoft YaHei")
            self.assertIn("Microsoft YaHei", matplotlib.rcParams["font.sans-serif"][0])

    def _png_path(self, name):
        return os.path.join(self.tmpdir.name, name)

    def assert_png_saved(self, path):
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_plot_line(self):
        fig = plot_line(self.df, x="城市", save_path=self._png_path("line.png"))
        self.assert_png_saved(self._png_path("line.png"))
        self.assertIsNotNone(fig)

    def test_plot_bar(self):
        plot_bar(self.df, x="城市", save_path=self._png_path("bar.png"))
        self.assert_png_saved(self._png_path("bar.png"))

    def test_plot_hist(self):
        plot_hist(self.df, col="销售额", save_path=self._png_path("hist.png"))
        self.assert_png_saved(self._png_path("hist.png"))

    def test_plot_box(self):
        plot_box(self.df, save_path=self._png_path("box.png"))
        self.assert_png_saved(self._png_path("box.png"))

    def test_plot_scatter(self):
        plot_scatter(self.df, x="销售额", y="成本", save_path=self._png_path("scatter.png"))
        self.assert_png_saved(self._png_path("scatter.png"))

    def test_plot_pie(self):
        plot_pie(self.df, col="城市", save_path=self._png_path("pie.png"))
        self.assert_png_saved(self._png_path("pie.png"))

    def test_plot_corr_heatmap(self):
        plot_corr_heatmap(
            self.df, method="pearson", save_path=self._png_path("corr.png")
        )
        self.assert_png_saved(self._png_path("corr.png"))

    def test_plot_no_numeric_raises(self):
        df = pd.DataFrame({"s": ["a", "b"]})
        with self.assertRaises(ValueError):
            plot_box(df)


if __name__ == "__main__":
    unittest.main()
