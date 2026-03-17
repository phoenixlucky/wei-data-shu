"""Compatibility workbook handler."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Sequence, Union

from openpyxl.worksheet.worksheet import Worksheet

from ._helpers import _auto_range
from .manager import ExcelManager


class ExcelHandler:
    def __init__(self, file_name: Union[str, Path]):
        self._manager = ExcelManager(file_name)

    def _ensure_sheet(self, sheet_name: str) -> Worksheet:
        return self._manager._ensure_sheet(sheet_name)

    def excel_write(
        self,
        sheet_name: str,
        results: Sequence[Sequence],
        start_row: int,
        start_col: int,
        end_row: int,
        end_col: int,
    ) -> None:
        self._manager.write_sheet(
            sheet_name,
            results,
            start_row,
            start_col,
            end_row,
            end_col,
            apply_styles=False,
        )

    def excel_read(
        self,
        sheet_name: str,
        start_row: int,
        start_col: int,
        end_row: int,
        end_col: int,
    ) -> List[List[Any]]:
        return self._manager.read_sheet(sheet_name, start_row, start_col, end_row, end_col)

    def excel_save_as(self, file_name2: Optional[Union[str, Path]] = None) -> None:
        self._manager.save(file_name2)

    def excel_quit(self) -> None:
        self._manager.close()

    @staticmethod
    def fast_write(
        sheet_name: str,
        results: Sequence[Sequence],
        start_row: int,
        start_col: int,
        end_row: int = 0,
        end_col: int = 0,
        re: int = 0,
        xl_book: Optional["ExcelHandler"] = None,
    ) -> None:
        if xl_book is None:
            raise ValueError("必须提供 xl_book 参数")
        actual_end_row, actual_end_col = _auto_range(
            start_row, start_col, results, re, end_row, end_col
        )
        xl_book.excel_write(sheet_name, results, start_row, start_col, actual_end_row, actual_end_col)


__all__ = ["ExcelHandler"]
