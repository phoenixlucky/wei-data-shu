"""File management implementation."""

from __future__ import annotations

import re
import shutil
from pathlib import Path


class FileManagement:
    def add_prefix(self, filename: str, file_type: str) -> str:
        pattern = r"[\u4e00-\u9fa5]+"
        matches = re.findall(pattern, filename)
        name = matches[0] if matches else Path(filename).stem
        return f"{name}.{file_type}"

    def copy_files(
        self,
        src_dir: str | Path,
        dest_dir: str | Path,
        target_files: list[str],
        rename: bool = False,
        file_type: str = "xls",
    ) -> None:
        src_path = Path(src_dir)
        dest_path = Path(dest_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        for target_file in target_files:
            source_path = src_path / target_file
            destination_file = self.add_prefix(target_file, file_type) if rename else target_file
            destination_path = dest_path / destination_file
            if source_path.exists():
                shutil.copy2(str(source_path), str(destination_path))
                print(f"File {target_file} copied from {source_path} to {destination_path}")
            else:
                print(f"Source file {target_file} not found in the latest folder.")

    def find_latest_folder(self, base_dir: str | Path) -> Path | None:
        base = Path(base_dir)
        if not base.exists():
            return None
        folders = [item for item in base.iterdir() if item.is_dir()]
        if not folders:
            return None
        return max(folders, key=lambda path: path.stat().st_ctime)

    def copy_file_simple(self, source_path: str | Path, destination_path: str | Path) -> None:
        src = Path(source_path)
        dst = Path(destination_path)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))

    def create_new_folder(self, folder_name: str | Path) -> None:
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        print(f"文件夹 '{folder_name}' 创建成功")

    def delete_folder_or_file(self, path: str | Path) -> None:
        target = Path(path)
        try:
            if target.is_file():
                target.unlink()
                print(f"文件 '{path}' 已删除。")
            elif target.is_dir():
                shutil.rmtree(str(target))
                print(f"文件夹 '{path}' 及其内容已删除。")
            else:
                print(f"路径 '{path}' 不存在。")
        except Exception as exc:
            print(f"删除 '{path}' 时出错: {exc}")


__all__ = ["FileManagement"]
