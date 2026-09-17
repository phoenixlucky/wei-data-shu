"""Public package exports for `wei-data-shu`."""

from importlib import import_module
from importlib.metadata import PackageNotFoundError, version

from ._api import ROOT_EXPORTS, export_names, make_dir, make_getattr

try:
    __version__ = version("wei-data-shu")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = export_names(ROOT_EXPORTS) + ["__version__"]

__getattr__ = make_getattr(__name__, ROOT_EXPORTS)
__dir__ = make_dir(__name__, ROOT_EXPORTS, extra=["__version__", "__all__"])
