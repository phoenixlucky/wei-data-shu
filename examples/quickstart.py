"""快速上手示例：密码、颜色、日期、Excel（对应 README 快速开始）。"""

from wei_data_shu.excel import ExcelManager
from wei_data_shu.text import DateFormat
from wei_data_shu.utils import generate_password, search_colors


def main() -> None:
    # 1. 生成一个易读密码
    print("密码:", generate_password(13))

    # 2. 搜索颜色
    for record in search_colors("薄荷"):
        print("颜色:", record["hex"], record["name"], record["name_zh"])

    # 3. 昨天的日期
    print("昨天:", DateFormat(interval_day=1).get_timeparameter())

    # 4. Excel 写入 + 读取（需要 excel extras: pip install 'wei-data-shu[excel]'）
    with ExcelManager("example.xlsx") as manager:
        manager.write_sheet("sheet1", [["姓名", "分数"], ["张三", 90]], 1, 1, 2, 2)
        print("读取:", manager.read_sheet("sheet1", 1, 1, 2, 2))


if __name__ == "__main__":
    main()
