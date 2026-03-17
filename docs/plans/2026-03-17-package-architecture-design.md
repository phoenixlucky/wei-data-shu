# Package Architecture Finalization

## Requirements Summary

- Remove the old flat `*Manager.py` module model from the public architecture.
- Standardize all usage on domain packages such as `wei_data_shu.excel` and `wei_data_shu.text`.
- Keep the root package minimal so its contract stays stable and easy to reason about.
- Split tests by domain so architectural regressions are easy to localize.

## Final Architecture

```text
wei_data_shu/
├─ __init__.py              # root package, domain-only exports
├─ _api.py                  # root export registry
├─ ai/                      # Ollama chat integration
├─ database/                # database integrations
├─ docs/                    # document workflow facade
├─ excel/                   # workbook manager, handler, client, operations, quick helpers
├─ files/                   # file operations
├─ mail/                    # email reporting
├─ text/                    # text/date utilities and analysis
└─ utils/                   # shared colors and timing helpers
```

Principles:

- Root imports expose domains only.
- Domain packages own their implementations.
- Heavy dependencies are loaded lazily at domain boundaries when practical.
- README examples must always use domain-package imports.

## Key Decisions

### Decision 1
Use `wei_data_shu.__init__` only as a domain router.

Reasoning:

- Root-level object exports caused the public API to grow without clear ownership.
- Domain-only exports make it obvious where new functionality belongs.

Consequence:

- Users now import concrete objects from `wei_data_shu.database`, `wei_data_shu.excel`, `wei_data_shu.text`, and related packages.

### Decision 2
Delete migrated legacy modules instead of keeping compatibility shims.

Reasoning:

- The project had already moved to updated documentation and package structure.
- Keeping duplicate entry points would reintroduce drift and maintenance overhead.

Consequence:

- Internal structure now matches the documented structure.
- Refactors are simpler because there is only one supported import path model.

### Decision 3
Split the Excel implementation by responsibility.

Resulting layout:

- `excel.manager`: core workbook API
- `excel.handler`: range-oriented handler interface
- `excel.client`: Excel desktop integration
- `excel.operations`: split/merge/convert workflows
- `excel.quick`: convenience helpers
- `excel._helpers`: shared implementation helpers

## Testing Strategy

Tests are now organized by architectural slice:

- `test_root_package.py`
- `test_ai_domain.py`
- `test_database_domain.py`
- `test_docs_domain.py`
- `test_excel_domain.py`
- `test_files_domain.py`
- `test_mail_domain.py`
- `test_text_domain.py`
- `test_utils_domain.py`

This keeps boundary checks local to the domain being changed and reduces the chance that one large test file obscures package-level regressions.

## Residual Risks

- Some domain implementations still depend on optional third-party packages such as `pandas`, `openpyxl`, `mysql-connector-python`, and `xlwings`.
- Because local environments may not install every optional dependency, package `__init__` files should continue to avoid eager imports when that would make lightweight inspection or test discovery fail.

## Maintenance Rules

1. Add new user-facing features under an existing domain package or create a new domain package if the capability is genuinely separate.
2. Do not add new root-level object exports.
3. Update README examples whenever a public import path changes.
4. Add or update the matching domain test file for every package-level API change.
