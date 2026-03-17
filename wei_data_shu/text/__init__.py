"""Text domain exports."""

from importlib import import_module

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


def __getattr__(name: str):
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    module = import_module(module_name)
    return getattr(module, attr_name)
