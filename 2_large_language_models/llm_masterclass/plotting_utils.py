# Python Standard Library Imports
from typing import List

# Third Party Imports
import matplotlib.cm as cm
import numpy as np
import plotly.graph_objects as go
from loguru import logger


def get_colors(words: List[str]) -> List[str]:
    # Get the colors in rgba format (values between 0 and 1)
    colors = cm.rainbow(np.linspace(0, 1, len(words)))

    # Multiply by 255 to get values between 0 and 255, then convert to integers
    colors = (colors * 255).astype(int)

    # Convert the colors to 'rgba' strings
    colors = ["rgba({},{},{},{})".format(*color) for color in colors]
    return colors


def generate_plot_data_and_annotations(
    words, word_clusters, reshaped_t_sne_embeddings, colors
):
    data = []
    annotations = []
    for word, embeddings, similar_words, color in zip(
        words, reshaped_t_sne_embeddings, word_clusters, colors
    ):
        x = embeddings[:, 0]
        y = embeddings[:, 1]
        scatter = go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(
                color=color, size=10, line=dict(color="Black", width=2), opacity=0.7
            ),
            text=similar_words,
            hoverinfo="text",
            name=word,
        )
        data.append(scatter)

        r = 0.2
        annotations.append(
            dict(
                x=(1 + r) * np.mean(x),
                y=(1 + r) * np.mean(y),
                xref="x",
                yref="y",
                text=word,
                showarrow=False,
                font=dict(size=20, color=color),
            )
        )

    return data, annotations
