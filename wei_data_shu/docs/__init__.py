"""Document workflow domain exports."""

from importlib import import_module

__all__ = ["FileManagement", "ExcelHandler", "OpenExcel", "ExcelOperation", "eExcel"]


def __getattr__(name: str):
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module("wei_data_shu.docs.workflow")
    return getattr(module, name)
