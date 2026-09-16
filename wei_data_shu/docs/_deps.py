"""Optional dependency helpers for the docs domain.

Markdown / HTML 渲染只依赖标准库，因此始终可用；Word / PowerPoint / Excel 源分别需要
``python-docx``、``python-pptx`` 与 ``openpyxl``，统一通过 ``wei-data-shu[docs]`` 安装。

可用性用 :func:`importlib.util.find_spec` 探测——它只查找模块位置、不执行模块代码，
因此 ``import wei_data_shu.docs`` 不会顺带把这些重依赖载入 ``sys.modules``；
真正的 import 推迟到各后端函数内部。
"""

from __future__ import annotations

from importlib.util import find_spec

_INSTALL_HINT = "pip install wei-data-shu[docs]"

#: 逻辑名 -> 可导入的模块名（供 find_spec 探测）
_DEP_MODULES = {
    "docx": "docx",
    "pptx": "pptx",
    "openpyxl": "openpyxl",
}


def _is_available(dep_name: str) -> bool:
    """探测依赖是否可导入（不执行模块代码，缺失时返回 ``False``）。"""
    module_name = _DEP_MODULES.get(dep_name, dep_name)
    try:
        return find_spec(module_name) is not None
    except (ImportError, ValueError):  # 损坏的安装或非法模块名
        return False


def require_deps(*dep_names: str) -> None:
    """Raise a friendly ImportError if any required optional dependency is missing."""
    missing = [name for name in dep_names if not _is_available(name)]
    if missing:
        missing_list = ", ".join(missing)
        raise ImportError(f"当前功能缺少依赖: {missing_list}. 请安装可选依赖: {_INSTALL_HINT}")


def has_deps(*dep_names: str) -> bool:
    """Return ``True`` when every requested optional dependency is importable."""
    return all(_is_available(name) for name in dep_names)


__all__ = [
    "has_deps",
    "require_deps",
]
