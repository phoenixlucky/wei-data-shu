## wei_office_simptool

`wei_office_simptool` 一个用于简化办公工作的工具库，提供了数据库操作、Excel 处理、邮件发送、日期时间戳的格式转换、文件移动等常见功能,实现1到3行代码完成相关处理的快捷操作。

#### 📁项目结构

```text
wei_office_simptool/
├─ wei_office_simptool/     # 核心包
│  ├─ database/             # 数据库领域导出
│  ├─ excel/                # Excel 领域导出
│  ├─ text/                 # 文本领域导出
│  └─ mail/                 # 邮件领域导出
├─ tests/                   # 单元测试
├─ pyproject.toml           # 包配置
└─ README.md
```

结构说明：
- 核心代码统一放在 `wei_office_simptool/` 包下；
- 测试代码放在 `tests/`，避免和发布包混在一起；
- 构建产物（`build/`、`dist/`、`*.egg-info`）不纳入版本控制。

#### 🔁兼容迁移说明（chartsManager 已弃用）

旧路径仍可用（含弃用提示），建议迁移到新路径：

```python
# 旧：from wei_office_simptool.chartsManager import TrendPredictor, MultipleTrendPredictor, TextAnalysis

# 新：
from wei_office_simptool.text.forecast import TrendPredictor, MultipleTrendPredictor
from wei_office_simptool.text.analysis import TextAnalysis
```

#### 🔌安装与升级

使用以下命令安装 `wei_office_simptool`：

```bash
pip install wei_office_simptool
```

安装可选能力（按需安装）：

```bash
# 文本分析/趋势预测（chartsManager、TextAnalysis 等）
pip install "wei_office_simptool[analysis]"

# Excel 客户端能力（OpenExcel 的 Excel App 场景）
pip install "wei_office_simptool[excel-client]"
```

使用以下命令升级 `wei_office_simptool`：

```bash
pip install wei_office_simptool --upgrade
```

#### 🔧功能

<!-- #### 1. Database 类 （可以连接各种数据库） 弃用
用于连接和操作数据库。
```python
from wei_office_simptool import Database

# 示例代码
db = Database(host='your_host', port=3306, user='your_user', password='your_password', db='your_database')
result = db("SELECT * FROM your_table", operation_mode="s")
print(result)
``` -->

#### 1. MySQLDatabase 类
主要用于Mysql数据库的快速连接
```python
from wei_office_simptool import MySQLDatabase
```
##### 📌MySQL 连接配置
```python
mysql_config = {
    'host': 'your_host',
    'port': 3306,
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database'
}
```
##### ✏️创建 MySQLDatabase 对象
```python
db = MySQLDatabase(mysql_config)
```
##### 📥插入数据
```python
insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
insert_params = ("value1", "value2")
db.execute_query(insert_query, insert_params)
```
##### 🔍查询数据
```python
select_query = "SELECT * FROM your_table"
results = db.fetch_query(select_query)
for row in results:
    print(row)
```
##### ⌛更新数据
```python
update_query = "UPDATE your_table SET column1 = %s WHERE column2 = %s"
update_params = ("new_value", "value2")
db.execute_query(update_query, update_params)
```
##### 🔪删除数据
```python
delete_query = "DELETE FROM your_table WHERE column1 = %s"
delete_params = ("new_value",)
db.execute_query(delete_query, delete_params)
```
##### 🚪关闭连接
```python
db.close()
```
##### SQLAI智能聊天机器人
```python
from wei_office_simptool import SQLManager

# 示例代码
cfg = {
    'user': 'root',
    'password': '你的密码',
    'host': '127.0.0.1',
    'database': 'mlcorpus'
}
db = SQLManager.MySQLDatabase(cfg)
db.run_ai_chatbot(chat_history_size=5, system_msg="System: You are a helpful AI assistant.")
```

#### 2. Excel 相关类
提供完整的 Excel 文件创建、读取、写入和操作功能。

```python
from pathlib import Path
from wei_office_simptool import ExcelManager, ExcelHandler, OpenExcel, ExcelOperation, quick_excel
```

#### 2.1 ExcelManager 类（推荐使用）
轻量级 Excel 工作簿管理类，基于 openpyxl，无需安装 Excel 应用。

**特性：**
- 自动创建不存在的文件
- 支持多工作表操作
- 快速读写数据
- 自动应用样式
- DataFrame 支持

```python
from wei_office_simptool import ExcelManager

# 创建或打开文件
wb = ExcelManager("data.xlsx")

# 写入数据（自动应用样式）
wb.write_sheet("Sheet1", [["Name", "Age"], ["Alice", 25]], start_row=1, start_col=1)

# 快速写入（自动计算范围）
wb.fast_write("Sheet1", [["Bob", 30]], start_row=3, start_col=1)

# 读取数据
data = wb.read_sheet("Sheet1", 1, 1)

# 使用上下文管理器（自动保存）
with ExcelManager("data.xlsx") as wb:
    wb.fast_write("Sheet1", [[1, 2], [3, 4]], 1, 1)

# 保存并关闭
wb.save()
wb.close()
```

