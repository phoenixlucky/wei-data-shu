"""Convenience Excel helpers."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Union

from .manager import ExcelManager

if TYPE_CHECKING:
    import pandas as pd


def quick_excel(
    file_path: Union[str, Path],
    data: Optional[Sequence[Sequence]] = None,
    sheet_name: str = "sheet1",
    start_row: int = 1,
    start_col: int = 1,
) -> ExcelManager:
    manager = ExcelManager.create(file_path, sheet_name)
    if data is not None and len(data) > 0:
        manager.fast_write(sheet_name, data, start_row, start_col)
        manager.save()
    return manager


def read_excel_quick(
    file_path: Union[str, Path],
    sheet_name: str = "sheet1",
    as_dataframe: bool = False,
) -> Union[List[List[Any]], pd.DataFrame]:
    with ExcelManager(file_path) as manager:
        if as_dataframe:
            return manager.read_dataframe(sheet_name)
        return manager.read_sheet(sheet_name)


__all__ = ["quick_excel", "read_excel_quick"]
