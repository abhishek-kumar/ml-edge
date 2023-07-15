"""
Test the functionality defined inside the procesing submodule of llm_masterclass package
"""

import pytest
import llm_masterclass.download_utils as du
import llm_masterclass.processing as pc
import pydantic

@pytest.fixture(scope="session")
def gensim_word2vec_google_news_300_model():
    return du.download_word2vec_google_news_300_dim()

def test_cant_instantiate_embedding_model_protocol():
    with pytest.raises(TypeError):
        pc.EmbeddingModelProtocol()

def test_can_validate_signature_to_most_similar():
    pc.MostSimilarSignature(word='test', topn=10)

def test_rejects_invalid_signature_to_most_similar():
    with pytest.raises(pydantic.ValidationError):
        pc.MostSimilarSignature(word=20, topn='10')

# def test_can_generate_similar_words_embeddings(gensim_word2vec_google_news_300_model):
    words = ['Paris', 'Python']
    topn = 4
    similar_word_embeddings: pc.SimilarWordsEmbeddings = pc.generate_similar_words_embeddings(
        words, 
        pc.GensimEmbeddingModel(gensim_word2vec_google_news_300_model), 
        topn=topn
    )
    assert len(similar_word_embeddings.words) == len(words)

