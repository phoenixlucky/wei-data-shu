"""Jupyter / Notebook 运行环境探测。

Notebook 里 ``matplotlib`` 使用 inline 后端：函数返回的 Figure 会自动内联渲染，
无需调用会阻塞的 ``plt.show()``。图表函数据此调整显示行为。
"""

from __future__ import annotations

_NOTEBOOK_SHELLS = {"ZMQInteractiveShell", "Shell", "TerminalInteractiveShell"}


def in_notebook() -> bool:
    """当前代码是否运行在 Jupyter Notebook / JupyterLab / Colab 等交互内核中。"""
    try:
        from IPython import get_ipython  # type: ignore[import-untyped]
    except ImportError:
        return False
    shell = get_ipython()
    if shell is None:
        return False
    return type(shell).__name__ in _NOTEBOOK_SHELLS


__all__ = ["in_notebook"]
