# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and the project follows Semantic Versioning in a pragmatic way:

- minor releases may include breaking changes before `1.0.0`
- patch releases are reserved for backwards-compatible fixes and documentation-only corrections

## [Unreleased]

## [0.10.0] - 2026-09-17

### Added

- `wei_data_shu.analysis.resolve_font_path()`：返回可用的中文字体文件路径，供词云等场景使用
- `textCombing(separator_config=...)`：显式指定标点配置文件，替代原先隐式的 `./character.json`
- 共享可选依赖核心 `wei_data_shu._deps`：统一「依赖名 → 模块名」映射与安装提示，供各领域复用
- `pyproject.toml` 新增 `dev` extra 与 `[tool.ruff]` / `[tool.mypy]` 配置
- CI 新增 lint（`ruff check` / `ruff format --check`）与 `mypy` 作业、Windows 测试作业；发布流程新增 tag 与版本一致性校验及发布前测试

### Changed

- 依赖守卫统一：`analysis` / `docs` / `text` 三个 `_deps` 委托共享核心；`text` 改为惰性探测，`TrendPredictor` / `TextAnalysis` 不再在模块导入时拉起 `jieba` / `wordcloud` / `statsmodels`
- `wei_data_shu.excel` 延迟到调用时导入 `pandas` / `openpyxl`，缺失时给出 `pip install wei-data-shu[excel]` 提示
- 领域包 `__init__` 的惰性 `__getattr__` / `__dir__` 收敛到 `_api.make_getattr` / `_api.make_dir`
- CLI `main()` 改为命令分发表，去掉长 `if/elif` 链
- 全仓库按 `ruff format` 统一格式

### Fixed

- `TrendPredictor` 向 statsmodels 的 `forecast` 传入不受支持的 `alpha` 参数，导致趋势预测直接抛 `TypeError`
- `ExcelOperation.split_table` 未关闭 `pd.ExcelFile`，在 Windows 上会锁住工作簿
- `ExcelManager.read_dataframe(header_row=...)` 参数此前被忽略，始终以第一行为表头
- `ExcelManager.write_sheet` / `quick_excel` 对 DataFrame / ndarray 使用真值判断会抛 “truth value is ambiguous”
- `analysis.read_csv` / `read_json` 默认改用 `utf-8-sig` 并在解码失败时回退 `gbk`，BOM 与 Excel 导出的中文 CSV 可直接读取
- `DailyEmailReport.set_email_content` 在正文为 `None` 时抛 `ValueError`，而不是把 `None` 交给 `MIMEText`
- 调色板中重复的 `#9575CD` / `#7986CB` 条目导致 `search_colors` 返回重复项
- `textCombing.process_text` 不再逐行从当前工作目录读取 `character.json`，缺失配置改为显式参数且只读取一次
- `wei_data_shu/__main__.py` 增加 `if __name__ == "__main__"` 守卫

### Removed

- `tests/__init__.py` 中与环境无关的 ASCII 横幅

## [0.9.2] - 2026-09-16

### Changed

- `wei_data_shu.utils` 公开导出 `read_text` 与 `bom_tolerant_encoding`（0.9.1 新增的 `utils.textio` 原先仅供内部使用），现在可直接 `from wei_data_shu.utils import read_text`；README 功能概览表、项目结构树与使用手册第 11 章同步补充

## [0.9.1] - 2026-09-16

### Fixed

- 带 UTF-8 BOM 的文本文件读取时 BOM 未被剥离：Markdown 首行标题会降级为普通段落、编号列表首行无法识别，`table` 转换出的 CSV 首个列名也会多出一个不可见字符。新增 `wei_data_shu.utils.textio`（`read_text` / `bom_tolerant_encoding`），`read_markdown()` 与 CLI 的 `md2html` / `text clean` / `table` / `mail send --body-file` 改用 BOM 安全读取；`parse_markdown()` 同时忽略直接传入文本开头的 BOM。以 UTF-8 读取时行为在无 BOM 情况下不变，显式指定的其他编码照旧生效
- `analysis` 域的可选依赖提示把「已安装但导入失败」误报为「缺少依赖」，会引导用户重装已经装好的包（例如 matplotlib 缺少 `_c_internal_utils` 扩展时）。`require_deps()` 现在区分「未安装」与「已安装但无法导入」两种情况，后者附带真实异常；`data info` 与 `plot` 子命令改为透传该消息
- `md2html --fragment` 的输出缺少结尾换行，与 `md` / `table` 子命令不一致

