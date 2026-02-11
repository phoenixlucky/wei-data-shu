"""Text analysis utilities (tokenization and word cloud plotting)."""

from collections import Counter

from ._deps import WordCloud, jieba, np, plt, require_analysis_deps


class TextAnalysis:
    def __init__(self, dataframe):
        require_analysis_deps("jieba", "numpy", "matplotlib", "wordcloud", "pandas")
        self.df = dataframe

    def get_word_freq(self, group_col, text_col, agg_func):
        aggregated_text = self.df.groupby(group_col)[text_col].apply(agg_func).reset_index()
        aggregated_text["word_freq"] = aggregated_text[text_col].apply(self.compute_word_freq)
        return aggregated_text

    def compute_word_freq(self, text):
        words = jieba.cut(text)
        return Counter(words)

    def plot_wordclouds(self, word_freqs, titles, save_path="wordclouds.png"):
        def create_ellipse_mask(width, height):
            y, x = np.ogrid[-height // 2 : height // 2, -width // 2 : width // 2]
            mask = (x**2 / (width // 2) ** 2 + y**2 / (height // 2) ** 2) <= 1
            return 255 * mask.astype(int)

        ellipse_mask = 255 - create_ellipse_mask(400, 200)
        num_plots = len(word_freqs)
        if num_plots == 0:
            raise ValueError("word_freqs 不能为空")

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
                font_path="C:/Windows/Fonts/SimHei.ttf",
                background_color="white",
                mask=ellipse_mask,
            ).generate_from_frequencies(word_freq)

            ax.imshow(wordcloud, interpolation="bilinear")
            ax.set_title(title)
            ax.axis("off")
            ax.set_xticks([])
            ax.set_yticks([])
            plotted += 1

        for j in range(plotted, rows * cols):
            fig.delaxes(axes[j // cols, j % cols])

        plt.axis("off")
        plt.tight_layout()
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()


__all__ = ["TextAnalysis"]
