from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# import nltk
from typing import List

from nltk.tokenize import word_tokenize


def vectorize_text(text):
    # Preprocess your text as needed
    # For example, you can convert to lowercase and tokenize
    text = text.lower()
    tokens = word_tokenize(text)

    # Train Word2Vec model
    model = Word2Vec([tokens], vector_size=20, min_count=1)

    # Get word vectors
    word_vectors = model.wv

    return word_vectors


def reduce_dimensions(word_vectors):
    # Perform dimensionality reduction using t-SNE
    tsne = TSNE()
    vectors_2d = tsne.fit_transform(word_vectors.vectors)

    return vectors_2d


def plot_word2vec(texts: List[str]):
    combined_texts = " ".join(texts)
    word_vectors = vectorize_text(combined_texts)
    vectors_2d = reduce_dimensions(word_vectors)

    x = vectors_2d[:, 0]
    y = vectors_2d[:, 1]

    # Retrieve word labels
    words = word_vectors.index_to_key

    # Plot word vectors with labels
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y)

    for i, word in enumerate(words):
        plt.annotate(word, (x[i], y[i]))

    plt.show()


if __name__ == "__main__":
    # Example usage
    text = "Tesla to recall 1.1 million cars in China over potential safety risks, Chinese regulator says"
    plot_word2vec([text])