### Added

- 新增 `tests/test_cli_edge_cases.py`，覆盖上述三处修复

## [0.9.0] - 2026-09-16

### Added

- CLI 扩展为覆盖全部领域的命令行工具，新增 8 组子命令：
  - `files latest <目录>`：列出创建时间最新的子文件夹
  - `md2html <文件>`：把任意支持的文档渲染为 HTML 页面（`--fragment` 只输出片段，`--title` 附带文档标题）
  - `text clean <文件>`：文本去重与重新编号，`--mode` 可选 `renumber`（默认，同内容不同编号也算重复）、`original`（保留原编号，仅整行相同才去重）、`sql`（转 SQL IN 列表）
  - `table <文件>`：Markdown 表格与 CSV/TSV 互转，`-i` 选择第几个表格，`--delimiter` 指定分隔符
  - `data info <文件>`：打印行列数、逐列非空/缺失/类型与前若干行预览
  - `plot <文件> -o <图片>`：把数据文件画成 `line` / `bar` / `hist` / `box` / `scatter` / `pie` / `heatmap` 图
  - `mail send`：通过 SMTP/SSL 发送纯文本或 HTML 邮件，支持多个收件人与附件，`--dry-run` 仅组装不发送
  - `db query --sql`：执行 MySQL 查询，结果可按 `table` / `csv` / `json` 输出
- `md` 与 `convert` 子命令的文档来源扩展到 `.xlsx` / `.xlsm`
- CLI 中的数据库与邮箱密码支持环境变量 `WEI_DATA_SHU_DB_PASSWORD` / `WEI_DATA_SHU_MAIL_PASSWORD`，避免密码写入命令行历史
- 新增 `tests/test_cli_commands.py`，覆盖上述新增子命令

### Changed

- Excel 工作表名匹配改为不区分大小写（与 Excel 本身行为一致）：`read_sheet` / `write_sheet` / `get_sheet_info` / `delete_sheet` / `copy_sheet` 可用任意大小写引用同一张表，`get_sheet_info` 返回的 `name` 与 `index` 为工作簿中的真实表名
- README 重写：新增「这库是给谁用的」与常见场景速查，安装章节改为「想做的事 → 安装命令」对照表，第一个例子改为零 extras 即可运行
- 使用手册同步补充新增 CLI 子命令的用法

### Fixed

- `ExcelManager` 在工作表名仅大小写不同时的错误行为：原先 `_ensure_sheet` 会误建同名表（openpyxl 自动改名后按原名索引）并抛 `KeyError`，`delete_sheet` 也无法命中大小写不同的表名

## [0.8.0] - 2026-09-16

### Added

- 新增 `docs` 文档域能力：`Document` 格式无关中间模型 + Markdown（零依赖）/ Word（`python-docx`）/ PowerPoint（`python-pptx`）三种后端读写，并支持任意两方互转 `convert()`
- `convert()` 支持 `xlsx` / `.xlsm` 作为第四种**源**格式：整本工作簿按工作表读入（每个工作表一个二级标题 + 表格），空工作表与全空行自动跳过；`xlsx` 不能作为转换目标
- `Document._repr_html_()` 提供 Jupyter HTML 预览（底层 `render_html()`，表格带边框），所有文本与属性值统一 HTML 转义；Markdown / HTML 渲染均零第三方依赖
- 一行式 API：`to_markdown` / `to_word` / `to_ppt` / `read_doc` / `build`，可直接接受 DataFrame、二维列表、`list[str]`、`dict` 或 `Document`
- CLI 新增 `convert`（文档格式互转）与 `md`（把任意支持的文档打印为 Markdown）子命令，`md` 同时支持 `xlsx` 来源
- `wei_data_shu.utils.in_notebook` 提供 Jupyter 环境探测；`Document` 实现 `_repr_markdown_` 与 `_repr_html_`，notebook 中可直接渲染文档预览
- 新增 `[docs]` extras（`python-docx`、`python-pptx`、`openpyxl`）；Markdown 与 HTML 预览位于核心包，零额外依赖
- 新增 `examples/docs_demo.py`，使用手册补充「docs 文档读写与互转」章节

