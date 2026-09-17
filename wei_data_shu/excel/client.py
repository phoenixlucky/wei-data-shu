"""Excel desktop client integration."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, List, Optional, Sequence, Union

from ..text.core import StringBaba
from ._helpers import _require_xlwings
from .manager import ExcelManager

_MACRO_SECURITY_LEVELS = {
    "enable": 1,  # msoAutomationSecurityLow
    "default": 2,  # msoAutomationSecurityByUI
    "disable": 3,  # msoAutomationSecurityForceDisable
}


def _set_macro_security(app: Any, macro_security: Optional[str]) -> None:
    if macro_security is None:
        return
    if macro_security not in _MACRO_SECURITY_LEVELS:
        choices = ", ".join(_MACRO_SECURITY_LEVELS)
        raise ValueError(f"macro_security 必须是 {choices} 之一")
    app.api.AutomationSecurity = _MACRO_SECURITY_LEVELS[macro_security]


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
    def open_save_Excel(self, macro_security: Optional[str] = None) -> Iterator[Any]:
        app = None
        wb = None
        try:
            xw = _require_xlwings()
            app = xw.App(visible=False)
            _set_macro_security(app, macro_security)
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

    @contextmanager
    def open_with_macros_enabled(self) -> Iterator[Any]:
        """Open the workbook with macros enabled for this Excel session."""

        with self.open_save_Excel(macro_security="enable") as wb:
            yield wb

    @contextmanager
    def open_with_macros_disabled(self) -> Iterator[Any]:
        """Open the workbook with macros forcibly disabled for this session."""

        with self.open_save_Excel(macro_security="disable") as wb:
            yield wb

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

    def run_macro(
        self,
        macro_name: str,
        args: Optional[Sequence[Any]] = None,
        save: bool = True,
        macro_security: str = "enable",
    ) -> Any:
        """Run a VBA macro through the local Excel application.

        ``macro_name`` may be a workbook-qualified name such as
        ``Module1.RefreshReport`` or ``'Report.xlsm'!Module1.RefreshReport``.
        The workbook is saved to ``savefile`` by default.
        """

        if not isinstance(macro_name, str) or not macro_name.strip():
            raise ValueError("macro_name 必须是非空字符串")

        app = None
        wb = None
        try:
            xw = _require_xlwings()
            app = xw.App(visible=False)
            _set_macro_security(app, macro_security)
            wb = app.books.open(self.openfile)
            result = wb.macro(macro_name)(*(list(args) if args is not None else []))
            if save:
                wb.save(self.savefile)
            return result
        except Exception as exc:
            raise RuntimeError(f"执行 Excel 宏 '{macro_name}' 失败: {exc}") from exc
        finally:
            if wb is not None:
                try:
                    wb.close()
                except Exception:
                    pass
            if app is not None:
                try:
                    app.quit()
                except Exception:
                    pass


__all__ = ["OpenExcel"]
