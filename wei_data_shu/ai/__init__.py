"""AI integrations domain exports."""

from importlib import import_module

from .._api import make_dir, make_getattr

__all__ = ["ChatBot"]

_EXPORTS = {
    "ChatBot": ("wei_data_shu.ai.chatbot", "ChatBot"),
}

__getattr__ = make_getattr(__name__, _EXPORTS)
__dir__ = make_dir(__name__, _EXPORTS, extra=["__all__"])
