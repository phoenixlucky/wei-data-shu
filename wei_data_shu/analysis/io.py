"""Universal data loading helpers (files/URLs -> DataFrame)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ._deps import pd, require_deps

_CSV_ALIASES = {".csv", ".tsv", ".txt"}
_EXCEL_ALIASES = {".xlsx", ".xls", ".xlsm"}

#: 未显式指定编码时依次尝试的候选：``utf-8-sig`` 剥离 BOM，``gbk`` 兜底 Excel 导出的中文 CSV
_FALLBACK_ENCODINGS = ("utf-8-sig", "gbk")


def _read_text_data(reader: Any, path: str | Path, encoding: str | None, kwargs: dict[str, Any]) -> Any:
    """用候选编码读取文本数据；显式传入 ``encoding`` 时只用该编码。"""
    if encoding is not None:
        return reader(path, encoding=encoding, **kwargs)
    error: UnicodeDecodeError | None = None
    for candidate in _FALLBACK_ENCODINGS:
        try:
            return reader(path, encoding=candidate, **kwargs)
        except UnicodeDecodeError as exc:
            error = exc
    if error is not None:
        raise error
    raise ValueError(f"无法读取文本数据: {path}")


def read_csv(path: str | Path, encoding: str | None = None, **kwargs: Any) -> Any:
    """Read a CSV/TSV file into a DataFrame.

    UTF-8 的 BOM 会被自动剥离；未指定 ``encoding`` 时在解码失败后退回 ``gbk``，
    以兼容 Excel 导出的中文 CSV。其余关键字参数转发给 :func:`pandas.read_csv`。
    """
    require_deps("pandas")
    return _read_text_data(pd.read_csv, path, encoding, kwargs)


def read_json(path: str | Path, encoding: str | None = None, **kwargs: Any) -> Any:
    """Read a JSON file into a DataFrame.

    编码处理同 :func:`read_csv`；其余参数转发给 :func:`pandas.read_json`。
    """
    require_deps("pandas")
    return _read_text_data(pd.read_json, path, encoding, kwargs)


def read_excel(
    path: str | Path,
    sheet_name: str | int | list[str] | list[int] | None = 0,
    **kwargs: Any,
) -> Any:
    """Read an Excel workbook sheet into a DataFrame.

    Extra keyword arguments are forwarded to :func:`pandas.read_excel`.
    """
    require_deps("pandas")
    try:
        import openpyxl  # noqa: F401
    except ImportError:  # pragma: no cover
        raise ImportError(
            "读取 Excel 需要 openpyxl, 请安装可选依赖: pip install wei-data-shu[analysis] (或 wei-data-shu[excel])"
        ) from None
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)


def read_any(path: str | Path, **kwargs: Any) -> Any:
    """Read a data file into a DataFrame by dispatching on its extension.

    Supported: CSV/TSV/TXT, JSON, Excel (xlsx/xls/xlsm).
    """
    suffix = Path(path).suffix.lower()
    if suffix in _CSV_ALIASES:
        sep = kwargs.pop("sep", "\t" if suffix == ".tsv" else ",")
        return read_csv(path, sep=sep, **kwargs)
    if suffix == ".json":
        return read_json(path, **kwargs)
    if suffix in _EXCEL_ALIASES:
        return read_excel(path, **kwargs)
    raise ValueError(f"不支持的文件类型: {suffix!r}. 支持的扩展名: {sorted(_CSV_ALIASES | _EXCEL_ALIASES | {'.json'})}")


__all__ = ["read_csv", "read_json", "read_excel", "read_any"]
