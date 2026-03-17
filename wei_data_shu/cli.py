"""Command-line interface for wei-data-shu."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from wei_data_shu.utils import generate_password, search_colors


def _ensure_utf8_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wei-data-shu", description="Utilities for wei-data-shu")
    subparsers = parser.add_subparsers(dest="command")

    password_parser = subparsers.add_parser("password", help="Generate readable passwords")
    password_parser.add_argument("-l", "--length", type=int, default=13, help="Password length")
    password_parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate")

    colors_parser = subparsers.add_parser("colors", help="View or search color palette")
    colors_parser.add_argument("query", nargs="?", help="Search by hex, English name, or Chinese name")

    return parser


def _run_password(args: argparse.Namespace) -> int:
    if args.count <= 0:
        raise ValueError("count must be greater than 0")
    for _ in range(args.count):
        print(generate_password(args.length))
    return 0


def _run_colors(args: argparse.Namespace) -> int:
    results = search_colors(args.query)
    if not results:
        print(f'No colors matched "{args.query}".')
        return 1

    for record in results:
        print(f'{record["index"]:>2}. {record["hex"]} | {record["name"]} | {record["name_zh"]}')
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    _ensure_utf8_stdout()
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "password":
        return _run_password(args)
    if args.command == "colors":
        return _run_colors(args)

    parser.print_help()
    return 0


__all__ = ["main"]
