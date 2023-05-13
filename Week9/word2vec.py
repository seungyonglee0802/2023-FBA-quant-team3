from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

# import nltk
from typing import List


def vectorize_sentences(sentences: List[str], vector_size: int = 20):
    # Preprocess sentences as needed, tokenize, etc.
    tokenized_sentences = [sentence.lower().split() for sentence in sentences]

    # Train Word2Vec model
    model = Word2Vec(tokenized_sentences, vector_size=vector_size, min_count=1)

    vectors = []

    for sentence in tokenized_sentences:
        vector = np.zeros(vector_size)
        for word in sentence:
            vector += model.wv[word]
        vectors.append(vector)

    return vectors


def reduce_dimensions(vectors: List[np.ndarray]):
    # Perform dimensionality reduction using t-SNE
    tsne = TSNE(n_components=2)
    vectors_2d = tsne.fit_transform(np.array(vectors))

    return vectors_2d


def plot_word2vec(sentences: List[str], annotate: bool = True):
    sentence_vectors = vectorize_sentences(sentences)
    vectors_2d = reduce_dimensions(sentence_vectors)

    for i, (x, y) in enumerate(vectors_2d):
        plt.scatter(x, y)
        if annotate:
            plt.annotate(sentences[i], (x, y))
    plt.title("Word2Vec Visualization")
    plt.show()


if __name__ == "__main__":
    # Example usage
    titles = [
        "Tesla to open up Supercharger network to other EVs later this year",
        "Tesla reports better-than-expected earnings",
        "Tesla Is Giving Up On a Right-Hand-Drive Model S and Model X",
        "Tesla's Musk blames bureaucracy for German gigafactory delays",
        "Will self-driving vehicles send Tesla shares into hyperdrive?",
        "Ford CEO Jim Farley Takes on Elon Musk’s Tesla",
    ]
    plot_word2vec(titles)
