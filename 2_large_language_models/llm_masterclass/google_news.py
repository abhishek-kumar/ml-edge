# Third Party Imports
from gensim import downloader
from gensim.models.keyedvectors import KeyedVectors


def get_google_news_model() -> KeyedVectors:
    return downloader.load("word2vec-google-news-300")
