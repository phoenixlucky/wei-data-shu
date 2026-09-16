"""Markdown 读写与表格互转（仅依赖标准库）。

覆盖 GFM 常用子集：标题、段落、有序/无序列表、引用、围栏代码块、GFM 表格、
独立成行的图片、水平分隔线（解析为 :class:`~wei_data_shu.docs.model.PageBreak`）。
行内样式（粗体 / 斜体 / 链接）按原文保留，不做富文本建模。

Examples:
    >>> from wei_data_shu.docs import read_markdown, write_markdown
    >>> doc = read_markdown("report.md")
    >>> write_markdown(doc, "copy.md")
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..utils.textio import read_text

from .model import (
    BulletList,
    CodeBlock,
    Document,
    Heading,
    Image,
    PageBreak,
    Paragraph,
    PathLike,
    Table,
    coerce_rows,
)

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_ULIST_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
_OLIST_RE = re.compile(r"^\s*\d+[.)]\s+(.*)$")
_FENCE_RE = re.compile(r"^\s*(```|~~~)\s*([\w+#.-]*)\s*$")
_IMAGE_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\)\s*$")
_HR_RE = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
_QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")


def _is_cjk(char: str) -> bool:
    """判断是否为中日韩字符（决定折行拼接时是否需要空格）。"""
    code = ord(char)
    return 0x2E80 <= code <= 0x9FFF or 0xF900 <= code <= 0xFAFF or 0xFF00 <= code <= 0xFFEF


def _join_lines(parts: list[str]) -> str:
    """把同一段落的多行合并为一行；中文之间不插空格，其余用空格。"""
    joined = ""
    for part in parts:
        if not joined:
            joined = part
        elif _is_cjk(joined[-1]) or _is_cjk(part[0]):
            joined += part
        else:
            joined += " " + part
    return joined


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def parse_markdown(text: str) -> Document:
    """把 Markdown 文本解析为 :class:`~wei_data_shu.docs.model.Document`。"""
    if text.startswith("\ufeff"):  # 调用方可能把带 BOM 的文本直接传进来
        text = text[1:]
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    document = Document()
    pending: list[str] = []

    def flush() -> None:
        if pending:
            document.add(Paragraph(_join_lines(pending)))
            pending.clear()

    index = 0
    total = len(lines)
    while index < total:
        line = lines[index]

        fence = _FENCE_RE.match(line)
        if fence:
            flush()
            marker, language = fence.group(1), fence.group(2)
            index += 1
            body: list[str] = []
            while index < total and not lines[index].strip().startswith(marker):
                body.append(lines[index])
                index += 1
            index += 1  # 跳过结束围栏
            document.add(CodeBlock("\n".join(body), language))
            continue

        if not line.strip():
            flush()
            index += 1
            continue

        heading = _HEADING_RE.match(line)
        if heading:
            flush()
            document.add(Heading(heading.group(2).strip(), len(heading.group(1))))
            index += 1
            continue

        if _HR_RE.match(line):
            flush()
            document.add(PageBreak())
            index += 1
            continue

        # GFM 表格：当前行含 "|" 且下一行是分隔行
        if "|" in line and index + 1 < total and _TABLE_SEP_RE.match(lines[index + 1]):
            flush()
            rows = [_split_table_row(line)]
            index += 2
            while index < total and lines[index].strip() and "|" in lines[index]:
                rows.append(_split_table_row(lines[index]))
                index += 1
            document.add(Table(rows, header=True))
            continue

        unordered = _ULIST_RE.match(line)
        ordered = None if unordered else _OLIST_RE.match(line)
        if unordered or ordered:
            flush()
            item_re = _OLIST_RE if ordered else _ULIST_RE
            items: list[str] = []
            while index < total:
                match = item_re.match(lines[index])
                if not match:
                    break
                items.append(match.group(1).strip())
                index += 1
            document.add(BulletList(items, ordered=ordered is not None))
            continue

        image = _IMAGE_RE.match(line)
        if image:
            flush()
            document.add(Image(image.group("src"), image.group("alt") or None))
            index += 1
            continue

        quote = _QUOTE_RE.match(line)
        if quote:
            flush()
            quoted: list[str] = []
            while index < total:
                match = _QUOTE_RE.match(lines[index])
                if not match:
                    break
                quoted.append(match.group(1).strip())
                index += 1
            document.add(Paragraph(_join_lines(quoted), "quote"))
            continue

        pending.append(line.strip())
        index += 1

    flush()
    return document


def render_table(rows: list[list[str]], header: bool = True) -> str:
    """把矩形数据渲染为 GFM 表格文本。"""
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    padded = [list(row) + [""] * (width - len(row)) for row in rows]

    def line_of(cells: list[str]) -> str:
        return "| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |"

    lines = [line_of(padded[0])]
    if header:
        lines.append("| " + " | ".join(["---"] * width) + " |")
        body = padded[1:]
    else:
        body = padded
    lines.extend(line_of(row) for row in body)
    return "\n".join(lines)


def _render_node(node: Any) -> str:
    if isinstance(node, Heading):
        return f"{'#' * node.level} {node.text}".rstrip()
    if isinstance(node, Paragraph):
        if node.style == "quote":
            return "\n".join(f"> {line}" for line in node.text.split("\n"))
        return node.text
    if isinstance(node, BulletList):
        if node.ordered:
            return "\n".join(f"{i}. {item}" for i, item in enumerate(node.items, start=1))
        return "\n".join(f"- {item}" for item in node.items)
    if isinstance(node, CodeBlock):
        return f"```{node.language}\n{node.code}\n```"
    if isinstance(node, Table):
        return render_table(node.normalized(), node.header)
    if isinstance(node, Image):
        return f"![{node.caption or ''}]({node.path or ''})"
    if isinstance(node, PageBreak):
        return "---"
    return str(node)


def render_markdown(document: Document, include_title: bool = False) -> str:
    """把 :class:`~wei_data_shu.docs.model.Document` 渲染为 Markdown 文本。"""
    blocks: list[str] = []
    if include_title and document.title:
        blocks.append(f"# {document.title}")
    blocks.extend(_render_node(node) for node in document.nodes)
    body = "\n\n".join(block for block in blocks if block != "")
    return (body.strip("\n") + "\n") if body.strip() else ""


def read_markdown(path: PathLike, encoding: str = "utf-8") -> Document:
    """读取 ``.md`` / ``.markdown`` 文件为 :class:`Document`（UTF-8 的 BOM 会被剥离）。"""
    return parse_markdown(read_text(path, encoding))


def write_markdown(
    document: Document | str,
    path: PathLike,
    encoding: str = "utf-8",
) -> Path:
    """把 :class:`Document` 或 Markdown 文本写入文件，返回写入路径。"""
    target = Path(path)
    text = document if isinstance(document, str) else render_markdown(document)
    if text and not text.endswith("\n"):
        text += "\n"
    target.write_text(text, encoding=encoding)
    return target


def df_to_markdown(data: Any) -> str:
    """把 DataFrame（或任意二维数据）转换为 Markdown 表格文本。"""
    return render_table(coerce_rows(data), header=True)


def markdown_to_df(
    text: str | Document,
    table_index: int = 0,
    as_records: bool = False,
) -> Any:
    """取文档中的第 ``table_index`` 个表格并转换为 DataFrame。

    ``as_records=True`` 时返回 ``list[dict]``，无需安装 pandas。
    """
    document = parse_markdown(text) if isinstance(text, str) else text
    tables = [node for node in document.nodes if isinstance(node, Table)]
    if not tables:
        raise ValueError("文档中未找到 Markdown 表格")
    if table_index >= len(tables):
        raise IndexError(f"table_index={table_index} 越界，文档中共有 {len(tables)} 个表格")

    rows = tables[table_index].normalized()
    header = rows[0] if rows else []
    records = [dict(zip(header, row)) for row in rows[1:]]
    if as_records:
        return records

    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "markdown_to_df 需要 pandas, 请安装可选依赖: pip install wei-data-shu[analysis]; "
            "或改用 markdown_to_df(text, as_records=True) 返回 list[dict]"
        ) from None
    return pd.DataFrame(records, columns=header)


__all__ = [
    "df_to_markdown",
    "markdown_to_df",
    "parse_markdown",
    "read_markdown",
    "render_markdown",
    "render_table",
    "write_markdown",
]
