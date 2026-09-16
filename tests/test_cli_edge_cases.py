"""Edge cases found while auditing the 0.9.0 release.

覆盖三处修复：

- 带 UTF-8 BOM 的输入文件（Markdown 首行标题 / 编号列表首行 / 表格首个列名）
- 依赖「已安装但导入失败」与「未安装」的提示区分
- ``md2html --fragment`` 的输出以换行结尾
"""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from wei_data_shu.cli import main
from wei_data_shu.docs import read_markdown
from wei_data_shu.utils.textio import bom_tolerant_encoding, read_text

_BOM = "\ufeff"


class TestBomTolerantEncoding(unittest.TestCase):
    def test_utf8_spellings_become_utf8_sig(self):
        for spelling in ("utf-8", "UTF-8", "utf8", "UTF_8", "utf-8-sig"):
            with self.subTest(spelling=spelling):
                self.assertEqual(bom_tolerant_encoding(spelling), "utf-8-sig")

    def test_other_encodings_are_untouched(self):
        self.assertEqual(bom_tolerant_encoding("gbk"), "gbk")
        self.assertEqual(bom_tolerant_encoding("utf-16"), "utf-16")


class TestBomTolerantReading(unittest.TestCase):
    def test_read_text_strips_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.txt"
            path.write_text(_BOM + "hello\n", encoding="utf-8")
            self.assertEqual(read_text(path), "hello\n")

    def test_read_text_keeps_plain_file_intact(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.txt"
            path.write_text("hello\n", encoding="utf-8")
            self.assertEqual(read_text(path), "hello\n")

    def test_explicit_non_utf8_encoding_still_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gbk.txt"
            path.write_bytes("中文\n".encode("gbk"))
            self.assertEqual(read_text(path, "gbk"), "中文\n")

    def test_read_markdown_parses_heading_after_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            path.write_text(_BOM + "# 月报\n\n正文\n", encoding="utf-8")
            document = read_markdown(path)
            self.assertEqual(document.to_markdown().splitlines()[0], "# 月报")
            self.assertNotIn(_BOM, document.to_markdown())

    def test_read_markdown_still_parses_plain_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            path.write_text("# 月报\n\n正文\n", encoding="utf-8")
            self.assertEqual(read_markdown(path).to_markdown().splitlines()[0], "# 月报")


class TestCliBomInputs(unittest.TestCase):
    def test_md2html_keeps_first_heading_as_h1(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            path.write_text(_BOM + "# 月报\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["md2html", str(path), "--fragment"])
        self.assertEqual(exit_code, 0)
        self.assertIn("<h1>月报</h1>", stdout.getvalue())

    def test_text_clean_recognises_first_numbered_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.txt"
            path.write_text(_BOM + "1. apple\n2. banana\n3. apple\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["text", "clean", str(path)])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue().strip().splitlines(), ["1、apple", "2、banana"])

    def test_table_command_reads_first_column_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            path.write_text(_BOM + "| a | b |\n| --- | --- |\n| 1 | 2 |\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(path)])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue().splitlines()[0], "a,b")


class TestDependencyMessages(unittest.TestCase):
    """包已安装但损坏时，不应让用户再去装一遍。"""

    def test_import_failure_is_reported_as_such(self):
        from wei_data_shu.analysis import _deps

        with patch.object(_deps, "_IMPORT_ERRORS", {"matplotlib": "ImportError: boom"}), patch.object(
            _deps, "plt", None
        ), patch.object(_deps, "find_spec", return_value=object()):
            with self.assertRaises(ImportError) as ctx:
                _deps.require_deps("matplotlib")

        message = str(ctx.exception)
        self.assertIn("已安装但无法导入", message)
        self.assertIn("ImportError: boom", message)

    def test_missing_dependency_keeps_install_hint(self):
        from wei_data_shu.analysis import _deps

        with patch.object(_deps, "_IMPORT_ERRORS", {}), patch.object(_deps, "np", None), patch.object(
            _deps, "find_spec", return_value=None
        ):
            with self.assertRaises(ImportError) as ctx:
                _deps.require_deps("numpy")

        message = str(ctx.exception)
        self.assertIn("numpy 未安装", message)
        self.assertIn("pip install wei-data-shu[analysis]", message)

    def test_plot_command_surfaces_the_real_reason(self):
        reason = "当前功能缺少可用依赖: matplotlib 已安装但无法导入（ImportError: boom）"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rows.csv"
            path.write_text("name,value\nA,1\n", encoding="utf-8")
            stdout = io.StringIO()
            with patch("wei_data_shu.analysis._deps.require_deps", side_effect=ImportError(reason)):
                with redirect_stdout(stdout):
                    exit_code = main(
                        ["plot", str(path), "-k", "bar", "-x", "name", "-y", "value", "-o", str(Path(tmp) / "c.png")]
                    )
        self.assertEqual(exit_code, 1)
        self.assertIn("依赖不可用", stdout.getvalue())
        self.assertIn("已安装但无法导入", stdout.getvalue())


class TestCliOutputNewline(unittest.TestCase):
    def test_md2html_fragment_ends_with_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            path.write_text("# 月报\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["md2html", str(path), "--fragment"])
        self.assertEqual(exit_code, 0)
        self.assertTrue(stdout.getvalue().endswith("\n"))

    def test_md_command_ends_with_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            path.write_text("# 月报\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["md", str(path)])
        self.assertEqual(exit_code, 0)
        self.assertTrue(stdout.getvalue().endswith("\n"))


if __name__ == "__main__":
    unittest.main()
