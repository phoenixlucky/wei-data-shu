"""跨格式文档互转（源：``.md`` / ``.docx`` / ``.pptx`` / ``.xlsx``）。

任意两个方向都经由中间的 :class:`~wei_data_shu.docs.model.Document` 表示，
因此新增后端后互转自动可用。``.xlsx`` / ``.xlsm`` 只作为读取来源（整本工作簿
按工作表读入），不能作为转换目标。

Examples:
    >>> from wei_data_shu.docs import convert
    >>> convert("report.md", "report.docx")
    >>> convert("report.docx", "outline.pptx")
    >>> convert("sales.xlsx", "sales.md")
"""

from __future__ import annotations

from pathlib import Path

from .model import (
    READABLE_SUFFIXES,
    WRITABLE_SUFFIXES,
    PathLike,
    format_suffix,
    load_document,
    save_document,
)

SOURCE_SUFFIXES = READABLE_SUFFIXES
TARGET_SUFFIXES = WRITABLE_SUFFIXES


def convert(source: PathLike, target: PathLike, overwrite: bool = True) -> Path:
    """把 ``source`` 文档转换为 ``target`` 格式，返回写入路径。

    Args:
        source: 源文档路径，按扩展名自动选择读取后端（``.md`` / ``.docx`` / ``.pptx`` / ``.xlsx``）。
        target: 目标文档路径，按扩展名自动选择写入后端（``.md`` / ``.docx`` / ``.pptx``）。
        overwrite: 目标已存在时是否覆盖，``False`` 则抛 ``FileExistsError``。
    """
    src = Path(source)
    dst = Path(target)
    if not src.exists():
        raise FileNotFoundError(f"源文件不存在: {src}")
    if format_suffix(dst) not in TARGET_SUFFIXES:
        raise ValueError(
            f"不支持的目标格式: {dst.suffix or '(无扩展名)'!r}. 支持: {', '.join(TARGET_SUFFIXES)}"
            "（.xlsx 只能作为源格式读取，无法作为转换目标）"
        )
    if dst.exists() and not overwrite:
        raise FileExistsError(f"目标文件已存在: {dst}")

    document = load_document(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    return save_document(document, dst)


__all__ = ["SOURCE_SUFFIXES", "TARGET_SUFFIXES", "convert"]
