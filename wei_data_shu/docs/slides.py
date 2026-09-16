"""PowerPoint (``.pptx``) 读写，基于可选依赖 ``python-pptx``。

一页幻灯片 = 一个一级标题及其后续内容；正文段落与列表写入占位符文本框，
表格与图片作为独立形状插入。安装::

    pip install wei-data-shu[docs]
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ._deps import require_deps
from .model import (
    BulletList,
    CodeBlock,
    Document,
    Heading,
    Image,
    Paragraph,
    PathLike,
    Table,
)

_TABLE_LEFT_INCHES = 0.6
_TABLE_TOP_INCHES = 1.8
_TABLE_WIDTH_INCHES = 8.5
_TABLE_ROW_HEIGHT_INCHES = 0.4
_PICTURE_LEFT_INCHES = 0.8
_PICTURE_TOP_INCHES = 1.8
_PICTURE_WIDTH_INCHES = 6.0


def _slide_title(slide: Any) -> str | None:
    try:
        shape = slide.shapes.title
    except Exception:  # pragma: no cover - 依赖具体模板
        return None
    if shape is None or not shape.has_text_frame:
        return None
    return shape.text.strip() or None


def _sections(document: Document) -> list[tuple[str | None, list[Any]]]:
    """按一 / 二级标题把节点切成若干幻灯片分组（一页一个标题）。

    更深的标题（``###`` 及以下）留在所属页的正文中，避免内容被拆成碎片页。
    """
    sections: list[tuple[str | None, list[Any]]] = []
    title = document.title
    body: list[Any] = []
    for node in document.nodes:
        if isinstance(node, Heading) and node.level <= 2:
            if title or body:
                sections.append((title, body))
            title, body = node.text, []
        else:
            body.append(node)
    if title or body:
        sections.append((title, body))
    if not sections:
        sections.append((document.title or "文档", []))
    return sections


def _node_text(node: Any) -> tuple[str, bool]:
    """返回 ``(文本, 是否为列表项)``。"""
    if isinstance(node, Paragraph):
        return node.text, False
    if isinstance(node, CodeBlock):
        return node.code, False
    if isinstance(node, BulletList):
        return "\n".join(node.items), True
    return "", False


def write_pptx(document: Document, path: PathLike) -> Path:
    """把 :class:`Document` 写入 ``.pptx`` 文件，返回写入路径。"""
    require_deps("pptx")
    from pptx import Presentation
    from pptx.util import Inches

    prs = Presentation()
    title_layout = prs.slide_layouts[0]
    body_layout = prs.slide_layouts[1]

    for index, (title, nodes) in enumerate(_sections(document)):
        is_title_slide = index == 0 and not nodes
        slide = prs.slides.add_slide(title_layout if is_title_slide else body_layout)
        if title and slide.shapes.title is not None:
            slide.shapes.title.text = title
        if is_title_slide:
            continue

        placeholders = list(slide.placeholders)
        text_frame = placeholders[1].text_frame if len(placeholders) > 1 else None
        first_paragraph = True

        for node in nodes:
            if isinstance(node, Table):
                rows = node.normalized()
                if not rows:
                    continue
                shape = slide.shapes.add_table(
                    len(rows),
                    len(rows[0]),
                    Inches(_TABLE_LEFT_INCHES),
                    Inches(_TABLE_TOP_INCHES),
                    Inches(_TABLE_WIDTH_INCHES),
                    Inches(_TABLE_ROW_HEIGHT_INCHES * len(rows)),
                )
                for row_index, row in enumerate(rows):
                    for col_index, value in enumerate(row):
                        shape.table.cell(row_index, col_index).text = value
                continue

            if isinstance(node, Image):
                if node.path and Path(node.path).exists():
                    slide.shapes.add_picture(
                        node.path,
                        Inches(_PICTURE_LEFT_INCHES),
                        Inches(_PICTURE_TOP_INCHES),
                        width=Inches(_PICTURE_WIDTH_INCHES),
                    )
                continue

            text, is_list = _node_text(node)
            if not text or text_frame is None:
                continue
            for line_index, line in enumerate(text.split("\n")):
                if first_paragraph and line_index == 0:
                    paragraph = text_frame.paragraphs[0]
                    first_paragraph = False
                else:
                    paragraph = text_frame.add_paragraph()
                paragraph.text = line
                paragraph.level = 1 if is_list else 0

    target = Path(path)
    prs.save(str(target))
    return target


def read_pptx(path: PathLike) -> Document:
    """读取 ``.pptx`` 文件为 :class:`Document`（标题转一级标题，缩进项转列表）。"""
    require_deps("pptx")
    from pptx import Presentation

    prs = Presentation(str(path))
    document = Document()

    for slide in prs.slides:
        title = _slide_title(slide)
        if title:
            document.add(Heading(title, 1))

        title_shape = slide.shapes.title
        for shape in sorted(slide.shapes, key=lambda item: (item.top or 0, item.left or 0)):
            if shape is title_shape:
                continue
            if getattr(shape, "has_table", False) and shape.has_table:
                rows = [[cell.text.strip() for cell in row.cells] for row in shape.table.rows]
                if rows:
                    document.add(Table(rows, header=True))
                continue
            if not shape.has_text_frame:
                continue

            bullets: list[str] = []
            for paragraph in shape.text_frame.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue
                if (paragraph.level or 0) > 0:
                    bullets.append(text)
                    continue
                if bullets:
                    document.add(BulletList(bullets))
                    bullets = []
                document.add(Paragraph(text))
            if bullets:
                document.add(BulletList(bullets))

    return document


__all__ = ["read_pptx", "write_pptx"]
