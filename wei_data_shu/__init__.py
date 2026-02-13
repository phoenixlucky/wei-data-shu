"""Public package exports for `wei_office_simptool`."""

from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
import warnings

try:
    __version__ = version("wei_office_simptool")
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
    "SQLManager": ("wei_office_simptool.SQLManager", None),
    "baseColor": ("wei_office_simptool.baseColor", None),
    "chartsManager": ("wei_office_simptool.chartsManager", None),
    "excelManager": ("wei_office_simptool.excelManager", None),
    "fileManager": ("wei_office_simptool.fileManager", None),
    "mailManager": ("wei_office_simptool.mailManager", None),
    "ollamaManager": ("wei_office_simptool.ollamaManager", None),
    "stringManager": ("wei_office_simptool.stringManager", None),
    "textManager": ("wei_office_simptool.textManager", None),
    "timingTool": ("wei_office_simptool.timingTool", None),
    "database": ("wei_office_simptool.database", None),
    "excel": ("wei_office_simptool.excel", None),
    "mail": ("wei_office_simptool.mail", None),
    "text": ("wei_office_simptool.text", None),
    "MySQLDatabase": ("wei_office_simptool.database", "MySQLDatabase"),
    "mav_colors": ("wei_office_simptool.baseColor", "mav_colors"),
    "TrendPredictor": ("wei_office_simptool.text.forecast", "TrendPredictor"),
    "MultipleTrendPredictor": ("wei_office_simptool.text.forecast", "MultipleTrendPredictor"),
    "TextAnalysis": ("wei_office_simptool.text.analysis", "TextAnalysis"),
    "create_workbook": ("wei_office_simptool.excel", "create_workbook"),
    "ExcelManager": ("wei_office_simptool.excel", "ExcelManager"),
    "ExcelHandler": ("wei_office_simptool.excel", "ExcelHandler"),
    "OpenExcel": ("wei_office_simptool.excel", "OpenExcel"),
    "ExcelOperation": ("wei_office_simptool.excel", "ExcelOperation"),
    "quick_excel": ("wei_office_simptool.excel", "quick_excel"),
    "read_excel_quick": ("wei_office_simptool.excel", "read_excel_quick"),
    "FileManagement": ("wei_office_simptool.fileManager", "FileManagement"),
    "DailyEmailReport": ("wei_office_simptool.mail", "DailyEmailReport"),
    "ChatBot": ("wei_office_simptool.ollamaManager", "ChatBot"),
    "StringBaba": ("wei_office_simptool.text", "StringBaba"),
    "DateFormat": ("wei_office_simptool.text", "DateFormat"),
    "decrypt": ("wei_office_simptool.text", "decrypt"),
    "eFormat": ("wei_office_simptool.text", "eFormat"),
    "textCombing": ("wei_office_simptool.text", "textCombing"),
    "fn_timer": ("wei_office_simptool.timingTool", "fn_timer"),
}


def __getattr__(name: str):
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    if name == "chartsManager":
        warnings.warn(
            "`wei_office_simptool.chartsManager` 已弃用，将在后续版本移除。"
            "请改用 `wei_office_simptool.text.analysis` 或 `wei_office_simptool.text.forecast`.",
            FutureWarning,
            stacklevel=2,
        )
    module_name, attr_name = target
    module = import_module(module_name)
    if attr_name is None:
        return module
    return getattr(module, attr_name)


def __dir__():
    return sorted(set(globals().keys()) | set(__all__))
