"""HTML 片段渲染（Jupyter ``_repr_html_`` 预览用）。

输出是**片段**（不含 ``<html>`` / ``<body>``），可直接嵌入 Jupyter 单元格输出。
所有文本与属性值一律经 :func:`html.escape` 转义，表格使用与主题无关的 ``rgba``
边框色，在浅色与深色主题下都可读。

Examples:
    >>> from wei_data_shu.docs import Document, render_html
    >>> print(render_html(Document().add_heading("月报", 1).add_table(rows)))
"""

from __future__ import annotations

from html import escape
from typing import Any

from .model import (
    BulletList,
    CodeBlock,
    Document,
    Heading,
    Image,
    PageBreak,
    Paragraph,
    Table,
)

_TABLE_STYLE = "border-collapse:collapse;margin:8px 0;"
_CELL_STYLE = "border:1px solid rgba(128,128,128,.45);padding:4px 10px;text-align:left;"
_HEAD_STYLE = _CELL_STYLE + "background:rgba(128,128,128,.12);font-weight:600;"
_CONTAINER_STYLE = "line-height:1.6;"


def _text(value: str) -> str:
    """转义文本并把换行转为 ``<br>``（HTML 默认折叠换行符）。"""
    return escape(value, quote=False).replace("\n", "<br>")


def _table_html(table: Table) -> str:
    rows = table.normalized()
    if not rows:
        return ""
    parts = [f'<table style="{_TABLE_STYLE}">']
    body = rows
    if table.header:
        head_cells = "".join(f'<th style="{_HEAD_STYLE}">{_text(cell)}</th>' for cell in rows[0])
        parts.append(f"<thead><tr>{head_cells}</tr></thead>")
        body = rows[1:]
    if body:
        body_rows = "".join(
            "<tr>" + "".join(f'<td style="{_CELL_STYLE}">{_text(cell)}</td>' for cell in row) + "</tr>"
            for row in body
        )
        parts.append(f"<tbody>{body_rows}</tbody>")
    parts.append("</table>")
    return "".join(parts)


def _image_html(image: Image) -> str:
    src = escape(image.path or "", quote=True)
    if not image.caption:
        return f'<img src="{src}" alt="">'
    caption = _text(image.caption)
    return f'<figure><img src="{src}" alt="{escape(image.caption, quote=True)}"><figcaption>{caption}</figcaption></figure>'


def _node_html(node: Any) -> str:
    if isinstance(node, Heading):
        level = node.level
        return f"<h{level}>{_text(node.text)}</h{level}>"
    if isinstance(node, Paragraph):
        if node.style == "quote":
            return f"<blockquote><p>{_text(node.text)}</p></blockquote>"
        return f"<p>{_text(node.text)}</p>"
    if isinstance(node, BulletList):
        tag = "ol" if node.ordered else "ul"
        items = "".join(f"<li>{_text(item)}</li>" for item in node.items)
        return f"<{tag}>{items}</{tag}>"
    if isinstance(node, CodeBlock):
        language = f' class="language-{escape(node.language, quote=True)}"' if node.language else ""
        return f"<pre><code{language}>{escape(node.code)}</code></pre>"
    if isinstance(node, Table):
        return _table_html(node)
    if isinstance(node, Image):
        return _image_html(node)
    if isinstance(node, PageBreak):
        return "<hr>"
    return f"<p>{_text(str(node))}</p>"


def render_html(document: Document, include_title: bool = False) -> str:
    """把 :class:`~wei_data_shu.docs.model.Document` 渲染为 HTML 片段。"""
    blocks: list[str] = []
    if include_title and document.title:
        blocks.append(f"<h1>{_text(document.title)}</h1>")
    blocks.extend(_node_html(node) for node in document.nodes)
    body = "".join(block for block in blocks if block)
    return f'<div style="{_CONTAINER_STYLE}">{body}</div>'


__all__ = ["render_html"]
