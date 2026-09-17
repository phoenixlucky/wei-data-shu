"""General utilities domain exports."""

from importlib import import_module

from .._api import make_dir, make_getattr

__all__ = [
    "fn_timer",
    "mav_colors",
    "color_records",
    "search_colors",
    "generate_password",
    "in_notebook",
    "read_text",
    "bom_tolerant_encoding",
]

_EXPORTS = {
    "fn_timer": ("wei_data_shu.utils.timing", "fn_timer"),
    "mav_colors": ("wei_data_shu.utils.colors", "mav_colors"),
    "color_records": ("wei_data_shu.utils.colors", "color_records"),
    "search_colors": ("wei_data_shu.utils.colors", "search_colors"),
    "generate_password": ("wei_data_shu.utils.passwords", "generate_password"),
    "in_notebook": ("wei_data_shu.utils.notebook", "in_notebook"),
    "read_text": ("wei_data_shu.utils.textio", "read_text"),
    "bom_tolerant_encoding": ("wei_data_shu.utils.textio", "bom_tolerant_encoding"),
}

__getattr__ = make_getattr(__name__, _EXPORTS)
__dir__ = make_dir(__name__, _EXPORTS, extra=["__all__"])
