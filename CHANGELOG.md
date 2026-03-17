# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and the project follows Semantic Versioning in a pragmatic way:

- minor releases may include breaking changes before `1.0.0`
- patch releases are reserved for backwards-compatible fixes and documentation-only corrections

## [0.5.1] - 2026-03-17

### Added

- added a practical "5-minute quick start" example to the README using `ExcelManager`, `DateFormat`, `search_colors()`, and `generate_password()`

### Changed

- improved README usage documentation structure for faster onboarding
- bumped package version to `0.5.1`

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
