"""Data cleaning & preprocessing utilities (missing values, duplicates, outliers, scaling, encoding)."""

from __future__ import annotations

from typing import Any, Iterable

from ._deps import pd, require_deps

_STRATEGIES = ("mean", "median", "mode", "ffill", "bfill")
_SCALE_METHODS = ("minmax", "zscore")
_OUTLIER_METHODS = ("iqr", "zscore")


def _as_cols(df: Any, cols: Iterable[str] | None, numeric_only: bool = False) -> list[str]:
    """Resolve the target column list; default to all columns (or all numeric ones)."""
    if cols is not None:
        return list(cols)
    if numeric_only:
        return list(df.select_dtypes(include=["number"]).columns)
    return list(df.columns)


class DataCleaner:
    """Chainable data cleaning & preprocessing pipeline.

    Every cleaning method mutates and returns ``self`` so calls can be chained;
    call :attr:`df` (or :meth:`get`) at the end to obtain the result.

    Example::

        cleaned = (
            DataCleaner(df)
            .drop_missing(subset=["销售额"])
            .fill_missing(strategy="median")
            .remove_duplicates()
            .normalize(cols=["销售额"])
            .get()
        )
    """

    def __init__(self, dataframe: Any) -> None:
        require_deps("pandas")
        self.df = dataframe.copy()

    # ------------------------------------------------------------------ result
    def get(self) -> Any:
        """Return the current (cleaned) DataFrame."""
        return self.df

    # --------------------------------------------------------------- missing
    def missing_summary(self) -> Any:
        """Return per-column missing counts and ratios as a DataFrame."""
        total = len(self.df)
        counts = self.df.isna().sum()
        return pd.DataFrame({"缺失数量": counts, "缺失比例": counts / total})

    def drop_missing(
        self,
        subset: Iterable[str] | None = None,
        how: str = "any",
        thresh: int | None = None,
    ) -> "DataCleaner":
        """Drop rows containing missing values (wrapper of ``df.dropna``)."""
        if thresh is not None:
            self.df = self.df.dropna(subset=subset, thresh=thresh)
        else:
            self.df = self.df.dropna(subset=subset, how=how)
        return self

    def fill_missing(
        self,
        cols: Iterable[str] | None = None,
        value: Any = None,
        strategy: str | None = None,
    ) -> "DataCleaner":
        """Fill missing values with a constant ``value`` or a ``strategy``.

        Strategies: ``mean`` / ``median`` (numeric columns only), ``mode``,
        ``ffill`` (forward fill), ``bfill`` (backward fill).
        """
        if value is not None and strategy is None:
            strategy = "const"
        if strategy is None:
            raise ValueError(f"请指定 value 或 strategy 之一, 可选 strategy: {_STRATEGIES}")
        if strategy not in _STRATEGIES and strategy != "const":
            raise ValueError(f"不支持的填充策略: {strategy!r}, 可选: {_STRATEGIES}")

        target = _as_cols(self.df, cols, numeric_only=strategy in ("mean", "median"))
        for col in target:
            if strategy == "const":
                self.df[col] = self.df[col].fillna(value)
            elif strategy == "mean":
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif strategy == "median":
                self.df[col] = self.df[col].fillna(self.df[col].median())
            elif strategy == "mode":
                self.df[col] = self.df[col].fillna(self.df[col].mode().iloc[0])
            elif strategy == "ffill":
                self.df[col] = self.df[col].ffill()
            elif strategy == "bfill":
                self.df[col] = self.df[col].bfill()
        return self

    def interpolate_missing(
        self,
        cols: Iterable[str] | None = None,
        method: str = "linear",
    ) -> "DataCleaner":
        """Interpolate missing values in numeric columns (wrapper of ``df.interpolate``)."""
        target = _as_cols(self.df, cols, numeric_only=True)
        self.df[target] = self.df[target].interpolate(method=method)
        return self

    # ------------------------------------------------------------- duplicates
    def remove_duplicates(
        self,
        subset: Iterable[str] | None = None,
        keep: str = "first",
    ) -> "DataCleaner":
        """Drop duplicate rows (wrapper of ``df.drop_duplicates``)."""
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        return self

    # ---------------------------------------------------------------- outliers
    def _outlier_bounds(self, col: str, method: str, threshold: float) -> tuple[float, float]:
        series = self.df[col].dropna()
        if method == "iqr":
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            return q1 - threshold * iqr, q3 + threshold * iqr
        if method == "zscore":
            mean, std = series.mean(), series.std(ddof=0)
            if std == 0:
                return float("-inf"), float("inf")
            return mean - threshold * std, mean + threshold * std
        raise ValueError(f"不支持的异常值检测方法: {method!r}, 可选: {_OUTLIER_METHODS}")

    def detect_outliers(
        self,
        cols: Iterable[str] | None = None,
        method: str = "iqr",
        threshold: float | None = None,
    ) -> Any:
        """Return a boolean DataFrame marking outlier rows (True = outlier).

        ``method="iqr"`` uses the 1.5x IQR rule (customizable via ``threshold``);
        ``method="zscore"`` flags |z| > ``threshold`` (default 3).
        """
        if method not in _OUTLIER_METHODS:
            raise ValueError(f"不支持的异常值检测方法: {method!r}, 可选: {_OUTLIER_METHODS}")
        if threshold is None:
            threshold = 1.5 if method == "iqr" else 3.0
        target = _as_cols(self.df, cols, numeric_only=True)
        mask = pd.DataFrame(False, index=self.df.index, columns=target)
        for col in target:
            low, high = self._outlier_bounds(col, method, threshold)
            mask[col] = (self.df[col] < low) | (self.df[col] > high)
        return mask

    def remove_outliers(
        self,
        cols: Iterable[str] | None = None,
        method: str = "iqr",
        threshold: float | None = None,
    ) -> "DataCleaner":
        """Drop rows that are outliers in any of the target columns."""
        mask = self.detect_outliers(cols, method, threshold)
        self.df = self.df[~mask.any(axis=1)]
        return self

    def clip_outliers(
        self,
        cols: Iterable[str] | None = None,
        method: str = "iqr",
        threshold: float | None = None,
    ) -> "DataCleaner":
        """Winsorize outliers: clip values outside the bounds to the bound values."""
        if method not in _OUTLIER_METHODS:
            raise ValueError(f"不支持的异常值处理方法: {method!r}, 可选: {_OUTLIER_METHODS}")
        if threshold is None:
            threshold = 1.5 if method == "iqr" else 3.0
        for col in _as_cols(self.df, cols, numeric_only=True):
            low, high = self._outlier_bounds(col, method, threshold)
            self.df[col] = self.df[col].clip(lower=low, upper=high)
        return self

    # ---------------------------------------------------------------- scaling
    def normalize(
        self,
        cols: Iterable[str] | None = None,
        method: str = "minmax",
    ) -> "DataCleaner":
        """Scale numeric columns to a common range.

        ``method="minmax"`` maps to [0, 1]; ``method="zscore"`` standardizes
        to zero mean / unit variance.
        """
        if method not in _SCALE_METHODS:
            raise ValueError(f"不支持的归一化方法: {method!r}, 可选: {_SCALE_METHODS}")
        target = _as_cols(self.df, cols, numeric_only=True)
        for col in target:
            series = self.df[col]
            if method == "minmax":
                min_v, max_v = series.min(), series.max()
                self.df[col] = (series - min_v) / (max_v - min_v) if max_v != min_v else series * 0
            elif method == "zscore":
                mean, std = series.mean(), series.std(ddof=0)
                self.df[col] = (series - mean) / std if std else series * 0
        return self

    # ---------------------------------------------------------------- encoding
    def encode_categorical(
        self,
        cols: Iterable[str] | None = None,
        method: str = "onehot",
    ) -> "DataCleaner":
        """Encode categorical columns.

        ``method="onehot"`` creates dummy columns and drops the originals;
        ``method="label"`` maps each column to integer codes in place.
        """
        if method not in ("onehot", "label"):
            raise ValueError(f"不支持的编码方法: {method!r}, 可选: ('onehot', 'label')")
        target = _as_cols(self.df, cols)
        if method == "onehot":
            self.df = pd.get_dummies(self.df, columns=target, prefix=target, dtype=bool)
        else:
            for col in target:
                codes, _ = pd.factorize(self.df[col])
                self.df[col] = codes
        return self

    # ------------------------------------------------------------- type hints
    def infer_types(self) -> dict[str, str]:
        """Guess the semantic type of every column without modifying the data.

        Returns a mapping like ``{"销售额": "数值", "日期": "日期", "城市": "文本"}``.
        """
        result: dict[str, str] = {}
        for col in self.df.columns:
            series = self.df[col].dropna()
            if pd.api.types.is_numeric_dtype(series):
                result[col] = "数值"
            elif len(series) > 0:
                try:
                    pd.to_datetime(series)
                    result[col] = "日期"
                except (ValueError, TypeError):
                    result[col] = "文本"
            else:
                result[col] = "空列"
        return result

    def to_datetime(self, cols: Iterable[str], **kwargs: Any) -> "DataCleaner":
        """Convert the given columns to ``datetime64`` (wrapper of ``pd.to_datetime``)."""
        for col in _as_cols(self.df, cols):
            self.df[col] = pd.to_datetime(self.df[col], **kwargs)
        return self

    def to_numeric(
        self,
        cols: Iterable[str],
        errors: str = "coerce",
    ) -> "DataCleaner":
        """Convert the given columns to numeric (wrapper of ``pd.to_numeric``)."""
        for col in _as_cols(self.df, cols):
            self.df[col] = pd.to_numeric(self.df[col], errors=errors)
        return self


__all__ = ["DataCleaner"]
