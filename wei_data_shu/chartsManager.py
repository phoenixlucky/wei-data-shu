"""Compatibility layer for legacy `chartsManager` imports.

Deprecated:
- wei_data_shu.chartsManager.TrendPredictor -> wei_data_shu.text.forecast.TrendPredictor
- wei_data_shu.chartsManager.MultipleTrendPredictor -> wei_data_shu.text.forecast.MultipleTrendPredictor
- wei_data_shu.chartsManager.TextAnalysis -> wei_data_shu.text.analysis.TextAnalysis
"""

import warnings

from .text.analysis import TextAnalysis as _TextAnalysis
from .text.forecast import MultipleTrendPredictor as _MultipleTrendPredictor
from .text.forecast import TrendPredictor as _TrendPredictor

warnings.warn(
    "`wei_data_shu.chartsManager` 已弃用，将在后续版本移除。"
    "请改用 `wei_data_shu.text.analysis` 或 `wei_data_shu.text.forecast`.",
    FutureWarning,
    stacklevel=2,
)


class TrendPredictor(_TrendPredictor):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "`chartsManager.TrendPredictor` 已弃用，请改用 `wei_data_shu.text.forecast.TrendPredictor`.",
            FutureWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class MultipleTrendPredictor(_MultipleTrendPredictor):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "`chartsManager.MultipleTrendPredictor` 已弃用，请改用 `wei_data_shu.text.forecast.MultipleTrendPredictor`.",
            FutureWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class TextAnalysis(_TextAnalysis):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "`chartsManager.TextAnalysis` 已弃用，请改用 `wei_data_shu.text.analysis.TextAnalysis`.",
            FutureWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


__all__ = ["TrendPredictor", "MultipleTrendPredictor", "TextAnalysis"]