**DataFrame 支持：**
```python
import pandas as pd
from wei_office_simptool import ExcelManager

df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})

# DataFrame 写入 Excel
with ExcelManager("data.xlsx") as wb:
    wb.write_dataframe("Sheet1", df)

# Excel 读取为 DataFrame
with ExcelManager("data.xlsx") as wb:
    df = wb.read_dataframe("Sheet1")
```

**工作表管理：**
```python
from wei_office_simptool import ExcelManager

wb = ExcelManager("data.xlsx")

# 创建新工作表
wb.create_sheet("NewSheet")

# 获取工作表信息
info = wb.get_sheet_info("Sheet1")
print(info)

# 复制工作表
wb.copy_sheet("Sheet1", "Sheet1_Copy")

# 删除工作表
wb.delete_sheet("OldSheet")
```

#### 2.2 快速创建与读取
一行代码完成常用操作：

```python
from wei_office_simptool import quick_excel, read_excel_quick

# 快速创建并写入数据
wb = quick_excel("data.xlsx", [["Name", "Age"], ["Alice", 25]])

# 快速读取为列表
data = read_excel_quick("data.xlsx")

# 快速读取为 DataFrame
df = read_excel_quick("data.xlsx", as_dataframe=True)
```

#### 2.3 ExcelHandler 类（兼容版）
面向已有文件的读取/写入工具，为兼容性保留。

```python
from wei_office_simptool import ExcelHandler

eh = ExcelHandler("data.xlsx")

# 写入指定范围
eh.excel_write("Sheet1", [[1, 2], [3, 4]], 1, 1, 2, 2)

# 读取指定范围
data = eh.excel_read("Sheet1", 1, 1, 2, 2)

# 另存为
eh.excel_save_as("output.xlsx")

# 关闭
eh.excel_quit()
```

#### 2.4 OpenExcel 类（Excel 应用操作）
通过 Excel 应用打开工作簿，适合需要 RefreshAll 的场景。
**注意：需要安装 Microsoft Excel**

```python
from wei_office_simptool import OpenExcel

# 使用上下文管理器自动保存
with OpenExcel("data.xlsx").my_open() as wb:
    wb.fast_write("Sheet1", [[1, 2], [3, 4]], 1, 1)

# 刷新数据连接（需要 Excel 应用）
with OpenExcel("data.xlsx").open_save_Excel() as appwb:
    appwb.api.RefreshAll()

# 列出工作表并按关键词过滤
sheets = OpenExcel("data.xlsx").file_show(filter=["sheet", "报表"])
print(sheets)
```

#### 2.5 ExcelOperation 类（数据处理）
提供数据拆分、合并等高级操作。

```python
from wei_office_simptool import ExcelOperation

# 按工作表拆分为多个文件
op = ExcelOperation("data.xlsx", "output_folder")
files = op.split_table()

# 合并多个文件
op.merge_tables(["file1.xlsx", "file2.xlsx"], "merged.xlsx")

# 转换为 CSV
csv_path = op.convert_to_csv()
```

#### 2.6 完整流水线示例
```python
from pathlib import Path
from wei_office_simptool import ExcelManager, OpenExcel, ExcelOperation

base = Path.cwd()
f = str(base / "pipeline.xlsx")

# 1) 创建并写入数据
with ExcelManager(f) as wb:
    wb.fast_write("Sheet1", [["Name", "Age"], ["Alice", 25], ["Bob", 30]], 1, 1)

# 2) 通过 Excel 应用刷新（需要本机 Excel）
with OpenExcel(f).open_save_Excel() as appwb:
    appwb.api.RefreshAll()

# 3) 拆分工作表到单文件
op = ExcelOperation(f, str(base / "output"))
op.split_table()

# 4) 转换为 CSV
csv_file = op.convert_to_csv()
```

#### 3. eSend 类
用于发送邮件。

```python
from wei_office_simptool import eSend

# 示例代码
email_sender = eSend(sender,receiver,username,password,smtpserver='smtp.126.com')
email_sender.send_email(subject='Your Subject', e_content='Your Email Content', file_paths=['/path/to/file/'], file_names=['attachment.txt'])
```

#### 4. DateFormat 类
用于获取最近的时间处理。

