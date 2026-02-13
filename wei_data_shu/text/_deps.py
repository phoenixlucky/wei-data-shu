"""Optional dependency helpers for text analytics modules."""

from typing import Any, cast

try:
    import jieba
except ImportError:  # pragma: no cover
    jieba = cast(Any, None)

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = cast(Any, None)

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = cast(Any, None)

try:
    from matplotlib import pyplot as plt
except ImportError:  # pragma: no cover
    plt = cast(Any, None)

try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller
except ImportError:  # pragma: no cover
    ARIMA = cast(Any, None)
    adfuller = cast(Any, None)

try:
    from wordcloud import WordCloud
except ImportError:  # pragma: no cover
    WordCloud = cast(Any, None)


def require_analysis_deps(*dep_names: str) -> None:
    available = {
        "jieba": jieba,
        "numpy": np,
        "pandas": pd,
        "matplotlib": plt,
        "statsmodels": ARIMA,
        "wordcloud": WordCloud,
    }
    missing = [name for name in dep_names if available.get(name) is None]
    if missing:
        missing_list = ", ".join(missing)
        raise ImportError(
            f"当前功能缺少依赖: {missing_list}. 请安装可选依赖: pip install wei-data-shu[analysis]"
        )


__all__ = [
    "jieba",
    "np",
    "pd",
    "plt",
    "ARIMA",
    "adfuller",
    "WordCloud",
    "require_analysis_deps",
]
