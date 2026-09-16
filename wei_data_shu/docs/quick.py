"""一行式文档快捷 API：把数据/文本直接变成 Markdown、Word 或 PPT。

Examples:
    >>> from wei_data_shu.docs import to_markdown, to_word, to_ppt
    >>> to_word(rows, "report.docx", title="月度报告")   # noqa: DOC502 - 示例
    >>> to_ppt({"华东": rows, "华南": rows}, "report.pptx", title="月度报告")

``data`` 支持：:class:`Document`、DataFrame、嵌套列表（表格）、``list[str]``（列表项）、
``dict``（键作小标题）、普通字符串（段落）。
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any

from .conversion import convert
from .model import Document, PathLike, load_document, save_document


def _is_tabular(data: Any) -> bool:
    """判断是否为表格型数据（DataFrame 或二维序列）。"""
    if hasattr(data, "columns") and hasattr(data, "itertuples"):
        return True
    if isinstance(data, (str, bytes, Mapping, Document)):
        return False
    if isinstance(data, Iterable):
        rows = list(data)
        return bool(rows) and all(isinstance(row, (list, tuple)) for row in rows)
    return False


def _normalize(data: Any) -> Any:
    return list(data) if isinstance(data, Iterator) else data


def build(data: Any, title: str | None = None) -> Document:
    """把任意受支持的数据结构转换为 :class:`Document`。"""
    data = _normalize(data)
    if isinstance(data, Document):
        if title and not data.title:
            data.title = title
        return data

    document = Document(title=title)
    if title:
        document.add_heading(title, 1)

    if _is_tabular(data):
        document.add_table(data)
    elif isinstance(data, Mapping):
        for key, value in data.items():
            document.add_heading(str(key), 2)
            value = _normalize(value)
            if _is_tabular(value):
                document.add_table(value)
            elif isinstance(value, (list, tuple)):
                document.add_bullets([str(item) for item in value])
            elif isinstance(value, str):
                document.add_paragraph(value)
            else:
                document.add_paragraph(str(value))
    elif isinstance(data, str):
        document.add_paragraph(data)
    elif isinstance(data, Iterable):
        items = list(data)
        if items and all(isinstance(item, str) for item in items):
            document.add_bullets(items)
        elif items:
            document.add_table(items)
    else:
        document.add_paragraph(str(data))
    return document


def to_markdown(data: Any, path: PathLike | None = None, title: str | None = None) -> str | Path:
    """转换为 Markdown：给 ``path`` 时写入文件并返回路径，否则返回文本。"""
    text = build(data, title).to_markdown()
    if path is None:
        return text
    target = Path(path)
    target.write_text(text, encoding="utf-8")
    return target


def to_word(data: Any, path: PathLike, title: str | None = None) -> Path:
    """写出 ``.docx`` 文件（需要 ``wei-data-shu[docs]``）。"""
    return save_document(build(data, title), path)


def to_ppt(data: Any, path: PathLike, title: str | None = None) -> Path:
    """写出 ``.pptx`` 文件（需要 ``wei-data-shu[docs]``）。"""
    return save_document(build(data, title), path)


def read_doc(path: PathLike) -> Document:
    """读取 ``.md`` / ``.docx`` / ``.pptx`` / ``.xlsx`` / ``.xlsm`` 为 :class:`Document`。"""
    return load_document(path)


to_docx = to_word
to_pptx = to_ppt

__all__ = [
    "build",
    "convert",
    "read_doc",
    "to_docx",
    "to_markdown",
    "to_ppt",
    "to_pptx",
    "to_word",
]
