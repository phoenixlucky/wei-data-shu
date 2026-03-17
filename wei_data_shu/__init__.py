"""Public package exports for `wei-data-shu`."""

from importlib import import_module
from importlib.metadata import PackageNotFoundError, version

from ._api import ROOT_EXPORTS, export_names

try:
    __version__ = version("wei-data-shu")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = export_names(ROOT_EXPORTS) + ["__version__"]


def __getattr__(name: str):
    target = ROOT_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    module = import_module(module_name)
    if attr_name is None:
        return module
    return getattr(module, attr_name)


def __dir__():
    return sorted(set(globals().keys()) | {"__version__", "__all__"})
