"""Shared optional-dependency helpers.

各领域对可选依赖的探测方式并不相同：``analysis`` 需要在导入时就拿到
``numpy`` / ``pandas`` / ``matplotlib`` 对象；``docs`` 只做 ``find_spec`` 探测
（刻意不 import 重依赖）；``text`` 与 ``excel`` 只在调用时探测。这里只统一
「依赖名 -> 模块名」的映射与提示信息的拼装，探测策略仍由调用方决定。

调用方可以传入自定义的 ``installed`` 回调（例如领域内用可被 mock 的
``find_spec`` 实现），从而在保持提示一致的同时保留各域的可测试性。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from importlib.util import find_spec

#: 逻辑依赖名 -> 可导入的模块名
DEPENDENCY_MODULES: dict[str, str] = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "statsmodels": "statsmodels",
    "jieba": "jieba",
    "wordcloud": "wordcloud",
    "docx": "docx",
    "pptx": "pptx",
    "openpyxl": "openpyxl",
    "mysql": "mysql.connector",
    "xlwings": "xlwings",
}


def module_name(dep_name: str) -> str:
    """把逻辑依赖名映射为可导入的模块名。"""
    return DEPENDENCY_MODULES.get(dep_name, dep_name)


def is_installed(dep_name: str) -> bool:
    """依赖是否已安装：只判断模块能否被找到，不判断能否成功导入。"""
    try:
        return find_spec(module_name(dep_name)) is not None
    except (ImportError, ValueError):  # 损坏的安装或非法模块名
        return False


def install_hint(extra: str) -> str:
    return f"pip install wei-data-shu[{extra}]"


def describe(
    dep_name: str,
    *,
    import_error: str | None = None,
    installed: Callable[[str], bool] = is_installed,
) -> str:
    """区分「未安装」与「已安装但导入失败」，避免让用户重装已装好的包。"""
    if not installed(dep_name):
        return f"{dep_name} 未安装"
    if import_error:
        return f"{dep_name} 已安装但无法导入（{import_error}）"
    return f"{dep_name} 不可用"


def missing_message(
    unusable: Iterable[str],
    extra: str,
    *,
    import_errors: Mapping[str, str] | None = None,
    installed: Callable[[str], bool] = is_installed,
) -> str:
    """拼装统一的「缺少可用依赖」提示。"""
    errors = import_errors or {}
    details = "；".join(describe(name, import_error=errors.get(name), installed=installed) for name in unusable)
    return f"当前功能缺少可用依赖: {details}。请安装或修复后重试: {install_hint(extra)}"


def require_deps(
    *dep_names: str,
    extra: str,
    installed: Callable[[str], bool] = is_installed,
) -> None:
    """任一依赖不可用时抛出带安装提示的 :class:`ImportError`。"""
    unusable = [name for name in dep_names if not installed(name)]
    if unusable:
        raise ImportError(missing_message(unusable, extra, installed=installed))


__all__ = [
    "DEPENDENCY_MODULES",
    "describe",
    "install_hint",
    "is_installed",
    "missing_message",
    "module_name",
    "require_deps",
]
