"""Document workflow domain exports.

文档域包含两层能力：

* 格式读写与互转：``md`` / ``word`` / ``slides`` 三种可写后端，``sheet`` 提供 ``.xlsx``
  只读源，``html`` 提供 HTML 片段预览，共用 :class:`Document` 中间模型
* 既有办公工作流：Excel 与文件操作的组合编排（``workflow``）
"""

from importlib import import_module

__all__ = [
    # --- 中间模型 ---
    "BulletList",
    "CodeBlock",
    "Document",
    "Heading",
    "Image",
    "Node",
    "PageBreak",
    "Paragraph",
    "Table",
    # --- Markdown（零第三方依赖） ---
    "df_to_markdown",
    "markdown_to_df",
    "parse_markdown",
    "read_markdown",
    "render_markdown",
    "render_table",
    "write_markdown",
    # --- HTML 片段预览（零第三方依赖） ---
    "render_html",
    # --- Word / PowerPoint（需要 wei-data-shu[docs]） ---
    "read_docx",
    "read_pptx",
    "write_docx",
    "write_pptx",
    # --- Excel 源（只读，需要 wei-data-shu[docs]） ---
    "read_xlsx",
    # --- 互转与一行式快捷 API ---
    "build",
    "convert",
    "read_doc",
    "to_docx",
    "to_markdown",
    "to_ppt",
    "to_pptx",
    "to_word",
    # --- 既有 Excel / 文件工作流 ---
    "ExcelHandler",
    "ExcelOperation",
    "FileManagement",
    "OpenExcel",
    "eExcel",
]

_EXPORTS: dict[str, tuple[str, str]] = {}


def _register(module: str, names: list[str]) -> None:
    for name in names:
        _EXPORTS[name] = (f"wei_data_shu.docs.{module}", name)


_register(
    "model",
    [
        "BulletList",
        "CodeBlock",
        "Document",
        "Heading",
        "Image",
        "Node",
        "PageBreak",
        "Paragraph",
        "Table",
    ],
)
_register(
    "md",
    [
        "df_to_markdown",
        "markdown_to_df",
        "parse_markdown",
        "read_markdown",
        "render_markdown",
        "render_table",
        "write_markdown",
    ],
)
_register("html", ["render_html"])
_register("word", ["read_docx", "write_docx"])
_register("slides", ["read_pptx", "write_pptx"])
_register("sheet", ["read_xlsx"])
_register("conversion", ["convert"])
_register("quick", ["build", "read_doc", "to_docx", "to_markdown", "to_ppt", "to_pptx", "to_word"])
_register("workflow", ["ExcelHandler", "ExcelOperation", "FileManagement", "OpenExcel", "eExcel"])


def __getattr__(name: str):
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    module = import_module(module_name)
    return getattr(module, attr_name)


def __dir__():
    return sorted(set(globals()) | set(__all__))
