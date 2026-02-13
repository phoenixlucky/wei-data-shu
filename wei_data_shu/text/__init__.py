"""Text domain exports with lazy optional analysis imports."""

from importlib import import_module

from ..stringManager import DateFormat, StringBaba, decrypt, eFormat
from ..textManager import textCombing

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

_OPTIONAL_EXPORTS = {
    "TrendPredictor": ("wei_office_simptool.text.forecast", "TrendPredictor"),
    "MultipleTrendPredictor": ("wei_office_simptool.text.forecast", "MultipleTrendPredictor"),
    "TextAnalysis": ("wei_office_simptool.text.analysis", "TextAnalysis"),
}


def __getattr__(name: str):
    target = _OPTIONAL_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    module = import_module(module_name)
    return getattr(module, attr_name)
