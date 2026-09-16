"""Tests for the file / document / text / table / analysis / mail / db CLI commands."""

import io
import json
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from wei_data_shu.cli import _print_rows, main


class TestCliFilesCommand(unittest.TestCase):
    def test_latest_picks_newest_subfolder(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "old").mkdir()
            time.sleep(0.03)
            (base / "new").mkdir()
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["files", "latest", str(base)])
            self.assertEqual(exit_code, 0)
            self.assertEqual(Path(stdout.getvalue().strip()).name, "new")

    def test_latest_rejects_missing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["files", "latest", str(Path(tmp) / "nope")])
        self.assertEqual(exit_code, 1)
        self.assertIn("目录不存在", stdout.getvalue())

    def test_latest_reports_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["files", "latest", tmp])
        self.assertEqual(exit_code, 1)
        self.assertIn("没有子目录", stdout.getvalue())


class TestCliMd2HtmlCommand(unittest.TestCase):
    def test_wraps_markdown_into_full_html_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "doc.md"
            source.write_text("# 月度报告\n\n正文\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["md2html", str(source)])
        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertTrue(output.startswith("<!DOCTYPE html>"))
        self.assertIn('<meta charset="utf-8">', output)
        self.assertIn("<h1>月度报告</h1>", output)

    def test_fragment_mode_omits_page_wrapper(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "doc.md"
            source.write_text("# 月度报告\n\n正文\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["md2html", str(source), "--fragment"])
        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertNotIn("<!DOCTYPE html>", output)
        self.assertIn("<h1>月度报告</h1>", output)

    def test_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "doc.md"
            source.write_text("# 标题\n", encoding="utf-8")
            target = Path(tmp) / "doc.html"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["md2html", str(source), "-o", str(target)])
            self.assertEqual(exit_code, 0)
            self.assertIn("<!DOCTYPE html>", target.read_text(encoding="utf-8"))


class TestCliTextCommand(unittest.TestCase):
    def test_clean_renumbers_and_drops_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "notes.txt"
            source.write_text("1、苹果\n2、香蕉\n3、苹果\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["text", "clean", str(source)])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue().splitlines(), ["1、苹果", "2、香蕉"])

    def test_clean_sql_mode_builds_in_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "notes.txt"
            source.write_text("1、苹果\n2、香蕉\n3、苹果\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["text", "clean", str(source), "--mode", "sql"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue().strip(), '"1、苹果","2、香蕉","3、苹果"')

    def test_clean_original_keeps_numbers_and_only_drops_exact_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "notes.txt"
            # 「1、苹果」与「3、苹果」内容相同但编号不同，original 模式不剥离编号，两行都保留；
            # 完全相同的「1、苹果」则被去掉。
            source.write_text("1、苹果\n1、苹果\n3、苹果\n1、香蕉\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["text", "clean", str(source), "--mode", "original"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue().splitlines(), ["1、苹果", "3、苹果", "1、香蕉"])

    def test_clean_reports_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["text", "clean", str(Path(tmp) / "nope.txt")])
        self.assertEqual(exit_code, 1)
        self.assertIn("读取失败", stdout.getvalue())


class TestCliTableCommand(unittest.TestCase):
    def test_markdown_to_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "table.md"
            source.write_text("| 名称 | 数量 |\n| --- | --- |\n| 苹果 | 3 |\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(source)])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), "名称,数量\n苹果,3\n")

    def test_csv_to_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "table.csv"
            source.write_text("名称,数量\n苹果,3\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(source)])
        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("| 名称 | 数量 |", output)
        self.assertIn("| --- | --- |", output)
        self.assertIn("| 苹果 | 3 |", output)

    def test_table_index_selects_second_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "table.md"
            source.write_text(
                "| a | b |\n| --- | --- |\n| 1 | 2 |\n\n| c | d |\n| --- | --- |\n| 3 | 4 |\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(source), "--index", "1"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), "c,d\n3,4\n")

    def test_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "table.md"
            source.write_text("| a | b |\n| --- | --- |\n| 1 | 2 |\n", encoding="utf-8")
            target = Path(tmp) / "out.csv"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(source), "-o", str(target)])
            self.assertEqual(exit_code, 0)
            self.assertEqual(target.read_text(encoding="utf-8"), "a,b\n1,2\n")

    def test_rejects_unsupported_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "table.txt"
            source.write_text("a,1\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(source)])
        self.assertEqual(exit_code, 1)
        self.assertIn("不支持的文件类型", stdout.getvalue())

    def test_reports_document_without_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "doc.md"
            source.write_text("# 只有标题\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(source)])
        self.assertEqual(exit_code, 1)
        self.assertIn("未找到 Markdown 表格", stdout.getvalue())

    def test_reports_out_of_range_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "table.md"
            source.write_text("| a | b |\n| --- | --- |\n| 1 | 2 |\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["table", str(source), "--index", "3"])
        self.assertEqual(exit_code, 1)
        self.assertIn("越界", stdout.getvalue())


class TestCliAnalysisCommands(unittest.TestCase):
    def test_data_info_without_pandas_prints_install_hint(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch("wei_data_shu.analysis._deps.pd", None):
            exit_code = main(["data", "info", "missing.csv"])
        self.assertEqual(exit_code, 1)
        self.assertIn("wei-data-shu[analysis]", stdout.getvalue())

    def test_plot_without_pandas_prints_install_hint(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch("wei_data_shu.analysis._deps.pd", None):
            exit_code = main(["plot", "missing.csv", "-o", "chart.png", "-k", "line"])
        self.assertEqual(exit_code, 1)
        self.assertIn("wei-data-shu[analysis]", stdout.getvalue())

    def test_plot_without_matplotlib_prints_install_hint(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch("wei_data_shu.analysis._deps.plt", None):
            exit_code = main(["plot", "missing.csv", "-o", "chart.png", "-k", "line"])
        self.assertEqual(exit_code, 1)
        self.assertIn("wei-data-shu[analysis]", stdout.getvalue())


class TestCliMailCommand(unittest.TestCase):
    def test_send_requires_password(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch.dict("os.environ", {}, clear=True):
            exit_code = main(
                ["mail", "send", "--host", "smtp.example.com", "--user", "a@b.c", "-t", "z@y.z", "-s", "Hi", "-b", "body"]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("WEI_DATA_SHU_MAIL_PASSWORD", stdout.getvalue())

    def test_send_reads_password_from_environment(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch.dict("os.environ", {"WEI_DATA_SHU_MAIL_PASSWORD": "pw"}), patch(
            "wei_data_shu.mail.report.DailyEmailReport.send_email"
        ) as send_email:
            exit_code = main(
                ["mail", "send", "--host", "smtp.example.com", "--user", "a@b.c", "-t", "z@y.z", "-s", "Hi", "-b", "body"]
            )
        self.assertEqual(exit_code, 0)
        send_email.assert_called_once()

    def test_dry_run_composes_without_sending(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch("wei_data_shu.mail.report.DailyEmailReport.send_email") as send_email:
            exit_code = main(
                [
                    "mail",
                    "send",
                    "--host",
                    "smtp.example.com",
                    "--user",
                    "a@b.c",
                    "--password",
                    "pw",
                    "-t",
                    "z@y.z",
                    "-s",
                    "Hi",
                    "-b",
                    "body",
                    "--dry-run",
                ]
            )
        self.assertEqual(exit_code, 0)
        send_email.assert_not_called()
        self.assertIn("--dry-run", stdout.getvalue())

    def test_dry_run_reports_missing_attachment(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "mail",
                        "send",
                        "--host",
                        "smtp.example.com",
                        "--user",
                        "a@b.c",
                        "--password",
                        "pw",
                        "-t",
                        "z@y.z",
                        "-s",
                        "Hi",
                        "-b",
                        "body",
                        "--dry-run",
                        "-a",
                        str(Path(tmp) / "nope.txt"),
                    ]
                )
        self.assertEqual(exit_code, 1)
        self.assertIn("附件不存在", stdout.getvalue())

    def test_send_requires_body(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(
                ["mail", "send", "--host", "smtp.example.com", "--user", "a@b.c", "--password", "pw", "-t", "z@y.z", "-s", "Hi"]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("缺少正文", stdout.getvalue())


class TestCliDbCommand(unittest.TestCase):
    def test_query_requires_password(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), patch.dict("os.environ", {}, clear=True):
            exit_code = main(["db", "query", "--user", "u", "--database", "d", "--sql", "SELECT 1"])
        self.assertEqual(exit_code, 1)
        self.assertIn("WEI_DATA_SHU_DB_PASSWORD", stdout.getvalue())


class TestCliRowFormatting(unittest.TestCase):
    """``_print_rows`` 是 db query 的输出层，这里直接覆盖三种格式。"""

    def test_table_format_aligns_cjk_columns(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            _print_rows([{"名称": "苹果", "数量": 3}, {"名称": "banana", "数量": None}], "table")
        self.assertEqual(
            stdout.getvalue().splitlines(),
            ["名称    数量", "------  ----", "苹果    3", "banana  NULL"],
        )

    def test_csv_format_prints_header_then_rows(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            _print_rows([{"a": 1, "b": "x"}], "csv")
        self.assertEqual(stdout.getvalue(), "a,b\n1,x\n")

    def test_json_format_keeps_non_ascii_readable(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            _print_rows([{"名称": "苹果"}], "json")
        self.assertEqual(json.loads(stdout.getvalue()), [{"名称": "苹果"}])

    def test_empty_result_set(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            _print_rows([], "table")
        self.assertEqual(stdout.getvalue().strip(), "(0 行)")


if __name__ == "__main__":
    unittest.main()
