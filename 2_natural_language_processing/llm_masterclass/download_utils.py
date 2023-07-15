"""
This module defines utility functions for downloading datasets
"""

import gensim.downloader
import gensim
import pandas as pd

def download_word2vec_google_news_300_dim() -> gensim.models.keyedvectors.KeyedVectors:
    """
    Download the Word2Vec Google News 300 dimensional embeddings
    This downloads the embeddings to ~/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz
    """
    return gensim.downloader.load('word2vec-google-news-300')

def download_chicago_data() -> pd.DataFrame:
    download_url = "https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"
    return pd.read_csv(download_url)

