"""Mail domain exports."""

from importlib import import_module

from .._api import make_dir, make_getattr

__all__ = ["DailyEmailReport", "MailError"]

_EXPORTS = {
    "DailyEmailReport": ("wei_data_shu.mail.report", "DailyEmailReport"),
    "MailError": ("wei_data_shu.mail.report", "MailError"),
}

__getattr__ = make_getattr(__name__, _EXPORTS)
__dir__ = make_dir(__name__, _EXPORTS, extra=["__all__"])
