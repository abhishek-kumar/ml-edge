# Third Party Imports
from gensim import downloader
from gensim.models.keyedvectors import KeyedVectors

# llm_masterclass Imports
from llm_masterclass.similar_words import time


@time
def get_google_news_model() -> KeyedVectors:
    return downloader.load("word2vec-google-news-300")
