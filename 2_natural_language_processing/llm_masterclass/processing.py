from pydantic import BaseModel, validator
from typing import Protocol, List
import numpy as np
from tqdm import tqdm

class MostSimilarSignature(BaseModel):
    word: str
    topn: int

    @validator('word')
    def validate_word(cls, word):
        if word.isalpha():
            return word
        else:
            raise TypeError("Input word contains more than letters")

class MostSimilarReturnType(BaseModel):
    words: List[List[str]]
    similarity : List[List[np.ndarray]]
    class Config:
        arbitrary_types_allowed = True

    @validator('embeddings')
    def validate_embeddings(cls, v):
        return v
            
class EmbeddingModelProtocol(Protocol):
    def most_similar(self, args: MostSimilarSignature) -> MostSimilarReturnType:
        ...

class GensimEmbeddingModel:
    """
    Just a thin wrapper around gensim most_similar, but we have validation due to the types.
    """
    def __init__(self, embedding_model):
        self._model = embedding_model

    def most_similar(self, args: MostSimilarSignature) -> MostSimilarReturnType:
        list_of_similar_words = self._model.most_similar(**(args.dict()))
        return MostSimilarReturnType(
            words=[word for word, _ in list_of_similar_words],
            similarity =[similarity for _, similarity in list_of_similar_words]
        )

class SimilarWordsEmbeddings(BaseModel):
    words: List[str]
    most_similar_words = List[List[str]]
    most_similar_words_embeddings: List[List[np.ndarray]]

    class Config:
        arbitrary_types_allowed = True


def generate_similar_words_embeddings(words: List[str], embedding_model: EmbeddingModelProtocol, topn: int):
    # there's a `topn`-length list for each word above
    word_clusters: List[List[str]] = []
    word_cluster_embeddings: List[List[np.ndarray]] = []
    for word in tqdm(words):
        most_similar_words: List[str] = []
        most_similar_words_embeddings: List[np.ndarray] = []
        most_similar_inputs = MostSimilarSignature(word=word, topn=topn)
        for similar_word, similarity in embedding_model.most_similar(most_similar_inputs):
            most_similar_words.append(similar_word)
            most_similar_words_embeddings.append(embedding_model[similar_word])
        word_cluster_embeddings.append(most_similar_words_embeddings)
        word_clusters.append(most_similar_words)
    return SimilarWordsEmbeddings(
        words=words, 
        most_similar_words=word_clusters, 
        most_similar_words_embeddings=word_cluster_embeddings
    )
