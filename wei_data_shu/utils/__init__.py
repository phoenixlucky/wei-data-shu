"""General utilities domain exports."""

from importlib import import_module

__all__ = ["fn_timer", "mav_colors", "color_records", "search_colors", "generate_password"]

_EXPORTS = {
    "fn_timer": ("wei_data_shu.utils.timing", "fn_timer"),
    "mav_colors": ("wei_data_shu.utils.colors", "mav_colors"),
    "color_records": ("wei_data_shu.utils.colors", "color_records"),
    "search_colors": ("wei_data_shu.utils.colors", "search_colors"),
    "generate_password": ("wei_data_shu.utils.passwords", "generate_password"),
}


def __getattr__(name: str):
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    module = import_module(module_name)
    return getattr(module, attr_name)
