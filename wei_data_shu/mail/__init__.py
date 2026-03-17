"""Mail domain exports."""

from importlib import import_module

__all__ = ["DailyEmailReport"]


def __getattr__(name: str):
    if name != "DailyEmailReport":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module("wei_data_shu.mail.report")
    return module.DailyEmailReport
