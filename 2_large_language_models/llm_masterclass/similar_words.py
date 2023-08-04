# Python Standard Library Imports
from typing import List

# Third Party Imports
import numpy as np
from gensim.models.keyedvectors import KeyedVectors as GensimKeyedVectors


def get_word_clusters(words, word2vec_model: GensimKeyedVectors, topn=30):
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
