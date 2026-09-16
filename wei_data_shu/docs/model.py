"""与格式无关的文档中间模型（Markdown / Word / PowerPoint / Excel 的公共表示）。

各后端只需实现 ``Document <-> 自身格式`` 的转换，任意两方互转即自动成立：

.. code-block:: text

    .xlsx  --->  Document  <->  .md / .docx / .pptx

其中 ``.xlsx`` / ``.xlsm`` 仅作为**源**格式（只读），其余三种可读可写。

常用链式构造::

    from wei_data_shu.docs import Document

    Document().add_heading("月度报告", 1).add_paragraph("本月概览").add_table(rows).save("report.md")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Union

PathLike = Union[str, Path]

_MARKDOWN_SUFFIXES = {".md", ".markdown"}
_WORD_SUFFIXES = {".docx"}
_SLIDES_SUFFIXES = {".pptx"}
_EXCEL_SUFFIXES = {".xlsx", ".xlsm"}

READABLE_SUFFIXES = tuple(sorted(_MARKDOWN_SUFFIXES | _WORD_SUFFIXES | _SLIDES_SUFFIXES | _EXCEL_SUFFIXES))
WRITABLE_SUFFIXES = tuple(sorted(_MARKDOWN_SUFFIXES | _WORD_SUFFIXES | _SLIDES_SUFFIXES))


@dataclass
class Heading:
    """标题节点，``level`` 取值 1-6。"""

    text: str
    level: int = 1

    def __post_init__(self) -> None:
        self.level = max(1, min(6, int(self.level)))


@dataclass
class Paragraph:
    """普通段落；``style`` 目前支持 ``"quote"``（引用块）。"""

    text: str
    style: str | None = None


@dataclass
class BulletList:
    """列表节点，``ordered=True`` 时为有序列表。"""

    items: list[str] = field(default_factory=list)
    ordered: bool = False


@dataclass
class CodeBlock:
    """代码块节点。"""

    code: str
    language: str = ""


@dataclass
class Table:
    """表格节点；``header=True`` 时第一行作为表头。"""

    rows: list[list[str]] = field(default_factory=list)
    header: bool = True

    def __post_init__(self) -> None:
        self.rows = [[_as_cell(cell) for cell in row] for row in self.rows]

    @property
    def n_cols(self) -> int:
        return max((len(row) for row in self.rows), default=0)

    def normalized(self) -> list[list[str]]:
        """把每行补齐到相同列数，返回矩形数据（避免后端因参差行报错）。"""
        width = self.n_cols
        return [list(row) + [""] * (width - len(row)) for row in self.rows]


@dataclass
class Image:
    """图片节点；``caption`` 同时用作 Markdown 的 alt 文本。"""

    path: str | None = None
    caption: str | None = None

    def __post_init__(self) -> None:
        if self.path is not None:
            self.path = str(self.path)


@dataclass
class PageBreak:
    """分页节点（Markdown 渲染为水平分隔线）。"""


Node = Union[Heading, Paragraph, BulletList, CodeBlock, Table, Image, PageBreak]


def _as_cell(value: Any) -> str:
    if value is None:
        return ""
    return value if isinstance(value, str) else str(value)


def coerce_rows(data: Any) -> list[list[str]]:
    """把 DataFrame 或二维可迭代对象统一成 ``list[list[str]]``。

    pandas DataFrame 会带上表头行，其余数据逐行转为字符串（``None`` 视为空串）。
    """
    if hasattr(data, "columns") and hasattr(data, "itertuples"):  # pandas.DataFrame 鸭子类型
        header = [_as_cell(col) for col in data.columns]
        body = [[_as_cell(cell) for cell in row] for row in data.itertuples(index=False, name=None)]
        return [header] + body
    return [[_as_cell(cell) for cell in row] for row in data]


def format_suffix(path: PathLike) -> str:
    return Path(path).suffix.lower()


def save_document(document: "Document", path: PathLike) -> Path:
    """按扩展名把 :class:`Document` 写成 ``.md`` / ``.docx`` / ``.pptx``。"""
    target = Path(path)
    suffix = format_suffix(target)
    if suffix in _MARKDOWN_SUFFIXES:
        from .md import write_markdown

        write_markdown(document, target)
    elif suffix in _WORD_SUFFIXES:
        from .word import write_docx

        write_docx(document, target)
    elif suffix in _SLIDES_SUFFIXES:
        from .slides import write_pptx

        write_pptx(document, target)
    else:
        raise ValueError(
            f"不支持的输出格式: {suffix or '(无扩展名)'!r}. 支持: {', '.join(WRITABLE_SUFFIXES)}"
            "（.xlsx 仅可作为读取来源）"
        )
    return target


def load_document(path: PathLike) -> "Document":
    """按扩展名读取 ``.md`` / ``.docx`` / ``.pptx`` / ``.xlsx`` 为 :class:`Document`。"""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"文件不存在: {source}")
    suffix = format_suffix(source)
    if suffix in _MARKDOWN_SUFFIXES:
        from .md import read_markdown

        return read_markdown(source)
    if suffix in _WORD_SUFFIXES:
        from .word import read_docx

        return read_docx(source)
    if suffix in _SLIDES_SUFFIXES:
        from .slides import read_pptx

        return read_pptx(source)
    if suffix in _EXCEL_SUFFIXES:
        from .sheet import read_xlsx

        return read_xlsx(source)
    raise ValueError(
        f"不支持的输入格式: {suffix or '(无扩展名)'!r}. 支持: {', '.join(READABLE_SUFFIXES)}"
    )


@dataclass
class Document:
    """格式无关的文档对象：一组有序节点 + 可选标题与元数据。"""

    title: str | None = None
    nodes: list[Node] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------ 构建
    def add(self, node: Node) -> "Document":
        """追加任意节点，返回自身以支持链式调用。"""
        self.nodes.append(node)
        return self

    def add_heading(self, text: str, level: int = 1) -> "Document":
        return self.add(Heading(text, level))

    def add_paragraph(self, text: str, style: str | None = None) -> "Document":
        return self.add(Paragraph(text, style))

    def add_quote(self, text: str) -> "Document":
        return self.add(Paragraph(text, "quote"))

    def add_bullets(self, items: Iterable[str], ordered: bool = False) -> "Document":
        return self.add(BulletList([str(item) for item in items], ordered))

    def add_code(self, code: str, language: str = "") -> "Document":
        return self.add(CodeBlock(code.strip("\n"), language))

    def add_table(self, data: Any, header: bool = True) -> "Document":
        """追加表格；``data`` 可以是 DataFrame、嵌套列表或任意二维可迭代对象。"""
        return self.add(Table(coerce_rows(data), header))

    def add_image(self, path: PathLike, caption: str | None = None) -> "Document":
        return self.add(Image(str(path), caption))

    def add_page_break(self) -> "Document":
        return self.add(PageBreak())

    # ------------------------------------------------------------------ 读取
    def __iter__(self) -> Iterator[Node]:
        return iter(self.nodes)

    def __len__(self) -> int:
        return len(self.nodes)

    def __getitem__(self, index: int) -> Node:
        return self.nodes[index]

    def __repr__(self) -> str:
        return f"Document(title={self.title!r}, nodes={len(self.nodes)})"

    def _repr_markdown_(self) -> str:
        """Jupyter 中把文档渲染为 Markdown 预览。"""
        return self.to_markdown()

    def _repr_html_(self) -> str:
        """Jupyter 中把文档渲染为 HTML 预览（表格带边框；同时存在时优先于 Markdown）。"""
        return self.to_html()

    # ------------------------------------------------------------ 序列化/反序列化
    def to_markdown(self) -> str:
        from .md import render_markdown

        return render_markdown(self)

    def to_html(self, include_title: bool = False) -> str:
        """渲染为 HTML 片段（不含 ``<html>`` / ``<body>``，可直接嵌入网页或 notebook）。"""
        from .html import render_html

        return render_html(self, include_title)

    def save(self, path: PathLike) -> Path:
        """按扩展名保存（``.md`` / ``.docx`` / ``.pptx``），返回写入路径。"""
        return save_document(self, path)

    @classmethod
    def open(cls, path: PathLike) -> "Document":
        """按扩展名读取文档（``.md`` / ``.docx`` / ``.pptx`` / ``.xlsx``）。"""
        return load_document(path)


__all__ = [
    "BulletList",
    "CodeBlock",
    "Document",
    "Heading",
    "Image",
    "Node",
    "PageBreak",
    "Paragraph",
    "READABLE_SUFFIXES",
    "Table",
    "WRITABLE_SUFFIXES",
    "coerce_rows",
    "format_suffix",
    "load_document",
    "save_document",
]
