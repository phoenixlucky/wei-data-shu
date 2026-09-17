"""Text domain exports."""

from importlib import import_module

from .._api import make_dir, make_getattr

__all__ = [
    "StringBaba",
    "DateFormat",
    "decrypt",
    "eFormat",
    "textCombing",
    "TrendPredictor",
    "MultipleTrendPredictor",
    "TextAnalysis",
]

_EXPORTS = {
    "StringBaba": ("wei_data_shu.text.core", "StringBaba"),
    "DateFormat": ("wei_data_shu.text.core", "DateFormat"),
    "decrypt": ("wei_data_shu.text.core", "decrypt"),
    "eFormat": ("wei_data_shu.text.core", "eFormat"),
    "textCombing": ("wei_data_shu.text.combiner", "textCombing"),
    "TrendPredictor": ("wei_data_shu.text.forecast", "TrendPredictor"),
    "MultipleTrendPredictor": ("wei_data_shu.text.forecast", "MultipleTrendPredictor"),
    "TextAnalysis": ("wei_data_shu.text.analysis", "TextAnalysis"),
}

__getattr__ = make_getattr(__name__, _EXPORTS)
__dir__ = make_dir(__name__, _EXPORTS, extra=["__all__"])
