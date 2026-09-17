<div align="center">

# wei-data-shu 🧩

**把办公和数据里的重复手工活，写成一行 Python 代码**

读 Excel、写 Word / PPT、连 MySQL、发日报邮件、统计词频、画图、预测趋势、跟本地大模型对话 —— 九个常用领域打包成一个库，用到哪个才加载哪个，装完就能跑。

**English:** A domain-oriented toolkit for everyday office automation and data work — Excel, Word / PowerPoint, MySQL, email, file handling, text analytics, charts, trend forecasting and local LLM chat. Nine domain packages, lazily imported, no startup overhead.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/wei-data-shu?color=blue&cacheSeconds=3600)](https://pypi.org/project/wei-data-shu/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)
[![Development Status](https://img.shields.io/badge/status-beta-yellow)](https://pypi.org/project/wei-data-shu/)
[![GitHub stars](https://img.shields.io/github/stars/phoenixlucky/wei-data-shu?logo=github)](https://github.com/phoenixlucky/wei-data-shu)

</div>

---

## 这库是给谁用的

- **天天和表格打交道的人** — 批量读 Excel、拆分合并工作簿、把数据一键变成 Word / PPT 汇报材料
- **要清洗和可视化数据的人** — 读 CSV / Excel，处理缺失值和异常值，画折线图、热力图，跑趋势预测
- **写自动化脚本的人** — 把「取数 → 出报表 → 发邮件」串成一条流水线
- **想用 AI 又不想上云的人** — 连本机 Ollama 对话，聊天记录还能存下来

你不需要背一堆库名和参数：所有能力都挂在 `wei_data_shu.<领域>` 下，代码里用到哪个域，才加载哪个域。

## ✨ 特性

- **九大领域一个入口** — 数据库（MySQL）、Excel、文档、文件、文本、数据分析、邮件、AI 对话、通用工具，都在 `wei_data_shu` 下面
- **文档格式自由互转** — `md` / `docx` / `pptx` 任意方向互转，`xlsx` 也能整本读进来当数据源；底层共用一套 `Document` 中间模型，所以格式之间可以随意组合
- **一行出文档** — 二维列表或 DataFrame 直接变成 Markdown / Word / PPT 文件
- **启动不为它买单** — 根包只暴露领域名，`import wei_data_shu` 不会顺手把 pandas / matplotlib 拉起来
- **核心包很轻** — 只依赖 `toml` 和 `requests`；Excel、Word、数据库、图表这些重能力各占一个 extras，按需安装
- **Jupyter 里顺手** — 图表返回 `Figure` 直接内联显示，中文字体自动配好，`Document` 渲染成带边框的表格预览

## 📖 目录

- [这库是给谁用的？](#这库是给谁用的)
- [特性](#特性)
- [快速开始](#快速开始)
  - [安装](#安装)
  - [按需安装额外能力](#按需安装额外能力)
  - [第一个例子](#第一个例子)
  - [5 分钟上手](#5-分钟上手)
  - [导入方式](#导入方式)
  - [文档读写与互转](#文档读写与互转)
  - [Excel 宏操作](#excel-宏操作)
  - [命令行工具](#命令行工具)
- [常见场景速查](#常见场景速查)
- [功能概览](#功能概览)
- [项目结构](#项目结构)
  - [设计原则](#设计原则)
- [用法示例](#用法示例)
  - [使用手册（完整分域示例）](docs/USAGE.md)
- [Roadmap 路线图](#roadmap-路线图)
- [发布](#发布)
- [参与贡献](#参与贡献)
- [许可证](#许可证)

---

## 🚀 快速开始

### 安装

```bash
pip install wei-data-shu
```

核心包只依赖 `toml` 和 `requests`。Markdown 读写和 HTML 预览零额外依赖，装完就能用。

### 按需安装额外能力

需要什么装什么，不必为了写一个 Word 把整条数据分析链都拖进来：

| 想做的事 | 安装命令 | 会一并装上 |
| --- | --- | --- |
| 读写 Excel、拆分合并工作簿、与 DataFrame 互转 | `pip install "wei-data-shu[excel]"` | pandas, openpyxl |
| 读写 Word / PowerPoint、文档互转、读 `.xlsx` | `pip install "wei-data-shu[docs]"` | python-docx, python-pptx, openpyxl |
| 用本机 Excel 程序打开工作簿、启停宏、运行宏 | `pip install "wei-data-shu[excel-client]"` | xlwings（还需本机装 Microsoft Excel） |
| 连接 MySQL | `pip install "wei-data-shu[database]"` | mysql-connector-python |
| 词频、词云、趋势预测、数据清洗、画图 | `pip install "wei-data-shu[analysis]"` | jieba, numpy, matplotlib, statsmodels, wordcloud, pandas, openpyxl |

邮件、文件管理、AI 对话、颜色 / 密码 / 日期这些工具都在核心包里（只用标准库和 `requests`），不用装 extras。

升级到最新版本：

```bash
pip install --upgrade wei-data-shu
```

### 第一个例子

这段不需要任何 extras，装完核心包就能跑：

```python
from wei_data_shu.docs import to_markdown
from wei_data_shu.text import DateFormat
from wei_data_shu.utils import generate_password, search_colors

print(DateFormat(interval_day=0).get_timeparameter(Format="%Y-%m-%d"))  # 今天
print(DateFormat(interval_day=1).get_timeparameter())                   # 昨天，默认 %Y%m%d
print(generate_password(13))                                            # 13 位安全密码

mint = search_colors("薄荷")[0]                                         # 按中文名找颜色
print(mint["hex"], mint["name"], mint["name_zh"])

print(to_markdown([["渠道", "销售额"], ["电商", 12580]], title="月报"))
```

输出类似（日期取决于运行当天，密码每次都不一样）：

```text
2026-09-16
20260915
8rY#FvQ7mK2$T
#5BC49F mint green 薄荷绿
# 月报

| 渠道 | 销售额 |
| --- | --- |
| 电商 | 12580 |
```

`to_markdown` 不给路径就返回文本，给了路径写文件并返回 `Path`。要在 Jupyter 里看更漂亮的预览，把 `Document` 放在单元格最后一行即可。

### 5 分钟上手

下面这段是真能干活的例子，需要先装 **`wei-data-shu[excel]`**（用到 `ExcelManager`）：

```python
from pathlib import Path

from wei_data_shu.excel import ExcelManager
from wei_data_shu.text import DateFormat
from wei_data_shu.utils import generate_password, search_colors

# 1. 生成当天日期字符串
today = DateFormat(interval_day=0, timeclass="date").get_timeparameter(Format="%Y-%m-%d")
report_path = Path(f"demo-report-{today}.xlsx")

# 2. 写一张日报表，再读回来看一眼
rows = [
    ["日期", "渠道", "销售额"],
    [today, "电商", 12580],
    [today, "门店", 9680],
    [today, "分销", 7320],
]

with ExcelManager(str(report_path)) as wb:
    wb.write_sheet("日报", rows, start_row=1, start_col=1)
    summary = wb.read_sheet("日报", 1, 1)

# 3. 找颜色、生成临时密码
mint_colors = search_colors("薄荷")
temp_password = generate_password(13)

print("报表文件：", report_path.resolve())
print("首行数据：", summary[0])
print("颜色搜索：", mint_colors[0]["hex"], mint_colors[0]["name"], mint_colors[0]["name_zh"])
print("临时密码：", temp_password)
```

运行后会得到一个 `demo-report-YYYY-MM-DD.xlsx`，终端输出类似：

```text
报表文件： D:\path\to\demo-report-2026-09-16.xlsx
首行数据： ['日期', '渠道', '销售额']
颜色搜索： #5BC49F mint green 薄荷绿
临时密码： 8rY#FvQ7mK2$T
```

### 导入方式

所有公开 API 都从 `wei_data_shu.<领域>` 导入，根包只暴露领域包入口：

```python
from wei_data_shu.database import MySQLDatabase, MySQLDatabaseError
from wei_data_shu.excel import ExcelManager, OpenExcel, ExcelOperation, quick_excel
from wei_data_shu.docs import Document, to_markdown, to_word, to_ppt, convert
from wei_data_shu.files import FileManagement
from wei_data_shu.mail import DailyEmailReport
from wei_data_shu.text import DateFormat, StringBaba, TextAnalysis, TrendPredictor
from wei_data_shu.analysis import DataCleaner, read_csv, plot_line, plot_corr_heatmap
from wei_data_shu.ai import ChatBot
from wei_data_shu.utils import fn_timer, generate_password, search_colors, in_notebook
```

### 文档读写与互转

`docs` 域里所有格式共用一套 `Document` 中间模型：`md` / `docx` / `pptx` 可读可写，
`xlsx` 只作读取来源（每个工作表渲染成一页）。所以任意两方互转都自动成立：

```python
from wei_data_shu.docs import Document, convert, to_markdown, to_ppt, to_word

rows = [["渠道", "销售额"], ["电商", 12580], ["门店", 9680]]

# 一行式：二维数据 / DataFrame -> Markdown、Word、PPT
to_markdown(rows, "report.md", title="月度报告")   # 零额外依赖
to_word(rows, "report.docx", title="月度报告")     # 需要 wei-data-shu[docs]
to_ppt(rows, "report.pptx", title="月度报告")      # 需要 wei-data-shu[docs]

# 想要更复杂的文档，就用链式构造
Document(title="月度报告").add_heading("月度报告", 1).add_table(rows).add_bullets(
    ["电商同比 +12%", "门店同比 +3%"]
).save("report.md")

# 跨格式互转：md / docx / pptx 任意方向（按扩展名自动分派）
convert("report.md", "report.docx")
convert("report.docx", "outline.pptx")

# Excel 工作簿当来源：整本读入（一个工作表一页）
convert("sales.xlsx", "sales.md")
```

> 在 Jupyter 中把 `Document` 作为单元格最后一个表达式，会渲染带边框的 HTML 表格预览
> （`_repr_html_`）；也可以显式调用 `document.to_html()` / `document.to_markdown()`。

> 缺少可选依赖时会抛出带安装命令的 `ImportError`，例如 `pip install wei-data-shu[docs]`。

### Excel 宏操作

`.xlsm` 和 `.xltm` 文件通过 `ExcelManager` 读写时会自动保留 VBA 内容。运行宏或控制宏安全级别需要 Windows 本机安装 Microsoft Excel，并安装 `excel-client` 可选依赖：

```bash
pip install "wei-data-shu[excel-client]"
```

```python
from wei_data_shu.excel import OpenExcel

# 启用宏打开，执行操作后自动保存
with OpenExcel("report.xlsm").open_with_macros_enabled() as workbook:
    workbook.api.RefreshAll()

# 禁用宏打开不受信任的工作簿
with OpenExcel("untrusted.xlsm").open_with_macros_disabled() as workbook:
    print(workbook.name)

# 调用指定 VBA 宏，可传递参数并保存到新文件
result = OpenExcel("report.xlsm", "report-result.xlsm").run_macro(
    "Module1.RefreshReport",
    args=["2026-09"],
)
```

也可以直接使用 `open_save_Excel(macro_security="enable|disable|default")` 控制当前 Excel 会话的宏安全级别。该设置不会修改 Excel 的全局安全配置。

### 命令行工具

安装后可以直接在终端用：

```bash
# 查看帮助
wei-data-shu --help
# 或者
python -m wei_data_shu --help
```

```bash
# 颜色检索
wei-data-shu colors                # 列出所有颜色
wei-data-shu colors mint           # 按英文名搜索
wei-data-shu colors 薄荷           # 按中文名搜索
wei-data-shu colors "#5BC49F"      # 按 HEX 搜索

# 密码生成
wei-data-shu password --count 10 --length 13

# 日期计算（默认今天，可往前推 N 天）
wei-data-shu date                    # 2026-09-16
wei-data-shu date --days 1 --format "%Y%m%d"

# Excel 工作簿信息（需要 excel extras）
wei-data-shu excel info report.xlsx  # 列出各工作表行数

# 文档互转与预览
wei-data-shu convert report.md -o report.docx   # md -> docx / pptx
wei-data-shu md report.docx                     # 把文档打印成 Markdown
wei-data-shu md2html report.md -o report.html    # 渲染成 HTML 页面（--fragment 只要片段）

# 文件与文本小工具（核心包，无需 extras）
wei-data-shu files latest "D:\downloads"        # 找创建时间最新的子文件夹
wei-data-shu text clean notes.txt               # 去重 + 重新编号
wei-data-shu text clean notes.txt --mode sql    # 转成 SQL IN 列表
wei-data-shu table report.md                    # Markdown 表格 -> CSV

# 数据分析（需要 analysis extras）
wei-data-shu data info sales.csv                # 行列数 / 缺失值 / 前 5 行
wei-data-shu plot sales.csv -k line -x 月份 -y 销量 -o line.png

# 邮件与数据库（密码建议放环境变量，别写进 shell 历史）
wei-data-shu mail send --host smtp.qq.com --user me@qq.com \
  --to boss@corp.com --subject "日报" --body-file report.html --html
wei-data-shu db query --user root --database shop --sql "SELECT * FROM users LIMIT 5"
```

---

## 🔍 常见场景速查

不知道用哪个域时，先在这里找：

| 我想做的事 | 用这个 | 需要安装 |
| --- | --- | --- |
| 算今天 / 前 N 天的日期 | `DateFormat(interval_day=1).get_timeparameter()` | 核心包 |
| 生成不易看错的密码 | `generate_password(13)` | 核心包 |
| 按中英文名或 HEX 找颜色 | `search_colors("薄荷")` | 核心包 |
| 给函数测耗时 | `fn_timer` | 核心包 |
| 数据变成 Markdown | `to_markdown(rows, "a.md")` | 核心包 |
| 数据变成 Word / PPT | `to_word(rows, "a.docx")` / `to_ppt(rows, "a.pptx")` | `[docs]` |
| 文档之间互转 | `convert("a.md", "a.docx")` | 目标格式对应 extras |
| 读任意文档看内容 | `read_doc("a.docx").to_markdown()` | 同上 |
| 读写 Excel、跑 DataFrame | `ExcelManager` / `quick_excel` | `[excel]` |
| 拆分 / 合并工作簿、转 CSV | `ExcelOperation` | `[excel]` |
| 用本机 Excel 刷新公式、跑宏 | `OpenExcel` | `[excel-client]` |
| 找最新文件夹、批量复制重命名 | `FileManagement` | 核心包 |
| 发纯文本 / HTML 邮件、带附件 | `DailyEmailReport` | 核心包 |
| 连 MySQL 增删改查、调用存储过程 | `MySQLDatabase` | `[database]` |
| 词频统计、画词云 | `TextAnalysis` | `[analysis]` |
| 预测趋势（单列 / 多列） | `TrendPredictor` / `MultipleTrendPredictor` | `[analysis]` |
| 读 CSV / JSON / Excel，清洗数据 | `read_any` / `DataCleaner` | `[analysis]` |
| 画折线、柱状、热力图等 | `plot_line` / `plot_bar` / `plot_corr_heatmap` … | `[analysis]` |
| 跟本地 Ollama 模型对话 | `ChatBot` | 核心包 + 本机 Ollama |

---

## 🧭 功能概览

| 领域 | 导入路径 | 主要 API | 能做什么 |
| --- | --- | --- | --- |
| 数据库 | `wei_data_shu.database` | `MySQLDatabase`, `MySQLDatabaseError` | MySQL 连接、查询、插入、更新、删除、存储过程 |
| Excel | `wei_data_shu.excel` | `ExcelManager`, `ExcelHandler`, `OpenExcel`, `ExcelOperation`, `quick_excel`, `read_excel_quick`, `create_workbook` | 读写工作簿、样式、DataFrame、工作表管理、拆分合并、宏启用/禁用与调用 |
| 文档 | `wei_data_shu.docs` | `Document`, `build`, `to_markdown`, `to_word`, `to_ppt`, `to_docx`, `to_pptx`, `read_doc`, `convert`, `read_markdown`, `write_markdown`, `parse_markdown`, `render_markdown`, `df_to_markdown`, `markdown_to_df`, `render_table`, `render_html`, `read_docx`, `write_docx`, `read_pptx`, `write_pptx`, `read_xlsx` | Markdown / HTML 预览（均零依赖）、Word / PowerPoint 读写、`xlsx` 读取、md·docx·pptx 任意互转、表格与 DataFrame 互转 |
| 文件 | `wei_data_shu.files` | `FileManagement` | 查找最新文件夹、复制文件、批量重命名、删除 |
| 邮件 | `wei_data_shu.mail` | `DailyEmailReport`, `MailError` | SMTP/SSL 发送纯文本/HTML 邮件、附件 |
| 文本 | `wei_data_shu.text` | `DateFormat`, `StringBaba`, `decrypt`, `eFormat`, `TextAnalysis`, `TrendPredictor`, `MultipleTrendPredictor`, `textCombing` | 日期格式化、字符串清洗、词频分析、词云、ARIMA 趋势预测、段落重组、存储过程参数拼接 |
| 数据分析 | `wei_data_shu.analysis` | `read_csv`, `read_json`, `read_excel`, `read_any`, `DataCleaner`, `plot_line`, `plot_bar`, `plot_hist`, `plot_box`, `plot_scatter`, `plot_pie`, `plot_corr_heatmap`, `setup_chinese_font`, `resolve_font_path` | 通用数据读取、缺失值/重复值/异常值处理、归一化、类别编码、常用图表绘制、相关热力图、中文字体自动配置与字体路径解析 |
| AI | `wei_data_shu.ai` | `ChatBot` | 对接 Ollama API，支持流式/非流式对话、聊天记录持久化 |
| 工具 | `wei_data_shu.utils` | `fn_timer`, `generate_password`, `search_colors`, `color_records`, `mav_colors`, `in_notebook`, `read_text`, `bom_tolerant_encoding` | 函数计时器、安全密码生成、颜色检索、Jupyter 环境探测、BOM 安全的文本读取 |

> `docs` 域里还包含 `ExcelHandler` / `ExcelOperation` / `OpenExcel` / `FileManagement`，用于把 Excel 和文件操作编排成复合工作流。

---

## 🗂 项目结构

```text
wei_data_shu/
├─ wei_data_shu/            # 核心包
│  ├─ __init__.py           # 根包入口，按需惰性加载各个领域包
│  ├─ __main__.py           # python -m 入口
│  ├─ _api.py               # 统一公开 API 注册表
│  ├─ _deps.py              # 共享可选依赖核心（依赖名映射与安装提示）
│  ├─ cli.py                # 命令行接口（14 个子命令，见 docs/USAGE.md 第 1 节）
│  ├─ py.typed              # PEP 561 类型标记（IDE 补全）
│  ├─ ai/                   # AI 能力（ChatBot, Ollama）
│  ├─ analysis/             # 数据分析
│  │  ├─ io.py              #   通用数据读取（CSV/JSON/Excel, read_any）
│  │  ├─ cleaning.py        #   DataCleaner（缺失/重复/异常值, 归一化, 编码）
│  │  ├─ charts.py          #   可视化（折线/柱状/直方/箱线/散点/饼图/热力图）
│  │  └─ _deps.py           #   可选依赖守卫
│  ├─ database/             # 数据库能力（MySQL）
│  ├─ docs/                 # 文档能力
│  │  ├─ model.py           #   中间模型: Document 与各类节点
│  │  ├─ md.py              #   Markdown 读写（零第三方依赖）
│  │  ├─ html.py            #   HTML 片段渲染（零第三方依赖，notebook 预览）
│  │  ├─ word.py            #   Word 读写（python-docx）
│  │  ├─ slides.py          #   PowerPoint 读写（python-pptx）
│  │  ├─ sheet.py           #   Excel 工作簿读取（openpyxl，仅作源格式）
│  │  ├─ conversion.py      #   跨格式互转 convert()
│  │  ├─ quick.py           #   一行式 API: to_markdown / to_word / to_ppt
│  │  ├─ workflow.py        #   文档工作流（Excel + 文件处理组合）
│  │  └─ _deps.py           #   可选依赖守卫
│  ├─ excel/                # Excel 能力
│  │  ├─ manager.py         #   核心: ExcelManager
│  │  ├─ handler.py         #   兼容: ExcelHandler
│  │  ├─ client.py          #   桌面: OpenExcel (xlwings)
│  │  ├─ operations.py      #   高级: ExcelOperation (拆分/合并/CSV)
│  │  ├─ quick.py           #   快捷: quick_excel / read_excel_quick
│  │  ├─ _helpers.py        #   内部: 样式/创建/自动范围
│  │  └─ _deps.py           #   可选依赖守卫
│  ├─ files/                # 文件处理（FileManagement）
│  ├─ mail/                 # 邮件发送（DailyEmailReport）
│  ├─ text/                 # 文本处理
│  │  ├─ core.py            #   DateFormat, StringBaba, decrypt
│  │  ├─ analysis.py        #   TextAnalysis (jieba 分词, 词云)
│  │  ├─ forecast.py        #   TrendPredictor, MultipleTrendPredictor
│  │  ├─ combiner.py        #   textCombing (段落重组)
│  │  └─ _deps.py           #   可选依赖守卫
│  └─ utils/                # 通用工具
│     ├─ timing.py          #   fn_timer
│     ├─ passwords.py       #   generate_password
│     ├─ colors.py          #   mav_colors, search_colors
│     ├─ notebook.py        #   in_notebook（Jupyter 环境探测）
│     └─ textio.py          #   read_text, bom_tolerant_encoding（BOM 安全读取）
├─ tests/                   # 单元测试
├─ examples/                # 可运行示例（quickstart / excel / chatbot / docs_demo）
├─ docs/plans/              # 架构设计文档
├─ pyproject.toml           # 包配置 & 依赖
├─ LICENSE                  # GPL-3.0 许可证
└─ README.md                # 本文件
```

### 设计原则

| 原则 | 说明 |
| --- | --- |
| **惰性导入** | 每个领域包用 `__getattr__` 按需加载，避免启动时把所有依赖都导一遍 |
| **统一入口** | 根包只暴露领域包名称，公开 API 一律走 `wei_data_shu.<领域>.名字` |
| **结构清晰** | 按领域分包，各管各的；`docs` 包既提供文档格式后端，也提供跨领域的复合工作流 |
| **格式中立** | 格式差异都收敛到 `Document` 中间模型：`md` / `docx` / `pptx` 可读可写，`xlsx` 只作源格式；新增一个后端，全部互转立刻可用 |
| **可选依赖** | Word/PPT/Excel 源、数据库、文本分析、Excel App 通过 `[docs]` `[excel]` `[database]` `[analysis]` `[excel-client]` 按需安装，核心包只依赖 `toml` / `requests` |

---

## 💻 用法示例

完整的分域示例（数据库 / Excel / 文档读写与互转 / 邮件 / 日期 / 字符串 / 文本分析 / 趋势预测 / 文件管理 / AI 对话 / 通用工具 / 数据分析）请参阅 **[📖 使用手册](docs/USAGE.md)**。

这里保留一个不依赖任何第三方服务、也不需要 extras 的最小例子：

```python
from wei_data_shu.docs import to_markdown
from wei_data_shu.text import DateFormat
from wei_data_shu.utils import generate_password, search_colors

print(DateFormat(interval_day=1).get_timeparameter())  # 昨天日期
print(generate_password(13))                           # 安全密码
print(search_colors("薄荷")[0])                        # 颜色检索
print(to_markdown([["渠道", "销售额"], ["电商", 12580]], title="月报"))
```

---

## 🗺 Roadmap 路线图

下面这些是已经列入计划、还没实现的功能，欢迎认领或提建议：

| 类别 | 功能 | 说明 | 优先级 |
| --- | --- | --- | --- |
| 数据接入 | SQLite / PostgreSQL 支持 | 数据库层目前仅 MySQL，计划扩展本地零配置的 SQLite 与常用 PostgreSQL | 中 |
| 数据接入 | HTTP/API 数据抓取封装 | 把 `requests` 封装成「拉取 → 解析 → DataFrame」的一站式接口 | 中 |
| 数据接入 | 数据导出封装 | 一键把 DataFrame 导出到 CSV / JSON / Excel（多工作表） | 低 |
| 统计分析 | 描述性统计汇总 | 一键输出均值/分位数/偏度/峰度/缺失比例 | 高 |
| 统计分析 | 相关性分析 API | 独立的 Pearson / Spearman / Kendall 相关系数与显著性 | 高 |
| 统计分析 | 假设检验 | t 检验、卡方检验、ANOVA | 中 |
| 统计分析 | 透视表 / 抽样封装 | pivot table、随机抽样、分层抽样 | 中 |
| 建模 | 回归与分类 | 线性回归、逻辑回归封装 | 中 |
| 建模 | 聚类与降维 | KMeans、PCA | 中 |
| 建模 | 通用模型评估 | 分类/回归指标一键计算与交叉验证 | 低 |
| 交付 | 分析报告自动生成 | Word / PPT / Markdown 导出已在 0.8.0 落地，待补 HTML 模板化报告与统计结论自动嵌入 | 中 |
| 交付 | 图表插入文档 | 把 matplotlib 图写进 Word / PPT / Markdown（`Document.add_image` 已支持本地图片） | 中 |
| 交付 | 图表插入 Excel | 把 matplotlib 图写进 Excel 工作表，打通 analysis 与 excel 两个域 | 中 |
| 工程 | 定时任务调度 | 报表 / 抓取任务的定时执行配置 | 低 |

---

## 🚢 发布

打 `wei-data-shu-<版本>` 格式的 tag（例如 `wei-data-shu-0.10.0`）并推送，CI 会自动构建并发布到 PyPI：

```bash
git tag wei-data-shu-0.10.0
git push origin wei-data-shu-0.10.0
```

> 前提：仓库需配置 `PYPI_TOKEN` secret（见 [release.yml](.github/workflows/release.yml)）。
> 发布前请先在 `pyproject.toml` 与 [CHANGELOG.md](CHANGELOG.md) 中更新版本号与变更记录。

---

## 🤝 参与贡献

**English:** We welcome contributions! If you have any questions, suggestions, or improvements, please feel free to:

- [Submit an Issue](https://github.com/phoenixlucky/wei-data-shu/issues) — Report bugs or request features
- [Submit a Pull Request](https://github.com/phoenixlucky/wei-data-shu/pulls) — Contribute code

**中文:** 我们欢迎并感谢您的贡献！如果您有任何问题、建议或改进，请随时：

- [提交 Issue](https://github.com/phoenixlucky/wei-data-shu/issues) — 报告 bug 或提出功能建议
- [提交 Pull Request](https://github.com/phoenixlucky/wei-data-shu/pulls) — 贡献代码

---

## 📄 许可证

**Copyright © 2026 Ethan Wilkins.**

**English:** This project is free software: you can redistribute it and/or modify it under the terms of the [GNU General Public License v3 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html).

**中文:** 本项目为自由软件，您可以依据 [GNU General Public License v3 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html) 的条款重新分发或修改。

完整的许可证文本请参见项目根目录的 [LICENSE](./LICENSE) 文件。

---

**免责声明 / Disclaimer:**

**English:** This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

**中文:** 本程序按"原样"分发，不附带任何明示或暗示的担保。有关详细信息，请参阅 GNU General Public License。
