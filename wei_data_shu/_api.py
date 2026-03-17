"""Central public API registry for `wei-data-shu`.

This keeps the package-level exports and domain subpackage exports in one
place so the implementation can be reorganized without repeatedly touching
multiple import surfaces.
"""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

ExportTarget = Tuple[str, str | None]
ExportMap = Dict[str, ExportTarget]

DOMAIN_EXPORTS: dict[str, ExportMap] = {
    "domains": {
        "ai": ("wei_data_shu.ai", None),
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


__all__ = [
    "DOMAIN_EXPORTS",
    "ROOT_EXPORTS",
    "ExportMap",
    "ExportTarget",
    "domain_all",
    "export_names",
    "flatten_exports",
]
