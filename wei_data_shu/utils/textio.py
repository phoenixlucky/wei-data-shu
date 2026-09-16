"""Plain-text reading that stays transparent to a UTF-8 BOM.

Windows 上的常见工具（记事本「另存为 UTF-8」、Excel 导出的 CSV 等）会在文件开头
写入 BOM（``\\ufeff``）。以 ``utf-8`` 读取时 BOM 会作为首字符留在文本里，导致
Markdown 首行标题降级成段落、编号列表首行识别不出、CSV 首个列名多出一个不可见
字符；``utf-8-sig`` 在无 BOM 时与 ``utf-8`` 完全等价，有 BOM 时自动剥离。
"""

from __future__ import annotations

from pathlib import Path


def bom_tolerant_encoding(encoding: str = "utf-8") -> str:
    """把 UTF-8 编码名归一为 ``utf-8-sig``，其余编码原样返回。"""
    normalized = encoding.lower().replace("-", "").replace("_", "")
    return "utf-8-sig" if normalized in {"utf8", "utf8sig"} else encoding


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """读取文本文件，UTF-8 输入自动剥离 BOM。"""
    return Path(path).read_text(encoding=bom_tolerant_encoding(encoding))


__all__ = [
    "bom_tolerant_encoding",
    "read_text",
]
