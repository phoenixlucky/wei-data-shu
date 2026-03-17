"""Excel data operations."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

import pandas as pd


class ExcelOperation:
    def __init__(self, input_file: Union[str, Path], output_folder: Union[str, Path]):
        self.input_file = Path(input_file)
        self.output_folder = Path(output_folder)

    def split_table(self, sheet_names: Optional[List[str]] = None) -> List[Path]:
        if not self.input_file.exists():
            raise FileNotFoundError(f"输入文件不存在: {self.input_file}")
        self.output_folder.mkdir(parents=True, exist_ok=True)
        excel_file = pd.ExcelFile(self.input_file)
        sheets_to_process = sheet_names or excel_file.sheet_names
        generated_files = []

        for sheet_name in sheets_to_process:
            if sheet_name not in excel_file.sheet_names:
                print(f"警告: 工作表 '{sheet_name}' 不存在，已跳过")
                continue
            try:
                df = pd.read_excel(self.input_file, sheet_name=sheet_name)
                output_file = self.output_folder / f"{sheet_name}.xlsx"
                df.to_excel(output_file, index=False, engine="openpyxl")
                generated_files.append(output_file)
            except Exception as exc:
                print(f"警告: 拆分工作表 '{sheet_name}' 失败: {exc}")
        return generated_files

    def merge_tables(
        self,
        input_files: List[Union[str, Path]],
        output_file: Union[str, Path],
        sheet_name: str = "Merged",
    ) -> Path:
        all_data = []
        for file_path in input_files:
            path = Path(file_path)
            if not path.exists():
                print(f"警告: 文件不存在: {path}")
                continue
            try:
                all_data.append(pd.read_excel(path))
            except Exception as exc:
                print(f"警告: 读取文件失败 {path}: {exc}")

        if not all_data:
            raise ValueError("没有有效的数据可以合并")

        merged_df = pd.concat(all_data, ignore_index=True)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        merged_df.to_excel(output_path, sheet_name=sheet_name, index=False, engine="openpyxl")
        return output_path

    def convert_to_csv(self, sheet_name: Optional[str] = None, encoding: str = "utf-8-sig") -> Path:
        if not self.input_file.exists():
            raise FileNotFoundError(f"输入文件不存在: {self.input_file}")
        df = pd.read_excel(self.input_file, sheet_name=sheet_name or 0)
        output_file = self.output_folder / f"{self.input_file.stem}.csv"
        self.output_folder.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False, encoding=encoding)
        return output_file


__all__ = ["ExcelOperation"]
