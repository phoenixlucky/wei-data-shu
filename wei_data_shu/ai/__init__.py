"""AI integrations domain exports."""

from importlib import import_module

__all__ = ["ChatBot"]


def __getattr__(name: str):
    if name != "ChatBot":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module("wei_data_shu.ai.chatbot")
    return module.ChatBot
