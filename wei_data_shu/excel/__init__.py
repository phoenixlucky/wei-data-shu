"""Excel domain exports."""

from importlib import import_module

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


def __getattr__(name: str):
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    module = import_module(module_name)
    return getattr(module, attr_name)
