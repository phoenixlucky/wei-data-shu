"""Database domain exports."""

from importlib import import_module

__all__ = ["MySQLDatabase"]


def __getattr__(name: str):
    if name != "MySQLDatabase":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module("wei_data_shu.database.mysql")
    return module.MySQLDatabase
