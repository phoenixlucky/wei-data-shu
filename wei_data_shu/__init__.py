"""Public package exports for `wei-data-shu`."""

from importlib import import_module
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("wei-data-shu")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = [
    "SQLManager",
    "baseColor",
    "chartsManager",
    "excelManager",
    "fileManager",
    "mailManager",
    "ollamaManager",
    "stringManager",
    "textManager",
    "timingTool",
    "database",
    "excel",
    "mail",
    "text",
    "MySQLDatabase",
    "mav_colors",
    "TrendPredictor",
    "MultipleTrendPredictor",
    "TextAnalysis",
    "create_workbook",
    "ExcelManager",
    "ExcelHandler",
    "OpenExcel",
    "ExcelOperation",
    "quick_excel",
    "read_excel_quick",
    "FileManagement",
    "DailyEmailReport",
    "ChatBot",
    "StringBaba",
    "DateFormat",
    "decrypt",
    "eFormat",
    "textCombing",
    "fn_timer",
    "__version__",
]

_EXPORTS = {
    "SQLManager": ("wei_data_shu.SQLManager", None),
    "baseColor": ("wei_data_shu.baseColor", None),
    "chartsManager": ("wei_data_shu.chartsManager", None),
    "excelManager": ("wei_data_shu.excelManager", None),
    "fileManager": ("wei_data_shu.fileManager", None),
    "mailManager": ("wei_data_shu.mailManager", None),
    "ollamaManager": ("wei_data_shu.ollamaManager", None),
    "stringManager": ("wei_data_shu.stringManager", None),
    "textManager": ("wei_data_shu.textManager", None),
    "timingTool": ("wei_data_shu.timingTool", None),
    "database": ("wei_data_shu.database", None),
    "excel": ("wei_data_shu.excel", None),
    "mail": ("wei_data_shu.mail", None),
    "text": ("wei_data_shu.text", None),
    "MySQLDatabase": ("wei_data_shu.database", "MySQLDatabase"),
    "mav_colors": ("wei_data_shu.baseColor", "mav_colors"),
    "TrendPredictor": ("wei_data_shu.text.forecast", "TrendPredictor"),
    "MultipleTrendPredictor": ("wei_data_shu.text.forecast", "MultipleTrendPredictor"),
    "TextAnalysis": ("wei_data_shu.text.analysis", "TextAnalysis"),
    "create_workbook": ("wei_data_shu.excel", "create_workbook"),
    "ExcelManager": ("wei_data_shu.excel", "ExcelManager"),
    "ExcelHandler": ("wei_data_shu.excel", "ExcelHandler"),
    "OpenExcel": ("wei_data_shu.excel", "OpenExcel"),
    "ExcelOperation": ("wei_data_shu.excel", "ExcelOperation"),
    "quick_excel": ("wei_data_shu.excel", "quick_excel"),
    "read_excel_quick": ("wei_data_shu.excel", "read_excel_quick"),
    "FileManagement": ("wei_data_shu.fileManager", "FileManagement"),
    "DailyEmailReport": ("wei_data_shu.mail", "DailyEmailReport"),
    "ChatBot": ("wei_data_shu.ollamaManager", "ChatBot"),
    "StringBaba": ("wei_data_shu.text", "StringBaba"),
    "DateFormat": ("wei_data_shu.text", "DateFormat"),
    "decrypt": ("wei_data_shu.text", "decrypt"),
    "eFormat": ("wei_data_shu.text", "eFormat"),
    "textCombing": ("wei_data_shu.text", "textCombing"),
    "fn_timer": ("wei_data_shu.timingTool", "fn_timer"),
}


def __getattr__(name: str):
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    module = import_module(module_name)
    if attr_name is None:
        return module
    return getattr(module, attr_name)


def __dir__():
    return sorted(set(globals().keys()) | set(__all__))
