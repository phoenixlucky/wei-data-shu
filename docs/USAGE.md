# wei-data-shu 使用手册

> 面向办公自动化与数据处理的 Python 一站式工具库。本文档为**分域使用示例**全集，
> 快速入门请见 [README](../README.md) 的「5 分钟上手」。

覆盖领域：**数据库 · Excel · 文档 · 文件 · 文本分析 · 数据分析 · 邮件 · AI 对话 · 通用工具**。

## 安装

```bash
# 核心包（仅依赖 toml 与 requests）
pip install wei-data-shu

# 按需安装能力
pip install "wei-data-shu[excel]"        # Excel 读写 / 拆分合并（pandas, openpyxl）
pip install "wei-data-shu[database]"     # MySQL 数据库（mysql-connector-python）
pip install "wei-data-shu[analysis]"     # 文本/数据分析、趋势预测、图表
pip install "wei-data-shu[excel-client]" # 本机 Excel 应用操作（xlwings）
pip install "wei-data-shu[docs]"         # Word/PPT 读写、xlsx 读取与 md/docx/pptx 互转（python-docx, python-pptx, openpyxl）
```

## 目录

1. [命令行工具](#1-命令行工具)
2. [MySQLDatabase（数据库）](#2-mysqldatabase数据库)
3. [Excel（电子表格）](#3-excel电子表格)
4. [DailyEmailReport（邮件）](#4-dailyemailreport邮件)
5. [DateFormat（日期处理）](#5-dateformat日期处理)
6. [StringBaba（字符串处理）](#6-stringbaba字符串处理)
7. [TextAnalysis（文本分析）](#7-textanalysis文本分析)
8. [TrendPredictor（趋势预测）](#8-trendpredictor趋势预测)
9. [FileManagement（文件管理）](#9-filemanagement文件管理)
10. [ChatBot（AI 对话）](#10-chatbotai-对话)
11. [Utils（通用工具）](#11-utils通用工具)
12. [analysis 数据分析](#12-analysis-数据分析)
13. [docs 文档读写与互转](#13-docs-文档读写与互转)

---

## 1. 命令行工具

安装后可直接使用 `wei-data-shu`，或通过 `python -m wei_data_shu` 调用。

```bash
wei-data-shu --help        # 查看所有子命令
wei-data-shu <命令> --help  # 查看某个子命令的参数
```

### 子命令总览

| 子命令 | 作用 | 依赖 |
| --- | --- | --- |
| `password` | 生成易读安全密码 | 无 |
| `colors` | 查看 / 检索颜色（英文名、中文名、HEX） | 无 |
| `date` | 日期计算（今天 / 回退 N 天） | 无 |
| `excel info` | 查看 Excel 工作簿各工作表行数 | `[excel]` extras |
| `convert` | 文档格式互转（源：md / docx / pptx / xlsx，目标：md / docx / pptx） | 目标格式对应的 extras |
| `md` | 把任意支持的文档打印为 Markdown | 源格式对应的 extras |
| `files latest` | 找创建时间最新的子文件夹 | 无 |
| `md2html` | 把文档渲染为 HTML 页面 / 片段 | 源格式对应的 extras |
| `text clean` | 文本去重、重新编号或转 SQL IN 列表 | 无 |
| `table` | Markdown 表格 ⇄ CSV / TSV | 无 |
| `data info` | 数据文件行列数、每列缺失值与前几行 | `[analysis]` extras |
| `plot` | 折线 / 柱状 / 直方 / 箱线 / 散点 / 饼图 / 相关性热力图 | `[analysis]` extras |
| `mail send` | 发纯文本或 HTML 邮件，可带附件 | 核心包（需 SMTP 凭据） |
| `db query` | 连 MySQL 执行一条 SQL 并打印结果 | `[database]` extras |

> 未安装对应 extras 时，`excel` / `convert` / `md2html` / `data` / `plot` / `db` 子命令会提示安装命令，不影响其他子命令。
> `mail send` 与 `db query` 的密码可用 `--password` 传入，或读环境变量 `WEI_DATA_SHU_MAIL_PASSWORD` / `WEI_DATA_SHU_DB_PASSWORD`（避免写进 shell 历史）。

### 1.1 password — 密码生成

生成不含易混淆字符（`iIl1o0O`）的安全密码。

```
usage: wei-data-shu password [-h] [-l LENGTH] [-c COUNT]

  -l, --length LENGTH  Password length (default 13)
  -c, --count COUNT    Number of passwords to generate (default 1)
```

```bash
wei-data-shu password                      # 生成 1 个 13 位密码
wei-data-shu password --length 16          # 生成 1 个 16 位密码
wei-data-shu password -l 8 -c 5            # 生成 5 个 8 位密码
```

退出码：成功为 `0`；`--count` 小于等于 0 时报错。

### 1.2 colors — 颜色检索

内置 39 种常用颜色，支持英文名、中文名、HEX 检索；不带参数列出全部。

```
usage: wei-data-shu colors [-h] [query]

  query    Search by hex, English name, or Chinese name
```

```bash
wei-data-shu colors                  # 列出全部 39 种颜色
wei-data-shu colors mint              # 按英文名搜索
wei-data-shu colors 薄荷              # 按中文名搜索
wei-data-shu colors "#5BC49F"         # 按 HEX 搜索
```

输出格式（`序号. HEX | 英文名 | 中文名`）：

```text
 3. #5BC49F | mint green | 薄荷绿
 9. #A8E6CF | ice mint | 冰薄荷
```

退出码：找到结果为 `0`；无匹配为 `1`。

### 1.3 date — 日期计算

输出相对今天的日期（默认今天），适合报表文件名、定时任务等场景。

```
usage: wei-data-shu date [-h] [-d DAYS] [-f FORMAT]

  -d, --days DAYS      Days to subtract from today (default 0)
  -f, --format FORMAT  strftime format (default %Y-%m-%d)
```

```bash
wei-data-shu date                          # 2026-08-13（今天）
wei-data-shu date --days 1                 # 昨天：2026-08-12
wei-data-shu date -d 7 --format "%Y%m%d"   # 7 天前：20260806
```

退出码：成功为 `0`。

### 1.4 excel info — 工作簿信息

列出 Excel 工作簿中每个工作表的名字与行数（需要 `[excel]` extras）。

```
usage: wei-data-shu excel info FILE

  FILE    Path to the .xlsx file
```

```bash
wei-data-shu excel info report.xlsx
```

输出格式（`工作表名<TAB>行数 行`）：

```text
sheet1	4 行
销售数据	120 行
```

退出码：成功为 `0`；缺 extras 或文件无法打开为 `1`。

### 1.5 files latest — 找最新文件夹

按创建时间取最新的子文件夹，适合"每天一个日期文件夹"的归档场景。

```bash
wei-data-shu files latest "D:\downloads"     # 打印最新的子文件夹路径
```

退出码：成功为 `0`；目录不存在或没有子目录为 `1`。

### 1.6 md2html — 文档转 HTML

把文档渲染成 HTML：默认输出可直接用浏览器打开的完整页面，`--fragment` 只输出 HTML 片段（嵌入其他页面或 Jupyter 用）。

```bash
wei-data-shu md2html report.md                    # 完整 HTML 输出到 stdout
wei-data-shu md2html report.md -o report.html     # 写入文件
wei-data-shu md2html report.md --fragment         # 只要片段
```

源格式支持 `md` / `docx` / `pptx` / `xlsx` / `xlsm`，按扩展名自动选后端。

### 1.7 text clean — 文本去重与重排

默认去掉重复行并重新编号，常用于把从文档里粘出来的条目整理成干净的列表。

```bash
wei-data-shu text clean notes.txt                 # 重新编号 + 去重
wei-data-shu text clean notes.txt --mode original # 保留原编号，仅整行完全相同才去重
wei-data-shu text clean notes.txt --mode sql      # 转成 "a","b","c" 形式的 SQL IN 列表
```

三种模式的区别：`renumber` 先剥离行首编号再比较，所以「`1、苹果`」和「`3、苹果`」会被判为重复并合并，然后统一重新编号；
`original` 不剥离编号，只有整行文本一字不差时才去重（上面那两行会同时保留）。

`-o` 可把结果写入文件；默认编码 `utf-8`，用 `--encoding` 改。

### 1.8 table — Markdown 表格 ⇄ CSV

按扩展名自动判断方向：`.md` / `.markdown` 转 CSV，`.csv` / `.tsv` 转 Markdown 表格。

```bash
wei-data-shu table report.md            # Markdown 表格 -> CSV
wei-data-shu table data.csv             # CSV -> Markdown 表格
wei-data-shu table report.md -i 1       # 取文档里的第 2 个表格
```

### 1.9 data info — 数据文件速览（需要 `[analysis]`）

行列数、每列非空 / 缺失个数、列类型，以及前若干行预览。

```bash
wei-data-shu data info sales.csv        # 摘要 + 前 5 行
wei-data-shu data info sales.csv -n 0   # 只看摘要
```

支持 `.csv` / `.tsv` / `.txt` / `.json` / `.xlsx`。

### 1.10 plot — 绘图（需要 `[analysis]`）

```bash
wei-data-shu plot sales.csv -k line -x 月份 -y 销量 -o line.png
wei-data-shu plot sales.csv -k bar -x 地区 -o bar.png
wei-data-shu plot sales.csv -k heatmap -o corr.png
```

`-x` 是横轴 / 分组 / 分类列，`-y` 是数值列（逗号分隔可传多列），`-o` 为必填的输出图片路径。
`-k` 可选 `line` / `bar` / `hist` / `box` / `scatter` / `pie` / `heatmap`；`scatter` 需要 `--x` 与 `--y`，`pie` 需要 `--x`。

### 1.11 mail send — 发送邮件

```bash
wei-data-shu mail send --host smtp.qq.com --user me@qq.com \
  --to boss@corp.com --subject "日报" --body "见附件" -a report.xlsx

wei-data-shu mail send --host smtp.qq.com --user me@qq.com \
  --to boss@corp.com --subject "日报" --body-file report.html --html
```

密码建议放环境变量 `WEI_DATA_SHU_MAIL_PASSWORD`；`--dry-run` 只组装并校验（含附件存在性）而不发送。
返回码：发送成功为 `0`；缺密码、缺正文、附件不存在或发送失败为 `1`。

### 1.12 db query — 执行 MySQL 查询

```bash
wei-data-shu db query --user root --database shop --sql "SELECT * FROM users LIMIT 5"
wei-data-shu db query --user root --database shop --sql "SELECT 1" -f json
```

密码建议放环境变量 `WEI_DATA_SHU_DB_PASSWORD`；`-f` 可选 `table`（默认，等宽对齐）/ `csv` / `json`。
查询结果为空时输出 `(0 行)`，查询失败输出错误并以 `1` 退出。

---

## 2. MySQLDatabase（数据库）

### 基本 CRUD

```python
from wei_data_shu.database import MySQLDatabase

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "your_database",
}

db = MySQLDatabase(config)

# 插入
db.execute_query(
    "INSERT INTO users (name, age) VALUES (%s, %s)",
    ("Alice", 25),
)

# 查询
results = db.fetch_query("SELECT * FROM users WHERE age > %s", (20,))
for row in results:
    print(row)

# 更新
db.execute_query(
    "UPDATE users SET age = %s WHERE name = %s",
    (26, "Alice"),
)

# 删除
db.execute_query("DELETE FROM users WHERE name = %s", ("Bob",))

# 批量执行
db.execute_many(
    "INSERT INTO users (name, age) VALUES (%s, %s)",
    [("Cathy", 28), ("David", 32)],
)

# 存储过程（返回结果集列表或 None）
rows = db.call_procedure("get_users_by_age", (25,))

db.close()
```

### 错误处理与上下文管理器

所有数据库操作失败都会抛出 `MySQLDatabaseError`；推荐用 `with` 语句自动关闭连接：

```python
from wei_data_shu.database import MySQLDatabase, MySQLDatabaseError

try:
    with MySQLDatabase(config) as db:
        results = db.fetch_query("SELECT * FROM users WHERE age > %s", (20,))
except MySQLDatabaseError as exc:
    print("数据库操作失败:", exc)
```

> 说明：查询失败会抛异常；查询成功但结果为空时返回 `[]`，可放心区分"无数据"与"出错了"。

---

## 3. Excel（电子表格）

Excel 模块提供 5 个层次的能力：

| 类 | 依赖 | 适用场景 |
| --- | --- | --- |
| `ExcelManager` | pandas + openpyxl | 日常读写、样式、DataFrame、工作表管理 |
| `quick_excel` / `read_excel_quick` | pandas + openpyxl | 极简单次写入 / 读取 |
| `ExcelHandler` | openpyxl | 旧版兼容接口 |
| `ExcelOperation` | pandas + openpyxl | 拆分多工作表、合并多个文件、转 CSV |
| `OpenExcel` | xlwings + Microsoft Excel | 调用本机 Excel 应用（刷新公式、宏等） |

推荐优先使用 **`ExcelManager`**。

### 3.1 ExcelManager — 基本读写

```python
from wei_data_shu.excel import ExcelManager

# 方式一：with 语句（自动保存、关闭）
with ExcelManager("data.xlsx") as wb:
    wb.write_sheet("sheet1", [["Name", "Age"], ["Alice", 25]], start_row=1, start_col=1)
    wb.fast_write("sheet1", [["Bob", 30]], start_row=3, start_col=1)
    data = wb.read_sheet("sheet1", 1, 1)
    print(data)   # [['Name', 'Age'], ['Alice', 25], ['Bob', 30]]

# 方式二：手动管理
wb = ExcelManager("data.xlsx")
wb.fast_write("sheet1", [[1, 2], [3, 4]], 1, 1)
wb.save()
wb.close()
```

### 3.2 ExcelManager — DataFrame 读写

```python
import pandas as pd
from wei_data_shu.excel import ExcelManager

df = pd.DataFrame({"Name": ["Alice", "Bob", "Charlie"], "Age": [25, 30, 28]})

with ExcelManager("team.xlsx") as wb:
    wb.write_dataframe("sheet1", df)

with ExcelManager("team.xlsx") as wb:
    df_read = wb.read_dataframe("sheet1")
    print(df_read)
```

### 3.3 ExcelManager — 工作表管理

```python
from wei_data_shu.excel import ExcelManager

wb = ExcelManager("workbook.xlsx")

# 创建新工作表
wb.create_sheet("销售数据")
wb.create_sheet("旧数据")

# 获取工作表信息
info = wb.get_sheet_info("sheet1")
print(f"行数: {info['max_row']}, 列数: {info['max_column']}")

# 复制工作表
wb.copy_sheet("sheet1", "sheet1_备份")

# 删除工作表
wb.delete_sheet("旧数据")

# 列出所有工作表
print(wb.sheet_names)

wb.save()
wb.close()
```

### 3.4 quick_excel / read_excel_quick（极简模式）

```python
from wei_data_shu.excel import quick_excel, read_excel_quick

# 一行写入
wb = quick_excel("quick.xlsx", [["Name", "Age"], ["Alice", 25], ["Bob", 30]])

# 一行读取（返回列表）
data = read_excel_quick("quick.xlsx")
print(data)

# 读取为 DataFrame
df = read_excel_quick("quick.xlsx", as_dataframe=True)
print(df)
```

### 3.5 ExcelOperation — 拆分、合并、转 CSV

```python
from wei_data_shu.excel import ExcelOperation

op = ExcelOperation("input.xlsx", "./output")

# 将多工作表的工作簿拆分为单个文件（每个工作表一个 .xlsx）
files = op.split_table()
print("拆分文件:", files)

# 合并多个文件为一个工作簿
op.merge_tables(["sales_q1.xlsx", "sales_q2.xlsx"], "sales_上半年.xlsx")

# 转换为 CSV
csv_path = op.convert_to_csv()
print("CSV 文件:", csv_path)
```

### 3.6 OpenExcel — 本机 Excel 应用操作

需要安装 Microsoft Excel 和 `xlwings`：`pip install wei-data-shu[excel-client]`

```python
from wei_data_shu.excel import OpenExcel

# 方式一：读写后自动保存
with OpenExcel("data.xlsx").my_open() as wb:
    wb.fast_write("sheet1", [["Name", "Age"], ["Alice", 25]], 1, 1)

# 方式二：刷新公式（如数据透视表）
with OpenExcel("report.xlsx").open_save_Excel() as appwb:
    appwb.api.RefreshAll()

# 方式三：启用或禁用宏（仅对本次 Excel 会话生效）
with OpenExcel("report.xlsm").open_with_macros_enabled() as appwb:
    appwb.api.RefreshAll()

with OpenExcel("untrusted.xlsm").open_with_macros_disabled() as appwb:
    print(appwb.name)

# 方式四：直接运行宏并保存到目标文件
result = OpenExcel("report.xlsm", "report_result.xlsm").run_macro(
    "Module1.RefreshReport",
    args=["2026-09"],
)

# 方式五：列出工作簿中的工作表
sheets = OpenExcel("data.xlsx").file_show(filter=["sheet", "报表"])
print(sheets)
```

`run_macro()` 需要安装 Microsoft Excel 和 `xlwings`，并默认在本次会话中启用宏。`macro_security="default"` 使用 Excel 当前界面设置，`macro_security="disable"` 强制禁用宏。宏安全级别不会写入系统设置。

### 3.7 完整流水线示例

```python
from pathlib import Path
from wei_data_shu.excel import ExcelManager, OpenExcel, ExcelOperation

base = Path.cwd()
filepath = str(base / "pipeline.xlsx")

# 1. 写入数据
with ExcelManager(filepath) as wb:
    wb.fast_write("sheet1", [["Name", "Age"], ["Alice", 25], ["Bob", 30]], 1, 1)

# 2. 通过 Excel 应用刷新公式
with OpenExcel(filepath).open_save_Excel() as appwb:
    appwb.api.RefreshAll()

# 3. 拆分工作表
op = ExcelOperation(filepath, str(base / "output"))
op.split_table()

# 4. 转 CSV
csv_file = op.convert_to_csv()
```

---

## 4. DailyEmailReport（邮件）

### 发送纯文本邮件

```python
from wei_data_shu.mail import DailyEmailReport

email_reporter = DailyEmailReport(
    email_host="smtp.example.com",
    email_port=465,
    email_username="your_email@example.com",
    email_password="your_password",
)

email_reporter.add_receiver("recipient@example.com")

email_reporter.send_daily_report(
    "日报",
    "Hello,\n\n这是今日报表。\n\nBest Regards",
)
```

### 发送 HTML 邮件

```python
html = """
<html>
  <body>
    <h1>日报</h1>
    <table border="1">
      <tr><th>渠道</th><th>销售额</th></tr>
      <tr><td>电商</td><td>12,580</td></tr>
      <tr><td>门店</td><td>9,680</td></tr>
    </table>
  </body>
</html>
"""
email_reporter.send_daily_report("HTML 日报", html_content=html)
```

### 发送带附件的邮件

```python
email_reporter.set_email_content(
    subject="带附件的报表",
    body="详见附件。",
    file_paths=["./attachments/"],
    file_names=["report.xlsx"],
)
email_reporter.send_email()
```

### 错误处理

发送失败（网络 / 认证 / 无收件人）会抛出 `MailError`：

```python
from wei_data_shu.mail import DailyEmailReport, MailError

reporter = DailyEmailReport("smtp.example.com", 465, "u", "p")

try:
    reporter.add_receiver("recipient@example.com")
    reporter.send_email()
except MailError as exc:
    print("邮件发送失败:", exc)
```

---

## 5. DateFormat（日期处理）

### 生成格式化的日期 / 时间字符串

```python
from wei_data_shu.text import DateFormat

# 今天
today = DateFormat(interval_day=0, timeclass="date").get_timeparameter(Format="%Y-%m-%d")
print(today)  # 2026-03-17

# 昨天
yesterday = DateFormat(interval_day=1, timeclass="date").get_timeparameter(Format="%Y-%m-%d")

# 当前时间（时:分）
now = DateFormat(interval_day=0, timeclass="time").get_timeparameter(Format="%H:%M")
print(now)    # 14:30

# 当前时间戳
ts = DateFormat(interval_day=0, timeclass="timestamp").get_timeparameter()
print(ts)     # time.struct_time(...)

# 当前 datetime 对象
dt = DateFormat(interval_day=0, timeclass="datetime").get_timeparameter()
print(dt)     # datetime.datetime(...)
```

### 标准化 DataFrame 中的日期列

```python
import pandas as pd
from wei_data_shu.text import DateFormat

df = pd.DataFrame({"日期": ["2026-01-01", "2026/01/02", "2026年1月3日"]})
df = DateFormat(interval_day=0, timeclass="date").datetime_standar(df, "日期")
print(df.dtypes)  # datetime64[ns]
```

---

## 6. StringBaba（字符串处理）

### SQL 格式化

将多行文本拼接为 SQL `IN` 子句可用的格式：

```python
from wei_data_shu.text import StringBaba

text = """
苹果
香蕉
橘子
"""
result = StringBaba(text).format_string_sql()
print(result)  # "苹果","香蕉","橘子"
```

### 字符串列表过滤

```python
from wei_data_shu.text import StringBaba

items = ["苹果手机", "香蕉牛奶", "橘子汽水", "笔记本"]
filtered = StringBaba(items).filter_string_list(["手机", "汽水"])
print(filtered)  # ['苹果手机', '橘子汽水']
```

---

## 7. TextAnalysis（文本分析）

需要安装可选依赖：`pip install wei-data-shu[analysis]`

### 词频分析

```python
import pandas as pd
from wei_data_shu.text import TextAnalysis

data = {
    "Category": ["A", "A", "B", "B", "C"],
    "Text": [
        "我爱自然语言处理",
        "自然语言处理很有趣",
        "机器学习是一门很有前途的学科",
        "深度学习改变了人工智能",
        "数据科学包含统计与编程",
    ],
}
df = pd.DataFrame(data)

ta = TextAnalysis(df)
result = ta.get_word_freq(group_col="Category", text_col="Text", agg_func=" ".join)

print(result[["Category", "word_freq"]])
```

### 词云绘制

```python
word_freqs = result["word_freq"].tolist()
titles = result["Category"].tolist()
ta.plot_wordclouds(word_freqs, titles, save_path="wordclouds.png")
```

---

## 8. TrendPredictor（趋势预测）

需要安装可选依赖：`pip install wei-data-shu[analysis]`

### 单序列趋势预测

```python
import pandas as pd
from wei_data_shu.text import TrendPredictor

# 准备数据
dates = pd.date_range(start="2026-01-01", periods=100, freq="D")
values = [100 + i * 0.5 + (i % 7) * 3 for i in range(100)]  # 模拟趋势
df = pd.DataFrame({"日期": dates, "平滑均值": values})

# 创建预测器
predictor = TrendPredictor(
    market_trend_df=df,
    date_col="日期",
    smoothed_avg_col="平滑均值",
    steps=7,           # 预测未来 7 期
    order=(5, 1, 0),   # ARIMA 参数
    freq="D",          # 日频
)

# 查看原始数据（带趋势标签）
print(predictor.original_data())

# 获取预测结果
future_df, forecast, str_forecast, future_dates = predictor.forecast_data()
print(future_df)

# 模型评估
metrics = predictor.cross_validate(test_size=0.2)
print(metrics)

# 模型信息
info = predictor.get_model_info()
print(info)
```

### 多序列趋势预测

```python
from wei_data_shu.text import MultipleTrendPredictor

# 多列数据，每列是一个独立序列
df_multi = pd.DataFrame({
    "电商": [100, 110, 120, 130, 140, 150, 160],
    "门店": [80, 82, 85, 88, 90, 95, 100],
    "分销": [50, 55, 60, 58, 62, 65, 70],
}, index=pd.date_range(start="2026-01-01", periods=7, freq="D"))

predictor = MultipleTrendPredictor(df_multi, steps=3)
predictions = predictor.predict()
print(predictions)
```

---

## 9. FileManagement（文件管理）

### 查找最新文件夹

```python
from wei_data_shu.files import FileManagement

latest = FileManagement().find_latest_folder("./backups")
if latest:
    print(f"最新文件夹: {latest}")
```

### 复制文件

```python
from wei_data_shu.files import FileManagement

fm = FileManagement()

# 复制单个文件
fm.copy_file_simple("./source/report.xlsx", "./dest/report.xlsx")

# 批量复制并重命名（提取文件名中的中文作为新文件名）
fm.copy_files(
    src_dir="./source",
    dest_dir="./dest",
    target_files=["data_2026.xls", "summary_2026.xls"],
    rename=True,
    file_type="xls",
)
```

### 删除文件 / 文件夹

```python
fm.delete_folder_or_file("./temp/old_data.xlsx")
fm.delete_folder_or_file("./temp/archive")  # 递归删除目录
```

### 创建文件夹

```python
fm.create_new_folder("./output/reports/2026")
```

---

## 10. ChatBot（AI 对话）

通过 Ollama API 接入本地大语言模型，支持流式输出和聊天记录持久化。

```python
from wei_data_shu.ai import ChatBot

bot = ChatBot(
    api_url="http://localhost:11434/api/chat",
    model="llama3.2",
    messages_file="messages.toml",       # 初始系统提示
    history_file="chat_history.toml",    # 聊天记录自动保存
)

# 流式对话
print("开始聊天（输入 'exit' 退出，输入 'new' 新建会话）")
while True:
    user_input = input("你: ")
    if user_input.lower() == "exit":
        break
    if user_input.lower() == "new":
        bot.start_new_chat()
        continue
    bot.send_message(user_input, stream=True)
```

参数说明：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `api_url` | — | Ollama API 地址，如 `http://localhost:11434/api/chat` |
| `model` | `llama3.2` | 使用的模型名称 |
| `messages_file` | `messages.toml` | 初始消息配置文件（TOML 格式） |
| `history_file` | `chat_history.toml` | 聊天历史自动保存路径 |
| `stream` | `True` | 是否启用流式输出 |

---

## 11. Utils（通用工具）

### 函数计时器

用装饰器测量函数执行时间：

```python
from wei_data_shu.utils import fn_timer

@fn_timer
def build_report():
    import time
    time.sleep(0.5)
    return "done"

result, elapsed = build_report()
print(f"耗时: {elapsed:.2f} 秒")  # Total time running build_report: 0.50 seconds
```

### 密码生成

生成不含易混淆字符（`iIl1o0O`）的安全密码，适合临时密码/一次性密码：

```python
from wei_data_shu.utils import generate_password

# 默认长度 13
pwd = generate_password()
print(pwd)  # 8rY#FvQ7mK2$T

# 自定义长度
pwd16 = generate_password(16)
print(pwd16)
```

### 颜色检索

内置 39 种常用颜色，支持英文名、中文名、HEX 码检索：

```python
from wei_data_shu.utils import search_colors, mav_colors

# 按英文名搜索
results = search_colors("mint")
print(results[0])
# {'index': 3, 'hex': '#5BC49F', 'name': 'mint green', 'name_zh': '薄荷绿'}

# 按中文名搜索
results = search_colors("薄荷")
print(results[0]["hex"])  # #5BC49F

# 按 HEX 搜索
results = search_colors("#5BC49F")
print(results[0]["name_zh"])  # 薄荷绿

# 查看所有颜色
print(len(mav_colors))   # 39
print(mav_colors[:3])    # ['#60ACFC', '#32D3EB', '#5BC49F']
```

CLI 输出格式：

```text
 3. #5BC49F | mint green | 薄荷绿
```

---

## 12. analysis 数据分析

需要安装可选依赖：`pip install wei-data-shu[analysis]`

### 12.1 通用数据读取

```python
from wei_data_shu.analysis import read_csv, read_json, read_excel, read_any

df_csv = read_csv("sales.csv")                      # CSV / TSV / TXT
df_json = read_json("data.json")                    # JSON 数组 / 对象列表
df_xls = read_excel("sales.xlsx", sheet_name="6月") # Excel 指定工作表
df_any = read_any("data.json")                      # 按扩展名自动分发（csv/json/xlsx）
```

### 12.2 DataCleaner — 链式数据清洗

```python
import pandas as pd
from wei_data_shu.analysis import DataCleaner

df = pd.DataFrame({
    "城市": ["北京", "上海", "北京", "深圳", None],
    "销售额": [100.0, 200.0, None, 300.0, 50.0],
    "成本":   [60.0, 120.0, 90.0, 180.0, 30.0],
})

cleaned = (
    DataCleaner(df)
    .drop_missing(subset=["城市"])            # 删除关键列缺失的行
    .fill_missing(strategy="median")          # 数值列按中位数填充
    .remove_duplicates()                      # 去重
    .clip_outliers(cols=["销售额"])           # 异常值缩尾（IQR 规则）
    .normalize(cols=["销售额", "成本"])       # min-max 归一化到 [0,1]
    .encode_categorical(cols=["城市"], method="onehot")  # 独热编码
    .get()
)

print(cleaned)
```

### 12.3 缺失值统计与异常值检测

```python
cleaner = DataCleaner(df)

# 缺失值统计（缺失数量 / 缺失比例）
summary = cleaner.missing_summary()
print(summary)

# 异常值掩码（IQR / Z-Score 两种规则）
mask = cleaner.detect_outliers(cols=["销售额"], method="iqr")
print(mask)

# 删除异常值行
clean_df = cleaner.remove_outliers(cols=["销售额"]).get()

# 线性插值填充缺失
interp_df = cleaner.interpolate_missing().get()
```

### 12.4 类型推断与转换

```python
cleaner = DataCleaner(df)

# 推断每列类型（"数值" / "日期" / "文本"）
types = cleaner.infer_types()
print(types)

# 手动转换
cleaner.to_datetime(["日期列"]).to_numeric(["金额列"])
```

### 12.5 快速可视化

```python
from wei_data_shu.analysis import (
    plot_line, plot_bar, plot_hist, plot_box,
    plot_scatter, plot_pie, plot_corr_heatmap,
)

plot_line(df, x="日期", y="销售额", save_path="line.png")        # 折线
plot_bar(df, x="城市", y="销售额", save_path="bar.png")          # 柱状
plot_hist(df, col="销售额", bins=30, save_path="hist.png")       # 直方图
plot_box(df, cols=["销售额", "成本"], save_path="box.png")       # 箱线图
plot_scatter(df, x="销售额", y="成本", save_path="scatter.png")  # 散点
plot_pie(df, col="城市", save_path="pie.png")                    # 饼图
plot_corr_heatmap(df, method="pearson", save_path="corr.png")    # 相关热力图
```

所有绘图函数返回 `matplotlib.figure.Figure`，传 `save_path` 保存到文件，传 `show=True` 交互显示。

**中文字体已自动配置**：导入 `wei_data_shu.analysis`（或任意 `plot_*` 函数）时会自动检测并启用系统已安装的中文字体（Windows: Microsoft YaHei / SimHei；macOS: PingFang SC；Linux: Noto Sans CJK 等），中文标签直接可用，无需手动设置。若系统中没有中文字体，则自动降级为默认字体（中文可能显示为方块）。

需要自定义字体时，可手动调用：

```python
from wei_data_shu.analysis import setup_chinese_font

setup_chinese_font()                          # 自动检测
setup_chinese_font(["Noto Sans CJK SC"])      # 指定候选字体
setup_chinese_font(["SimHei"])                # 返回命中的字体名，未找到返回 None
```

---

## 13. docs 文档读写与互转

Markdown 读写与 HTML 片段预览零第三方依赖；Word / PowerPoint / Excel 来源需要
`pip install wei-data-shu[docs]`。所有格式共享一套 `Document` 中间模型：
`md` / `docx` / `pptx` 可读可写，`xlsx` 只作读取来源。

### 13.1 一行式 API

```python
from wei_data_shu.docs import to_markdown, to_word, to_ppt

rows = [["渠道", "销售额"], ["电商", 12580], ["门店", 9680]]

to_markdown(rows, "report.md", title="月度报告")   # 零依赖，返回写入路径
to_word(rows, "report.docx", title="月度报告")     # 需要 [docs]
to_ppt(rows, "report.pptx", title="月度报告")      # 需要 [docs]
```

`data` 支持 DataFrame、二维列表（表格）、`list[str]`（无序列表）、`dict`（键作二级标题）与普通字符串（段落）：

```python
from wei_data_shu.docs import to_ppt

to_ppt(
    {
        "华东": [["渠道", "销售额"], ["电商", 12580]],
        "华南": [["渠道", "销售额"], ["门店", 9680]],
    },
    "report.pptx",
    title="分区域销售",
)
```

### 13.2 Document — 链式构造

```python
from wei_data_shu.docs import Document

document = (
    Document(title="月度报告")
    .add_heading("月度报告", 1)
    .add_paragraph("本月销售额同比增长 12%。")
    .add_heading("分渠道", 2)
    .add_table([["渠道", "销售额"], ["电商", 12580], ["门店", 9680]])
    .add_bullets(["电商同比 +12%", "门店同比 +3%"])
    .add_quote("数据截至本月最后一个自然日。")
    .add_code('print("hello")', language="python")
    .add_image("chart.png", caption="销售趋势")
    .add_page_break()
)

document.save("report.docx")   # 按扩展名自动选择后端：.md / .docx / .pptx
document.to_markdown()         # 渲染为 Markdown 文本
Document.open("report.docx")   # 按扩展名读回
```

节点类型：`Heading` / `Paragraph` / `BulletList` / `Table` / `CodeBlock` / `Image` / `PageBreak`。

### 13.3 跨格式互转

```python
from wei_data_shu.docs import convert, read_xlsx

convert("report.md", "report.docx")     # Markdown -> Word
convert("report.docx", "outline.pptx")  # Word -> PowerPoint
convert("outline.pptx", "outline.md")   # PowerPoint -> Markdown

# Excel 工作簿作为来源：整本读入（一个工作表一页），需要 openpyxl（[docs] extras）
convert("sales.xlsx", "sales.docx")
document = read_xlsx("sales.xlsx")      # 也可直接读成 Document
```

规则说明：

- 源后缀支持 `.md` / `.markdown` / `.docx` / `.pptx` / `.xlsx` / `.xlsm`
- 目标后缀支持 `.md` / `.markdown` / `.docx` / `.pptx`，其他后缀抛 `ValueError`
- `xlsx` 只能作为来源，作为转换目标时抛 `ValueError` 并说明原因
- `overwrite=False` 且目标已存在时抛 `FileExistsError`
- PPT 按「一级 / 二级标题」分页，更深的标题保留在页内正文

Excel 读取规则（`read_xlsx`）：

- 每个**非空**工作表渲染为一个二级标题（工作表名）+ 一个表格，空工作表自动跳过
- 只读公式的缓存值；合并单元格只取左上角的值；全空行跳过、尾部空行裁掉
- 日期去掉零时刻（`2026-09-16`），带时间则保留（`2026-09-16 08:30:00`）；整数值浮点去掉 `.0`（`12580.0` → `12580`）
- 也可通过 `read_doc("sales.xlsx")` 或 `Document.open("sales.xlsx")` 读取

### 13.4 Markdown 与表格互转

```python
from wei_data_shu.docs import (
    df_to_markdown, markdown_to_df, parse_markdown,
    read_markdown, render_markdown, write_markdown,
)

text = df_to_markdown([["渠道", "销售额"], ["电商", 12580]])
# | 渠道 | 销售额 |
# | --- | --- |
# | 电商 | 12580 |

records = markdown_to_df(text, as_records=True)  # [{'渠道': '电商', '销售额': '12580'}]，无需 pandas
df = markdown_to_df(text)                        # 需要 pandas：pip install wei-data-shu[analysis]

document = read_markdown("report.md")            # Markdown 文件 -> Document
parse_markdown("# 标题\n\n正文")                 # Markdown 文本 -> Document
print(render_markdown(document))                 # Document -> Markdown 文本
write_markdown(document, "copy.md")              # 写出 Markdown 文件
```

解析覆盖 GFM 常用子集：标题、段落、有序/无序列表、引用、围栏代码块、表格、独立成行的图片、水平分隔线（解析为 `PageBreak`）；行内样式按原文保留。

### 13.5 命令行

```bash
wei-data-shu convert report.md -o report.docx    # 互转（--no-overwrite 时不覆盖已存在目标）
wei-data-shu convert sales.xlsx -o sales.md      # Excel 工作簿 -> Markdown
wei-data-shu md report.docx                      # 打印为 Markdown
wei-data-shu md sales.xlsx -o sales.md           # 写入文件（xlsx 同样可作来源）
wei-data-shu md2html report.md -o report.html     # 渲染成 HTML 页面（--fragment 只要片段）
wei-data-shu table report.md                     # Markdown 表格 -> CSV（.csv/.tsv 反向转回）
```

### 13.6 Word / PowerPoint 读写

```python
from wei_data_shu.docs import read_docx, read_pptx, write_docx, write_pptx

document = read_docx("input.docx")   # 标题 / 段落 / 列表 / 表格按正文顺序还原
write_docx(document, "output.docx")

deck = read_pptx("input.pptx")       # 每页标题 -> 一级标题，缩进项 -> 列表
write_pptx(deck, "output.pptx")
```

### 13.7 在 Jupyter 中使用

```python
from wei_data_shu.docs import Document, render_html
from wei_data_shu.utils import in_notebook

in_notebook()   # True：运行在 Jupyter / JupyterLab / Colab 内核中

document = Document().add_heading("月度报告", 1).add_table(rows)
document                # notebook 中直接渲染 HTML 预览（表格带边框）
document.to_html()      # 同一渲染器，返回可嵌入网页的 HTML 片段
document.to_markdown()  # 或者要 Markdown 文本
```

`_repr_html_` 与 `_repr_markdown_` 同时存在时，Jupyter 优先使用 `_repr_html_`。HTML 渲染会转义所有文本与属性值，文档中的 `<script>` 等内容不会被当作标签执行；需要嵌入自定义页面时可直接调用 `render_html(document)`。

`wei_data_shu.analysis` 的绘图函数返回 `matplotlib.figure.Figure`，在 notebook 中作为单元格最后一个表达式即自动内联显示，无需调用 `plt.show()`；`show=True` 在 Jupyter 中也不会阻塞。

---

## 常见问题

- **`to_word` / `to_ppt` / `read_docx` / `read_pptx` / `read_xlsx` 报缺少依赖**：执行 `pip install "wei-data-shu[docs]"`
- **`import wei_data_shu.excel` 报错**：未安装 excel extras，执行 `pip install "wei-data-shu[excel]"`
- **`import wei_data_shu.database` 报错**：未安装 database extras，执行 `pip install "wei-data-shu[database]"`
- **`TextAnalysis` / `TrendPredictor` 报缺少依赖**：执行 `pip install "wei-data-shu[analysis]"`
- **图表中文显示为方块**：说明系统中没有可用的中文字体，请安装中文字体（Windows 自带微软雅黑/黑体；Linux 可装 `fonts-noto-cjk`）后调用 `setup_chinese_font()`，或手动指定字体
- **数据库操作失败没有报错**：0.7.0 起失败统一抛 `MySQLDatabaseError`，请捕获该异常而非依赖打印
