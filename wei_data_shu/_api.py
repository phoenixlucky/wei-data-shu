"""Central public API registry for `wei-data-shu`.

This keeps the package-level exports and domain subpackage exports in one
place so the implementation can be reorganized without repeatedly touching
multiple import surfaces.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterable, Mapping
from typing import Any, Dict, Tuple

ExportTarget = Tuple[str, str | None]
ExportMap = Dict[str, ExportTarget]

DOMAIN_EXPORTS: dict[str, ExportMap] = {
    "domains": {
        "ai": ("wei_data_shu.ai", None),
        "analysis": ("wei_data_shu.analysis", None),
        "database": ("wei_data_shu.database", None),
        "docs": ("wei_data_shu.docs", None),
        "excel": ("wei_data_shu.excel", None),
        "files": ("wei_data_shu.files", None),
        "mail": ("wei_data_shu.mail", None),
        "text": ("wei_data_shu.text", None),
        "utils": ("wei_data_shu.utils", None),
    },
}


def flatten_exports(*domains: str) -> ExportMap:
    exports: ExportMap = {}
    for domain in domains:
        exports.update(DOMAIN_EXPORTS[domain])
    return exports


ROOT_EXPORTS = flatten_exports("domains")


def export_names(exports: ExportMap) -> list[str]:
    return sorted(exports)


def domain_all(*domains: str) -> list[str]:
    names: list[str] = []
    for domain in domains:
        names.extend(DOMAIN_EXPORTS[domain].keys())
    return sorted(set(names))


def make_getattr(module_name: str, exports: Mapping[str, ExportTarget]) -> Callable[[str], Any]:
    """为领域包生成惰性 ``__getattr__``。

    ``import_module`` 是运行时从目标模块的全局命名空间取的，因此
    ``patch("wei_data_shu.<domain>.import_module")`` 仍然可以拦截。
    """

    def __getattr__(name: str) -> Any:
        target = exports.get(name)
        if target is None:
            raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
        module_path, attr_name = target
        import_module = getattr(sys.modules[module_name], "import_module")
        module = import_module(module_path)
        return module if attr_name is None else getattr(module, attr_name)

    return __getattr__


def make_dir(
    module_name: str,
    exports: Mapping[str, ExportTarget],
    extra: Iterable[str] = (),
) -> Callable[[], list[str]]:
    """为领域包生成 ``__dir__``，把惰性导出的名字也列入。"""

    def __dir__() -> list[str]:
        module = sys.modules[module_name]
        return sorted(set(module.__dict__.keys()) | set(exports) | set(extra))

    return __dir__


__all__ = [
    "DOMAIN_EXPORTS",
    "ROOT_EXPORTS",
    "ExportMap",
    "ExportTarget",
    "domain_all",
    "export_names",
    "flatten_exports",
    "make_dir",
    "make_getattr",
]
