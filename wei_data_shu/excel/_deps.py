"""Optional dependency helpers for the excel domain."""

from __future__ import annotations

from .._deps import require_deps as _require

_EXTRA = "excel"


def require_excel_deps(*dep_names: str) -> None:
    """Excel 能力所需依赖缺失时抛出带 ``wei-data-shu[excel]`` 安装提示的错误。"""
    _require(*dep_names, extra=_EXTRA)


__all__ = ["require_excel_deps"]
