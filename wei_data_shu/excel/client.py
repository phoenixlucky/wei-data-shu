"""Excel desktop client integration."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, List, Optional, Sequence, Union

from ._helpers import _require_xlwings
from .manager import ExcelManager
from ..text.core import StringBaba


class OpenExcel:
    def __init__(self, openfile: Union[str, Path], savefile: Optional[Union[str, Path]] = None):
        self.openfile = Path(openfile)
        self.savefile = Path(savefile) if savefile else self.openfile

    @contextmanager
    def my_open(self) -> Iterator[ExcelManager]:
        manager = None
        try:
            manager = ExcelManager(self.openfile)
            yield manager
            manager.save(self.savefile)
        except Exception as exc:
            raise RuntimeError(f"操作 Excel 文件失败: {exc}") from exc
        finally:
            if manager:
                manager.close()

    @contextmanager
    def open_save_Excel(self) -> Iterator[Any]:
        app = None
        wb = None
        try:
            xw = _require_xlwings()
            app = xw.App(visible=False)
            wb = app.books.open(self.openfile)
        except Exception as exc:
            if app:
                app.quit()
            raise RuntimeError(f"无法打开 Excel 应用: {exc}") from exc

        try:
            yield wb
        finally:
            try:
                wb.api.RefreshAll()
                wb.save(self.savefile)
            except Exception as exc:
                print(f"警告: 刷新或保存失败: {exc}")
            finally:
                if app:
                    app.quit()

    def file_show(self, filter: Optional[Union[str, Sequence[str]]] = None) -> List[str]:
        app = None
        try:
            xw = _require_xlwings()
            app = xw.App(visible=False)
            wb = app.books.open(self.openfile)
            sheet_names = wb.sheet_names
        finally:
            if app:
                app.quit()

        if filter is not None:
            filters = [filter] if isinstance(filter, str) else list(filter)
            sheet_names = StringBaba(sheet_names).filter_string_list(filters)
        return sheet_names


__all__ = ["OpenExcel"]