```python
from wei_office_simptool import DateFormat

# 示例代码
#timeclass:1日期 date 2时间戳 timestamp 3时刻 time 4datetime
#获取当日的日期字符串
x=DateFormat(interval_day=0,timeclass='date').get_timeparameter(Format="%Y-%m-%d")
print(x)

# 格式化df的表的列属性
df = DateFormat(interval_day=0,timeclass='date').datetime_standar(df, '日期')
```

#### 5. FileManagement 类
用于文件移动并且重命名。
```python
#latest_folder2 当前目录
#destination_directory 目标目录
#target_files2 文件名
#add_prefix 重命名去除数字
#file_type 文件类型
FileManagement().copy_files(latest_folder2, destination_directory, target_files2, rename=True,file_type="xls")
#寻找最新文件夹
latest_folder = FileManagement().find_latest_folder(base_directory)
```

#### 6. StringBaba 类
用于清洗字符串。
```python
from wei_office_simptool import StringBaba

str="""
萝卜
白菜
"""
formatted_str =StringBaba(str1).format_string_sql()
```

#### 7. TextAnalysis 类
用于进行词频分析。
```python
from wei_office_simptool import TextAnalysis
# 示例用法
data = {
    'Category': ['A', 'A', 'B', 'D', 'C'],
    'Text': [
        '我爱自然语言处理',
        '自然语言处理很有趣',
        '机器学习是一门很有前途的学科',
        '我对机器学习很感兴趣',
        '数据科学包含很多有趣的内容'
    ]
}

df = pd.DataFrame(data)

ta = TextAnalysis(df)
result = ta.get_word_freq(group_col='Category', text_col='Text', agg_func=' '.join)

word_freqs = result['word_freq'].tolist()
titles = result['Category'].tolist()

ta.plot_wordclouds(word_freqs, titles)
```
#### 8. ChatBot类 
0.0.29新增，用于连接Ollama的AI接口

```python
from wei_office_simptool import ChatBot

bot = ChatBot(api_url='http://localhost:11434/api/chat')

print("开始聊天（输入 'exit' 退出，输入 'new' 新建聊天）")
while True:
    user_input = input("你: ")
    if user_input.lower() == 'exit':
        break
    elif user_input.lower() == 'new':
        bot.start_new_chat()
        continue

    # 默认使用流式响应，可以根据需要选择非流式响应
    bot.send_message(user_input, stream=True)

print("聊天结束。")
```

## 9 DailyEmailReport 类
用于发送每日报告邮件，支持HTML和纯文本格式。

```python
from wei_office_simptool import DailyEmailReport

# 初始化 DailyEmailReport 实例
email_reporter = DailyEmailReport(
    email_host='smtp.example.com',
    email_port=465,
    email_username='your_email@example.com',
    email_password='your_password'
)

# 添加收件人
email_reporter.add_receiver('recipient@example.com')

# 发送纯文本邮件
text_content = """
Hello,

Here is your daily report.

[Insert your report content here.]

Regards,
Your Name
"""
email_reporter.send_daily_report("Daily Report", text_content)

# 发送HTML邮件 - 方式1
html_content = """
<html>
  <body>
    <h1>Daily Report</h1>
    <p>Hello,</p>
    <p>Here is your <b>daily report</b>.</p>
    <ul>
      <li>Item 1</li>
      <li>Item 2</li>
    </ul>
    <p>Regards,<br>
    Your Name</p>
  </body>
</html>
"""
email_reporter.send_daily_report("HTML Report", html_content, is_html=True)

# 发送HTML邮件 - 方式2
email_reporter.send_daily_report("HTML Report", html_content=html_content)
```

## Contributing / 参与贡献

**English:** We welcome contributions! If you have any questions, suggestions, or improvements, please feel free to:
- [Submit an Issue](https://github.com/yourusername/wei_office_simptool/issues) - Report bugs or request features
- [Submit a Pull Request](https://github.com/yourusername/wei_office_simptool/pulls) - Contribute code

**中文:** 我们欢迎并感谢您的贡献！如果您有任何问题、建议或改进，请随时：
- [提交 Issue](https://github.com/yourusername/wei_office_simptool/issues) - 报告 bug 或提出功能建议
- [提交 Pull Request](https://github.com/yourusername/wei_office_simptool/pulls) - 贡献代码

---

## License / 许可证

**Copyright © 2026 Ethan Wilkins. All rights reserved.**

**English:** This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

**中文:** 本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT) 开源许可。

```
MIT License

Copyright (c) 2026 Ethan Wilkins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**免责声明 / Disclaimer:**

**English:** This software is provided "as is", without warranty of any kind, express or implied. The authors or copyright holders shall not be liable for any claims, damages, or other liabilities arising from the use of this software.

**中文:** 本软件按"原样"提供，不附带任何明示或暗示的担保。在任何情况下，作者或版权所有者均不对因使用本软件而产生的任何索赔、损害或其他责任承担责任。