### Changed

- 图表函数在 `show=True` 且后端为无 GUI 的 Agg 时改为记录日志提示，不再静默无效（Jupyter / 交互后端行为不变）
- 版本号提升至 `0.8.0`

### Fixed

- 测试套件在缺少可选依赖时产生假失败：`tests/test_analysis_domain.py` 与 `tests/test_excel_client.py` 原先在模块顶层直接 `import matplotlib` / `import pandas`，未安装对应 extras 时整个模块报 `ERROR` 而非跳过；现改为 try-import + `unittest.skipUnless`（与既有 `tests/test_excel_io.py` 一致），依赖缺失或不可用时降级为 skip
- 修复后在「依赖齐全」「依赖缺失」「依赖损坏（安装不完整）」三种环境下 `python -m unittest discover -s tests -p "test_*.py"` 均无 ERROR

## [0.7.3] - 2026-09-09

### Fixed

- MySQL 连接默认使用 `use_pure=True`，规避 Windows + Python 3.14 环境下 `mysql-connector-python` C Extension 可能触发原生访问冲突；调用方仍可显式设置 `use_pure=False`

## [0.7.2] - 2026-09-04

### Added

- Excel 支持 `.xlsm/.xltm` 文件的 VBA 保留、宏调用，以及当前会话内启用/禁用宏的快捷操作
- README 与使用手册补充 Excel 宏操作示例

### Fixed

- `setup_chinese_font` 模糊匹配时返回实际注册的字体名（而非候选名），并过滤空候选，避免 rcParams 设置未注册字体导致回退

## [0.7.1] - 2026-08-13

### Added

- `analysis` 域新增 `setup_chinese_font()`：导入时自动检测并配置系统 CJK 中文字体（Windows/macOS/Linux 候选），绘图中文标签开箱即用，无需手动设置 `rcParams`

### Changed

- README 增加中英文双语介绍，用法示例抽离为独立使用手册 `docs/USAGE.md`（含完整 CLI 用法介绍）
- release.yml 触发模式修正为 `wei-data-shu-*`（与实际 tag 命名一致），README 补充发布流程说明

## [0.7.0] - 2026-08-13

### Added

- 新增 `analysis` 数据分析域：`read_csv/read_json/read_excel/read_any` 通用读取、`DataCleaner` 链式清洗（缺失/重复/异常值、归一化、类别编码）、7 个图表函数（折线/柱状/直方/箱线/散点/饼图/相关热力图）
- `MySQLDatabase` 支持 `with` 语句上下文管理，退出自动关闭连接
- 新增异常类型：`MySQLDatabaseError`（数据库操作失败统一抛异常）、`MailError`（邮件发送失败）
- `py.typed` 标记 + 公共 API 类型注解（text/utils/mail/database 域），恢复 IDE 补全与静态检查
- CLI 新增 `date`（日期计算）与 `excel info`（工作簿信息）子命令
- 新增 `examples/` 目录：`quickstart.py`、`excel_demo.py`、`chatbot_demo.py`
- 新增 `.github/workflows/release.yml`：打 `v*` tag 自动构建并发布到 PyPI（需配置 `PYPI_TOKEN` secret）
- 测试从 25 增至 38：数据库错误处理、Excel 真实读写、邮件错误路径、CLI 新子命令

### Changed

