"""Document workflow domain exports.

文档域包含两层能力：

* 格式读写与互转：``md`` / ``word`` / ``slides`` 三种可写后端，``sheet`` 提供 ``.xlsx``
  只读源，``html`` 提供 HTML 片段预览，共用 :class:`Document` 中间模型
* 既有办公工作流：Excel 与文件操作的组合编排（``workflow``）
"""

from importlib import import_module

from .._api import make_dir, make_getattr

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

_EXPORTS = {
    # --- 中间模型 ---
    "BulletList": ("wei_data_shu.docs.model", "BulletList"),
    "CodeBlock": ("wei_data_shu.docs.model", "CodeBlock"),
    "Document": ("wei_data_shu.docs.model", "Document"),
    "Heading": ("wei_data_shu.docs.model", "Heading"),
    "Image": ("wei_data_shu.docs.model", "Image"),
    "Node": ("wei_data_shu.docs.model", "Node"),
    "PageBreak": ("wei_data_shu.docs.model", "PageBreak"),
    "Paragraph": ("wei_data_shu.docs.model", "Paragraph"),
    "Table": ("wei_data_shu.docs.model", "Table"),
    # --- Markdown ---
    "df_to_markdown": ("wei_data_shu.docs.md", "df_to_markdown"),
    "markdown_to_df": ("wei_data_shu.docs.md", "markdown_to_df"),
    "parse_markdown": ("wei_data_shu.docs.md", "parse_markdown"),
    "read_markdown": ("wei_data_shu.docs.md", "read_markdown"),
    "render_markdown": ("wei_data_shu.docs.md", "render_markdown"),
    "render_table": ("wei_data_shu.docs.md", "render_table"),
    "write_markdown": ("wei_data_shu.docs.md", "write_markdown"),
    # --- HTML ---
    "render_html": ("wei_data_shu.docs.html", "render_html"),
    # --- Word / PowerPoint ---
    "read_docx": ("wei_data_shu.docs.word", "read_docx"),
    "write_docx": ("wei_data_shu.docs.word", "write_docx"),
    "read_pptx": ("wei_data_shu.docs.slides", "read_pptx"),
    "write_pptx": ("wei_data_shu.docs.slides", "write_pptx"),
    # --- Excel 源 ---
    "read_xlsx": ("wei_data_shu.docs.sheet", "read_xlsx"),
    # --- 互转与快捷 API ---
    "convert": ("wei_data_shu.docs.conversion", "convert"),
    "build": ("wei_data_shu.docs.quick", "build"),
    "read_doc": ("wei_data_shu.docs.quick", "read_doc"),
    "to_docx": ("wei_data_shu.docs.quick", "to_docx"),
    "to_markdown": ("wei_data_shu.docs.quick", "to_markdown"),
    "to_ppt": ("wei_data_shu.docs.quick", "to_ppt"),
    "to_pptx": ("wei_data_shu.docs.quick", "to_pptx"),
    "to_word": ("wei_data_shu.docs.quick", "to_word"),
    # --- 既有 Excel / 文件工作流 ---
    "ExcelHandler": ("wei_data_shu.docs.workflow", "ExcelHandler"),
    "ExcelOperation": ("wei_data_shu.docs.workflow", "ExcelOperation"),
    "FileManagement": ("wei_data_shu.docs.workflow", "FileManagement"),
    "OpenExcel": ("wei_data_shu.docs.workflow", "OpenExcel"),
    "eExcel": ("wei_data_shu.docs.workflow", "eExcel"),
}

__getattr__ = make_getattr(__name__, _EXPORTS)
__dir__ = make_dir(__name__, _EXPORTS, extra=["__all__"])
