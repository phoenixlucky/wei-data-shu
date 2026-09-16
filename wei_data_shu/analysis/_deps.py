"""Optional dependency helpers for the analysis domain."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, cast

_INSTALL_HINT = "pip install wei-data-shu[analysis]"

#: 顶层导入失败的原因（依赖未安装，或已安装但安装损坏），用于给出准确的提示
_IMPORT_ERRORS: dict[str, str] = {}

try:
    import numpy as np
except ImportError as exc:  # pragma: no cover
    _IMPORT_ERRORS["numpy"] = f"{type(exc).__name__}: {exc}"
    np = cast(Any, None)

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    _IMPORT_ERRORS["pandas"] = f"{type(exc).__name__}: {exc}"
    pd = cast(Any, None)

try:
    from matplotlib import pyplot as plt
except ImportError as exc:  # pragma: no cover
    _IMPORT_ERRORS["matplotlib"] = f"{type(exc).__name__}: {exc}"
    plt = cast(Any, None)


def _is_installed(dep_name: str) -> bool:
    """依赖是否已安装：只判断模块能否被找到，不判断能否成功导入。"""
    try:
        return find_spec(dep_name) is not None
    except (ImportError, ValueError):  # 损坏的安装或非法模块名
        return False


def _describe(dep_name: str) -> str:
    """区分「未安装」与「已安装但导入失败」，避免让用户重装已装好的包。"""
    detail = _IMPORT_ERRORS.get(dep_name)
    if not _is_installed(dep_name):
        return f"{dep_name} 未安装"
    if detail:
        return f"{dep_name} 已安装但无法导入（{detail}）"
    return f"{dep_name} 不可用"


def require_deps(*dep_names: str) -> None:
    """Raise a friendly ImportError if any required optional dependency is unusable."""
    available = {
        "numpy": np,
        "pandas": pd,
        "matplotlib": plt,
    }
    unusable = [name for name in dep_names if available.get(name) is None]
    if unusable:
        details = "；".join(_describe(name) for name in unusable)
        raise ImportError(f"当前功能缺少可用依赖: {details}。请安装或修复后重试: {_INSTALL_HINT}")


__all__ = [
    "np",
    "pd",
    "plt",
    "require_deps",
]