- 依赖按领域拆分：核心包仅保留 `toml`/`requests`；`pandas`/`openpyxl` 移入 `[excel]` extras，`mysql-connector-python` 移入 `[database]` extras
- 数据库/邮件/Excel/文本模块内部 `print` 改为 `logging`，避免污染调用方输出
- 邮件附件改用 `Path` 拼接 + `MIMEApplication`（UTF-8 文件名），并校验路径与长度
- CI 安装命令更新为 `pip install -e ".[analysis,excel,database]"`

### Removed

- `MySQLDatabase.run_ai_chatbot`：依赖不可用的 `mysql.ai.genai`（MySQL HeatWave 专有模块），已移除。数据库 AI 能力请改用 `wei_data_shu.ai.ChatBot`

### Migration Notes

- `pip install wei-data-shu` 后，使用 Excel/数据库功能需额外安装 `wei-data-shu[excel]` / `wei-data-shu[database]`
- 依赖 `MySQLDatabase` 旧行为（失败静默打印）的代码，请改为捕获 `MySQLDatabaseError`

## [0.6.1] - 2026-03-17

### Added

- added `.github/dependabot.yml` with weekly schedule for pip and GitHub Actions
- added minimum version constraints to all pip dependencies (`pandas>=2.0`, `openpyxl>=3.1`, etc.)

### Changed

- bumped package version to `0.6.1`

## [0.5.3] - 2026-03-17

### Added

- added a `LICENSE` file (GPL-3.0) to the project root, matching existing package metadata
- added GPL-3.0 classifier to `pyproject.toml` and updated all license references in README
- added table of contents, project badges, and cross-reference tables to README
- added `MultipleTrendPredictor` usage example and enriched all domain samples

### Changed

- switched project license from MIT to GPL-3.0 (SPDX: `GPL-3.0-only`)
- rewrote and standardized the entire README: enriched usage examples for all 10 domains, added output samples, improved formatting consistency
- updated project description to bilingual format (Chinese + English)
- bumped package version to `0.5.3`

## [0.5.2] - 2026-03-17

### Added

- added a practical "5-minute quick start" example to the README using `ExcelManager`, `DateFormat`, `search_colors()`, and `generate_password()`

### Changed

- improved README usage documentation structure for faster onboarding
- bumped package version to `0.5.2`

## [0.5.0] - 2026-03-17

### Added

- added a lightweight CLI entrypoint: `wei-data-shu` and `python -m wei_data_shu`
- added `wei_data_shu.utils.generate_password` for readable password generation with ambiguous characters removed
- added searchable color metadata with Chinese display names and `search_colors()` support for English, Chinese, and HEX queries
- added `wei_data_shu.utils` for shared helpers like `fn_timer`, `mav_colors`, and `generate_password`
- added architecture documentation under `docs/plans/`
- added domain-level tests for root package, AI, database, docs, Excel, files, mail, text, and utils

### Changed

- finalized the package architecture around domain packages: `ai`, `database`, `docs`, `excel`, `files`, `mail`, `text`, and `utils`
- restricted root package exports so `wei_data_shu` now exposes domain packages only
- updated README examples to use domain-package imports consistently
- split Excel functionality into dedicated modules under `wei_data_shu.excel`
- reorganized tests into domain-specific test files

### Removed

- removed legacy flat modules such as `SQLManager.py`, `excelManager.py`, `fileManager.py`, `mailManager.py`, `ollamaManager.py`, `stringManager.py`, `textManager.py`, `timingTool.py`, `baseColor.py`, and `chartsManager.py`
- removed support for the old root-level object import style in documentation and public architecture

### Migration Notes

- replace root-level object imports with domain-package imports
- example:

```python
from wei_data_shu.excel import ExcelManager
from wei_data_shu.database import MySQLDatabase
from wei_data_shu.text import DateFormat
```

## [0.4.0] - 2026-02-13

### Added

- introduced a reorganized package layout and modernized package metadata
- improved README coverage for Excel, text analysis, AI chat, and daily email reports

### Changed

- updated the project to publish as `wei-data-shu`
