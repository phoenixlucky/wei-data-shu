"""Optional dependency helpers for text analytics modules.

这里只做 ``find_spec`` 探测，不在模块导入时拉起 ``jieba`` / ``wordcloud`` /
``statsmodels`` 等重依赖；真正的 import 推迟到 :mod:`wei_data_shu.text.forecast`
与 :mod:`wei_data_shu.text.analysis` 的方法内部。
"""

from __future__ import annotations

from .._deps import require_deps

_EXTRA = "analysis"


def require_analysis_deps(*dep_names: str) -> None:
    """当前功能所需的分析依赖缺失时抛出带安装提示的 :class:`ImportError`。"""
    require_deps(*dep_names, extra=_EXTRA)


__all__ = [
    "require_analysis_deps",
]
