# Python Standard Library Imports
import time

# Third Party Imports
import dash
import matplotlib.cm as cm
import numpy as np
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
from gensim.models.keyedvectors import KeyedVectors as GensimKeyedVectors
from loguru import logger

# llm_masterclass Imports
from llm_masterclass import google_news
from llm_masterclass import similar_words as masterclass_similar_words

words_to_start = [
    "Paris",
    "Python",
    "Sunday",
    "Tolstoy",
    "Twitter",
    "bachelor",
    "delivery",
    "election",
    "expensive",
    "experience",
    "financial",
    "food",
    "iOS",
    "peace",
    "release",
    "war",
]
options = [{"label": word, "value": word} for word in words_to_start]

word2vec_google_news_300: GensimKeyedVectors = google_news.get_google_news_model()
tsne_model = masterclass_similar_words.create_tsne_model()

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="word-scatter", config={"displayModeBar": False}),
        html.Div(id="word-output"),
        dcc.Input(id="input-word", type="text", placeholder="Input a word..."),
        html.Button("Add Word", id="button-add", n_clicks=0),
        dcc.Dropdown(
            id="dropdown-word",
            options=options,
            value=words_to_start,
            multi=True,
            placeholder="Words to delete...",
        ),
        html.Button("Delete Word(s)", id="button-delete", n_clicks=0),
    ]
)


@app.callback(
    Output("dropdown-word", "value"),
    Output("dropdown-word", "options"),
    Input("button-add", "n_clicks"),
    State("input-word", "value"),
    State("dropdown-word", "options"),
    prevent_initial_call=True,
)
def add_word(n_clicks, input_word, dropdown_options):
    logger.info(f"Current dropdown options: {dropdown_options}")
    current_words = [option["value"] for option in dropdown_options]
    logger.info(f"Current words: {current_words}")
    logger.info(f"Current word: {input_word}")
    new_dropdown_options = [{"label": word, "value": word} for word in current_words]
    if n_clicks == 0 and not input_word:
        return new_dropdown_options
    if input_word not in current_words:  # if the word is new, add it
        new_dropdown_options.append({"label": input_word, "value": input_word})
    logger.info(f"Setting dropdown options: {new_dropdown_options}")
    new_words = [option["value"] for option in new_dropdown_options]
    logger.info(f"Setting dropdown value to: {new_words}")
    return new_words, new_dropdown_options


@app.callback(
    Output("word-scatter", "figure"),
    Input("button-add", "n_clicks"),
    Input("button-delete", "n_clicks"),
    Input("dropdown-word", "value"),
)
def update_graph(n_clicks_add, n_clicks_delete, words):
    logger.info(f"Plotting for words: {words}")
    # Get the colors in rgba format (values between 0 and 1)
    colors = cm.rainbow(np.linspace(0, 1, len(words)))

    # Multiply by 255 to get values between 0 and 255, then convert to integers
    colors = (colors * 255).astype(int)

    # Convert the colors to 'rgba' strings
    colors = ["rgba({},{},{},{})".format(*color) for color in colors]
    (
        word_clusters,
        word_cluster_embeddings_np,
    ) = masterclass_similar_words.get_word_clusters(words, word2vec_google_news_300)
    reshaped_t_sne_embeddings = masterclass_similar_words.get_reshaped_tsne_embeddings(
        word_cluster_embeddings_np, tsne_model
    )
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
            text=f"{word}",
            hoverinfo="text",
            name=word,
        )
        data.append(scatter)

        for i, similar_word in enumerate(similar_words):
            annotations.append(
                dict(
                    x=x[i],
                    y=y[i],
                    xref="x",
                    yref="y",
                    text=similar_word,
                    showarrow=False,
                    font=dict(size=12, color="black"),
                )
            )

    layout = go.Layout(
        title="Similar Words from Google News",
        hovermode="closest",
        xaxis=dict(
            gridcolor="rgb(255, 255, 255)",
            zerolinecolor="rgb(255, 255, 255)",
            showgrid=True,
            showticklabels=False,
            title="",
        ),
        yaxis=dict(
            gridcolor="rgb(255, 255, 255)",
            zerolinecolor="rgb(255, 255, 255)",
            showgrid=True,
            showticklabels=False,
            title="",
        ),
        showlegend=True,
        annotations=annotations,
    )

    return go.Figure(data=data, layout=layout)


if __name__ == "__main__":
    app.run_server(debug=True)
