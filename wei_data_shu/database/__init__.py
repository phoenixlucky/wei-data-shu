"""Database domain exports."""

from importlib import import_module

from .._api import make_dir, make_getattr

__all__ = ["MySQLDatabase", "MySQLDatabaseError"]

_EXPORTS = {
    "MySQLDatabase": ("wei_data_shu.database.mysql", "MySQLDatabase"),
    "MySQLDatabaseError": ("wei_data_shu.database.mysql", "MySQLDatabaseError"),
}

__getattr__ = make_getattr(__name__, _EXPORTS)
__dir__ = make_dir(__name__, _EXPORTS, extra=["__all__"])
