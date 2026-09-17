"""Text paragraph combiner."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class textCombing:
    def __init__(
        self,
        global_var1: str = "重排",
        global_var2: bool = False,
        separator_config: str | Path | None = None,
    ) -> None:
        self.global_var1 = global_var1
        self.global_var2 = global_var2
        self._separators = self._load_separators(separator_config)

    def _load_separators(self, separator_config: str | Path | None) -> str:
        """一次性读取标点配置；未提供或读取失败时返回空串（不添加标点）。

        旧实现每行都从当前工作目录打开 ``./character.json``，且异常被静默吞掉，
        既拖慢处理又让缺失的配置文件无从察觉。改为显式参数 + 单次读取。
        """
        if separator_config is None:
            return ""
        try:
            with Path(separator_config).open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError) as exc:
            logger.warning("读取标点配置 %s 失败，将不自动补标点: %s", separator_config, exc)
            return ""
        separators = data.get("separator", "")
        if isinstance(separators, (list, tuple)):
            return "".join(str(item) for item in separators)
        return separators if isinstance(separators, str) else ""

    def starts_with_symbol_and_number(self, line: str) -> tuple[int | str, str]:
        line = line.replace("\r", "")
        if self.global_var2:
            line = re.sub(r"\*\*|\u00B9|\u00B2|\u00B3|\u2074|\u2075|\u2076|\u2077|\u2078|\u2079", "", line)
        if self.global_var1 == "原版":
            return (0, line)
        pattern = r"^(\s|\w|·)?((?<!\d)([0-9]{1,3})((?!\d)|(?![\u4e00-\u9fff]))|(?<![\u4e00-\u9fff])(一|二|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|十六|十七|十七|十八|十九|二十|二十一|二十二|二十三|二十四|二十五|二十六|二十七|二十八|二十九|三十|三十一|三十二|三十三|三十四|三十五|三十六|三十七|三十八|三十九|四十|四十一|四十二|四十三|四十四|四十五|四十六|四十七|四十八|四十九|五十|五十一|五十二|五十三|五十四|五十五|五十六|五十七|五十八|五十九|六十|六十一|六十二|六十三|六十四|六十五|六十六|六十七|六十八|六十九|七十|七十一|七十二|七十三|七十四|七十五|七十六|七十七|七十八|七十九|八十|八十一|八十二|八十三|八十四|八十五|八十六|八十七|八十八|八十九|九十|九十一|九十二|九十三|九十四|九十五|九十六|九十七|九十八|九十九)(?![\u4e00-\u9fff]))(、|,|\.|，|\．|:|：){0,5}"
        match = re.match(pattern, line)
        if match:
            return (match.group(2), re.sub(pattern, "NUM", line))
        return (0, line)

    def process_text(self, text: str) -> str:
        processed_text = re.sub(r"\n+", "\n", text)
        processed_text = re.sub(r"^(\d+)(\、|\.|\ 、|\；)?", r"\1、", processed_text, flags=re.MULTILINE)
        processed_text = re.sub(r"^\d+(\、|\.|\ 、)？(\s?)", r"1 \2", processed_text)
        processed_text = re.sub(r"\u200B", "", processed_text)

        adjusted_text = ""
        adjusted_num = 0
        for line in processed_text.splitlines():
            if line.strip() == "":
                continue
            if line.strip()[0].isdigit():
                adjusted_text += "\n"
                adjusted_num = 0
            else:
                if adjusted_num == -1 and not line.strip()[0].isdigit():
                    adjusted_text += "1、"
            adjusted_num += len(line)
            adjusted_text += line
            if (
                self._separators
                and adjusted_text
                and adjusted_text[-1] not in self._separators
                and line[0] not in self._separators
            ):
                adjusted_text += "，"
            if adjusted_num >= 200:
                adjusted_num = -1
                adjusted_text = adjusted_text[:-1] + "。"
                adjusted_text += "\n"
        adjusted_text = adjusted_text.strip()[:-1] + "。"
        return adjusted_text.strip()

    def remove_leading_spaces(self, text: str) -> str:
        return "\n".join(line.lstrip() for line in text.split("\n"))

    def format_text(self, text: str) -> str:
        list_char: list[str] = []
        lines = [line for line in text.strip().split("\n") if line.strip() != ""]
        counter_character = 1
        output_text = ""

        for line in lines:
            patnum, line = self.starts_with_symbol_and_number(line)
            if line in list_char:
                continue
            list_char.append(line)
            if line.startswith("NUM"):
                if self.global_var1 == "不重排" and (patnum == "1" or patnum == 1 or patnum == "一"):
                    counter_character = 1
                output_text += f"{counter_character}、{self.remove_leading_spaces(line.strip()[3:])}\n"
                counter_character += 1
            elif line.startswith("SSS"):
                output_text += f"{self.remove_leading_spaces(line[3:].strip())}\n"
            else:
                output_text += line + "\n"
        return output_text.strip()


__all__ = ["textCombing"]
