"""Text analysis utilities (tokenization and word cloud plotting)."""

from __future__ import annotations

from collections import Counter
from typing import Any

from ._deps import require_analysis_deps


def _load_text_deps() -> tuple[Any, Any, Any, Any]:
    """按需加载分词 / 绘图依赖（模块导入时不拉起重依赖）。"""
    import jieba
    import numpy as np
    from matplotlib import pyplot as plt
    from wordcloud import WordCloud

    return jieba, np, plt, WordCloud


class TextAnalysis:
    def __init__(self, dataframe: Any) -> None:
        require_analysis_deps("jieba", "numpy", "matplotlib", "wordcloud", "pandas")
        self.df = dataframe

    def get_word_freq(self, group_col: str, text_col: str, agg_func: Any) -> Any:
        aggregated_text = self.df.groupby(group_col)[text_col].apply(agg_func).reset_index()
        aggregated_text["word_freq"] = aggregated_text[text_col].apply(self.compute_word_freq)
        return aggregated_text

    def compute_word_freq(self, text: str) -> Counter[str]:
        jieba, _, _, _ = _load_text_deps()
        words = jieba.cut(text)
        return Counter(words)

    def plot_wordclouds(
        self,
        word_freqs: list[Any],
        titles: list[str],
        save_path: str = "wordclouds.png",
    ) -> None:
        _, np, plt, WordCloud = _load_text_deps()

        def create_ellipse_mask(width: int, height: int) -> Any:
            y, x = np.ogrid[-height // 2 : height // 2, -width // 2 : width // 2]
            mask = (x**2 / (width // 2) ** 2 + y**2 / (height // 2) ** 2) <= 1
            return 255 * mask.astype(int)

        ellipse_mask = 255 - create_ellipse_mask(400, 200)
        num_plots = len(word_freqs)
        if num_plots == 0:
            raise ValueError("word_freqs 不能为空")

        from wei_data_shu.analysis.charts import resolve_font_path

        font_path = resolve_font_path()
        font_kwargs = {"font_path": font_path} if font_path else {}

        cols = 2
        rows = (num_plots + 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(16, 8))
        axes = np.array(axes).reshape(rows, cols)

        plotted = 0
        for i, (word_freq, title) in enumerate(zip(word_freqs, titles)):
            ax = axes[i // cols, i % cols]
            wordcloud = WordCloud(
                width=400,
                height=200,
                max_words=200,
                background_color="white",
                mask=ellipse_mask,
                **font_kwargs,
            ).generate_from_frequencies(word_freq)

            ax.imshow(wordcloud, interpolation="bilinear")
            ax.set_title(title)
            ax.axis("off")
            ax.set_xticks([])
            ax.set_yticks([])
            plotted += 1

        for j in range(plotted, rows * cols):
            fig.delaxes(axes[j // cols, j % cols])

        plt.tight_layout()
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)


__all__ = ["TextAnalysis"]
