"""Compatibility layer for legacy `chartsManager` imports.

Deprecated:
- wei_office_simptool.chartsManager.TrendPredictor -> wei_office_simptool.text.forecast.TrendPredictor
- wei_office_simptool.chartsManager.MultipleTrendPredictor -> wei_office_simptool.text.forecast.MultipleTrendPredictor
- wei_office_simptool.chartsManager.TextAnalysis -> wei_office_simptool.text.analysis.TextAnalysis
"""

import warnings

from .text.analysis import TextAnalysis as _TextAnalysis
from .text.forecast import MultipleTrendPredictor as _MultipleTrendPredictor
from .text.forecast import TrendPredictor as _TrendPredictor

warnings.warn(
    "`wei_office_simptool.chartsManager` 已弃用，将在后续版本移除。"
    "请改用 `wei_office_simptool.text.analysis` 或 `wei_office_simptool.text.forecast`.",
    FutureWarning,
    stacklevel=2,
)


class TrendPredictor(_TrendPredictor):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "`chartsManager.TrendPredictor` 已弃用，请改用 `wei_office_simptool.text.forecast.TrendPredictor`.",
            FutureWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class MultipleTrendPredictor(_MultipleTrendPredictor):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "`chartsManager.MultipleTrendPredictor` 已弃用，请改用 `wei_office_simptool.text.forecast.MultipleTrendPredictor`.",
            FutureWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class TextAnalysis(_TextAnalysis):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "`chartsManager.TextAnalysis` 已弃用，请改用 `wei_office_simptool.text.analysis.TextAnalysis`.",
            FutureWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


__all__ = ["TrendPredictor", "MultipleTrendPredictor", "TextAnalysis"]
