# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
████─█──█─████─███─█──█─███─███
█──█─█──█─█──█─█───██─█──█──█──
████─████─█──█─███─█─██──█──███
█────█──█─█──█─█───█──█──█──█──
█────█──█─████─███─█──█─███─███
╔╗╔╗╔╗╔═══╗╔══╗╔╗──╔══╗╔══╗╔══╗╔═══╗╔══╗
║║║║║║║╔══╝╚╗╔╝║║──╚╗╔╝║╔╗║║╔╗║╚═╗─║╚╗╔╝
║║║║║║║╚══╗─║║─║║───║║─║╚╝║║║║║─╔╝╔╝─║║─
║║║║║║║╔══╝─║║─║║───║║─║╔╗║║║║║╔╝╔╝──║║─
║╚╝╚╝║║╚══╗╔╝╚╗║╚═╗╔╝╚╗║║║║║╚╝║║─╚═╗╔╝╚╗
╚═╝╚═╝╚═══╝╚══╝╚══╝╚══╝╚╝╚╝╚══╝╚═══╝╚══╝
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

佛祖保佑       永不宕机     永无BUG

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@project:home
@author:Phoenix,weiliaozi
@file:pywork
@ide:PyCharm
@date:2023/12/3
@time:17:33
@month:十二月
@email:thisluckyboy@126.com
"""
import json
import re

class textCombing:
    def __init__(self,global_var1="重排",global_var2=False):
        self.global_var1 = global_var1
        self.global_var2 = global_var2

    def starts_with_symbol_and_number(self,line):
        line = line.replace("\r", "")
        if self.global_var2:
            line = re.sub(r'\*\*|\u00B9|\u00B2|\u00B3|\u2074|\u2075|\u2076|\u2077|\u2078|\u2079', '', line)
        if self.global_var1 == "原版":
            return (0, line)
        else:
            pattern = r'^(\s|\w|·)?((?<!\d)([0-9]{1,3})((?!\d)|(?![\u4e00-\u9fff]))|(?<![\u4e00-\u9fff])(一|二|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|十六|十七|十七|十八|十九|二十|二十一|二十二|二十三|二十四|二十五|二十六|二十七|二十八|二十九|三十|三十一|三十二|三十三|三十四|三十五|三十六|三十七|三十八|三十九|四十|四十一|四十二|四十三|四十四|四十五|四十六|四十七|四十八|四十九|五十|五十一|五十二|五十三|五十四|五十五|五十六|五十七|五十八|五十九|六十|六十一|六十二|六十三|六十四|六十五|六十六|六十七|六十八|六十九|七十|七十一|七十二|七十三|七十四|七十五|七十六|七十七|七十八|七十九|八十|八十一|八十二|八十三|八十四|八十五|八十六|八十七|八十八|八十九|九十|九十一|九十二|九十三|九十四|九十五|九十六|九十七|九十八|九十九)(?![\u4e00-\u9fff]))(、|,|\.|，|\．|:|：){0,5}'
            match = re.match(pattern, line)
            if match:
                line = re.sub(pattern, r'NUM', line)
                return (match.group(2), line)
            else:
                return (0, line)

    def process_text(self,text):
        processed_text = re.sub(r'\n+', '\n', text)
        processed_text = re.sub(r'^(\d+)(\、|\.|\ 、|\；)?', r'\1、', processed_text, flags=re.MULTILINE)
        processed_text = re.sub(r'^\d+(\、|\.|\ 、)？(\s?)', r'1 \2', processed_text)
        processed_text = re.sub(r'\u200B', '', processed_text)

        adjusted_text = ""
        adjusted_num = 0
        for line in processed_text.splitlines():
            if line.strip() != "":
                if line.strip()[0].isdigit():
                    adjusted_text += "\n"
                    adjusted_num = 0
                else:
                    if adjusted_num == -1 and not line.strip()[0].isdigit():
                        adjusted_text += '1、'
                adjusted_num += len(line)
                adjusted_text += line
                try:
                    # 读取配置文件
                    with open('./character.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if adjusted_text and (
                                not (adjusted_text[-1] in data['separator']) and not (
                                line[0] in data['separator'])):
                            adjusted_text += "，"
                except:
                    pass
                if adjusted_num >= 200:
                    adjusted_num = -1
                    adjusted_text = adjusted_text[:-1] + "。"
                    adjusted_text += "\n"
        adjusted_text = adjusted_text.strip()[:-1] + "。"
        return adjusted_text.strip()

    def remove_leading_spaces(self,text):
        # 将文本按行分割
        lines = text.split('\n')
        # 去除每行开头的空格或空字符
        cleaned_lines = [line.lstrip() for line in lines]
        # 重新组合文本
        cleaned_text = '\n'.join(cleaned_lines)
        return cleaned_text

    def format_text(self,text):
        list_char = []
        lines = [line for line in text.strip().split('\n') if line.strip() != '']
        counter_character = 1
        output_text = ""

        for line in lines:
            patnum, line = self.starts_with_symbol_and_number(line)
            if line in list_char:
                continue
            list_char.append(line)
            if line.startswith('NUM'):
                if self.global_var1 == "不重排" and (patnum == "1" or patnum == 1 or patnum == "一"):
                    counter_character = 1
                output_text += f"{str(counter_character)}、{self.remove_leading_spaces(line.strip()[3:])}\n"
                counter_character += 1
            elif line.startswith('SSS'):
                output_text += f"{self.remove_leading_spaces(line[3:].strip())}\n"
            else:
                output_text += line + '\n'
                # 最后的空行
        return output_text.strip()