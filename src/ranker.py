from typing import List

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def textrank(documents: List[str], threshold_bias: float = 0.2) -> List[str]:
    """
    Get the most relevant documents from the array of documents
    :param documents: List[str], original array of documents to filter
    :param threshold_bias: float, additional bias for the computed mean document score
    :return: List[str], array of the most relevant documents in the original order
    """
    bow_matrix = CountVectorizer().fit_transform(documents)
    tfidf_matrix = TfidfTransformer().fit_transform(bow_matrix)

    similarity_matrix = tfidf_matrix * tfidf_matrix.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_matrix)
    scores = nx.pagerank(nx_graph)

    document_array = np.asarray(
        sorted(
            ((scores[i], document) for i, document in enumerate(documents)),
            reverse=True,
        )
    )

    f_max = float(document_array[0][0])
    f_min = float(document_array[-1][0])

    # normalize scores
    if f_min == f_max:
        temp_array = [0] * len(document_array)
    else:
        temp_array = [
            (float(score) - f_min) / (f_max - f_min) for score, _ in document_array
        ]

    threshold = (sum(temp_array) / len(temp_array)) + threshold_bias

    # filter documents by score
    document_list = [
        document
        for (_, document), score in zip(document_array, temp_array)
        if score > threshold
    ]

    # restore the original order of documents
    seq_list = [document for document in documents if document in document_list]

    return seq_list
