# Python Standard Library Imports
from typing import List

# Third Party Imports
import numpy as np
from gensim.models.keyedvectors import KeyedVectors as GensimKeyedVectors
from sklearn.manifold import TSNE


def get_word_clusters(words, word2vec_model: GensimKeyedVectors, topn=30):
    """
    Given a list of words and a word2vec model, return a list of lists of similar words and a list of lists of similar word embeddings.
    """
    word_clusters: List[List[str]] = []
    word_cluster_embeddings: List[List[np.ndarray]] = []
    # for each of our query words
    for word in words:
        most_similar_words: List[str] = []
        most_similar_words_embeddings: List[np.ndarray] = []
        # generate a length 30 list of most similar words from our vocabulary
        for similar_word, similarity in word2vec_model.most_similar(word, topn=topn):
            # and add those words and their embeddings back
            most_similar_words.append(similar_word)
            most_similar_words_embeddings.append(word2vec_model[similar_word])
        # then, append the list of most similar words and their embeddings to the aggregate list
        word_cluster_embeddings.append(most_similar_words_embeddings)
        word_clusters.append(most_similar_words)

    return word_clusters, np.array(word_cluster_embeddings)


def create_tsne_model(
    perplexity=15, n_components=2, init="pca", n_iter=3500, random_state=32, n_jobs=-1
):
    return TSNE(
        perplexity=perplexity,
        n_components=n_components,
        init=init,
        n_iter=n_iter,
        random_state=random_state,
        n_jobs=n_jobs,
    )


def get_reshaped_tsne_embeddings(word_cluster_embeddings_np, tsne_model):
    """
    Given a list of lists of word embeddings, return a list of lists of t-SNE embeddings.
    """
    # n samples, by m similar words, by d dimensions
    n, m, d = word_cluster_embeddings_np.shape
    tsne_training_set = word_cluster_embeddings_np.reshape(n * m, d)
    t_sne_embeddings = tsne_model.fit_transform(tsne_training_set)
    return t_sne_embeddings.reshape(n, m, 2)
