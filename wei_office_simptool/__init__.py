"""Public package exports for `wei_office_simptool`."""

from importlib.metadata import PackageNotFoundError, version

from . import SQLManager, baseColor, chartsManager, excelManager, fileManager, mailManager, ollamaManager, stringManager, textManager, timingTool
from .SQLManager import MySQLDatabase
from .baseColor import mav_colors
from .chartsManager import MultipleTrendPredictor, TextAnalysis, TrendPredictor
from .excelManager import ExcelHandler, ExcelManager, ExcelOperation, OpenExcel, create_workbook, quick_excel, read_excel_quick
from .fileManager import FileManagement
from .mailManager import DailyEmailReport
from .ollamaManager import ChatBot
from .stringManager import DateFormat, StringBaba, decrypt, eFormat
from .textManager import textCombing
from .timingTool import fn_timer

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
