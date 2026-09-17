"""Excel data operations."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional, Union

from ._deps import require_excel_deps

logger = logging.getLogger(__name__)


class ExcelOperation:
    def __init__(self, input_file: Union[str, Path], output_folder: Union[str, Path]):
        self.input_file = Path(input_file)
        self.output_folder = Path(output_folder)

    def split_table(self, sheet_names: Optional[List[str]] = None) -> List[Path]:
        require_excel_deps("pandas", "openpyxl")
        import pandas as pd

        if not self.input_file.exists():
            raise FileNotFoundError(f"输入文件不存在: {self.input_file}")
        self.output_folder.mkdir(parents=True, exist_ok=True)
        generated_files = []

        # 用 with 关闭 ExcelFile：否则文件句柄会一直占用，Windows 上会锁住工作簿。
        with pd.ExcelFile(self.input_file) as excel_file:
            sheets_to_process = sheet_names or excel_file.sheet_names
            for sheet_name in sheets_to_process:
                if sheet_name not in excel_file.sheet_names:
                    logger.warning("工作表 '%s' 不存在，已跳过", sheet_name)
                    continue
                try:
                    df = excel_file.parse(sheet_name)
                    output_file = self.output_folder / f"{sheet_name}.xlsx"
                    df.to_excel(output_file, index=False, engine="openpyxl")
                    generated_files.append(output_file)
                except Exception as exc:
                    logger.warning("拆分工作表 '%s' 失败: %s", sheet_name, exc)
        return generated_files

    def merge_tables(
        self,
        input_files: List[Union[str, Path]],
        output_file: Union[str, Path],
        sheet_name: str = "Merged",
    ) -> Path:
        require_excel_deps("pandas", "openpyxl")
        import pandas as pd

        all_data = []
        for file_path in input_files:
            path = Path(file_path)
            if not path.exists():
                logger.warning("文件不存在: %s", path)
                continue
            try:
                all_data.append(pd.read_excel(path))
            except Exception as exc:
                logger.warning("读取文件失败 %s: %s", path, exc)

        if not all_data:
            raise ValueError("没有有效的数据可以合并")

        merged_df = pd.concat(all_data, ignore_index=True)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        merged_df.to_excel(output_path, sheet_name=sheet_name, index=False, engine="openpyxl")
        return output_path

    def convert_to_csv(self, sheet_name: Optional[str] = None, encoding: str = "utf-8-sig") -> Path:
        require_excel_deps("pandas", "openpyxl")
        import pandas as pd

        if not self.input_file.exists():
            raise FileNotFoundError(f"输入文件不存在: {self.input_file}")
        df = pd.read_excel(self.input_file, sheet_name=sheet_name or 0)
        output_file = self.output_folder / f"{self.input_file.stem}.csv"
        self.output_folder.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False, encoding=encoding)
        return output_file


__all__ = ["ExcelOperation"]
