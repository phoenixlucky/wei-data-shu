"""Excel domain exports."""

from importlib import import_module

from .._api import make_dir, make_getattr

__all__ = [
    "create_workbook",
    "ExcelManager",
    "eExcel",
    "ExcelHandler",
    "OpenExcel",
    "ExcelOperation",
    "quick_excel",
    "read_excel_quick",
]

_EXPORTS = {
    "create_workbook": ("wei_data_shu.excel._helpers", "create_workbook"),
    "ExcelManager": ("wei_data_shu.excel.manager", "ExcelManager"),
    "eExcel": ("wei_data_shu.excel.manager", "eExcel"),
    "ExcelHandler": ("wei_data_shu.excel.handler", "ExcelHandler"),
    "OpenExcel": ("wei_data_shu.excel.client", "OpenExcel"),
    "ExcelOperation": ("wei_data_shu.excel.operations", "ExcelOperation"),
    "quick_excel": ("wei_data_shu.excel.quick", "quick_excel"),
    "read_excel_quick": ("wei_data_shu.excel.quick", "read_excel_quick"),
}

__getattr__ = make_getattr(__name__, _EXPORTS)
__dir__ = make_dir(__name__, _EXPORTS, extra=["__all__"])
