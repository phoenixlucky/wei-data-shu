"""Color palette data and search helpers."""

from __future__ import annotations

mav_colors = [
    "#60ACFC",
    "#32D3EB",
    "#5BC49F",
    "#FEB64D",
    "#FF7C7C",
    "#9287E7",
    "#FFDD55",
    "#FFAA85",
    "#A8E6CF",
    "#DCE775",
    "#FF8A65",
    "#9575CD",
    "#81C784",
    "#4DD0E1",
    "#BA68C8",
    "#7986CB",
    "#4FC3F7",
    "#F06292",
    "#AED581",
    "#FFD54F",
    "#FFAB91",
    "#FBC02D",
    "#8D6E63",
    "#BDBDBD",
    "#FFCDD2",
    "#C5E1A5",
    "#80DEEA",
    "#CE93D8",
    "#F48FB1",
    "#B39DDB",
    "#FF7043",
    "#D4E157",
    "#FFEB3B",
    "#9575CD",
    "#7986CB",
    "#E57373",
    "#FFF176",
    "#FFB74D",
    "#A1887F",
]

_COLOR_ZH_NAMES = [
    "亮天蓝",
    "海晶蓝",
    "薄荷绿",
    "杏橙",
    "珊瑚红",
    "紫藤",
    "明黄",
    "蜜桃橙",
    "冰薄荷",
    "嫩柠黄",
    "暖橙",
    "淡紫罗兰",
    "青草绿",
    "湖水蓝",
    "兰花紫",
    "雾霾蓝",
    "晴空蓝",
    "玫粉",
    "鼠尾草绿",
    "金盏黄",
    "蜜桃粉",
    "琥珀黄",
    "可可棕",
    "中性灰",
    "樱花粉",
    "浅叶绿",
    "浅青蓝",
    "淡薰衣草",
    "蔷薇粉",
    "丁香紫",
    "日落橙",
    "青柠绿",
    "柠檬黄",
    "淡紫罗兰",
    "雾霾蓝",
    "豆沙红",
    "奶油黄",
    "木瓜橙",
    "奶茶棕",
]

_COLOR_EN_NAMES = [
    "sky blue",
    "aqua blue",
    "mint green",
    "apricot orange",
    "coral red",
    "wisteria purple",
    "sunny yellow",
    "peach orange",
    "ice mint",
    "lime cream",
    "warm orange",
    "soft violet",
    "grass green",
    "lagoon blue",
    "orchid purple",
    "mist blue",
    "clear sky blue",
    "rose pink",
    "sage green",
    "marigold yellow",
    "peach pink",
    "amber yellow",
    "cocoa brown",
    "neutral gray",
    "blush pink",
    "leaf green",
    "cyan mist",
    "lavender mist",
    "camellia pink",
    "lilac",
    "sunset orange",
    "lime green",
    "lemon yellow",
    "soft violet",
    "mist blue",
    "dusty rose",
    "butter yellow",
    "papaya orange",
    "latte brown",
]

color_records = [
    {
        "index": index,
        "hex": color,
        "name": en_name,
        "name_zh": zh_name,
        "aliases": {color.lower(), en_name.lower(), zh_name},
    }
    for index, (color, en_name, zh_name) in enumerate(
        zip(mav_colors, _COLOR_EN_NAMES, _COLOR_ZH_NAMES),
        start=1,
    )
]


def search_colors(query: str | None = None) -> list[dict[str, object]]:
    """Search colors by hex, English name, or Chinese name."""

    if query is None:
        return list(color_records)

    normalized = query.strip().lower()
    if not normalized:
        return list(color_records)

    results: list[dict[str, object]] = []
    for record in color_records:
        haystack = {
            record["hex"].lower(),
            str(record["name"]).lower(),
            str(record["name_zh"]),
        }
        aliases = {str(alias).lower() for alias in record["aliases"]}
        if any(normalized in candidate for candidate in haystack | aliases):
            results.append(record)
    return results


__all__ = ["mav_colors", "color_records", "search_colors"]
