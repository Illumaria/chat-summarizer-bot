from typing import List

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def textrank(documents: List[str], top_k: int = 10) -> List[int]:
    """
    Get the most relevant documents from the array of documents
    :param documents: List[str], original array of documents to filter
    :param top_k: int, number of relevant documents to return
    :return: List[int], array of the most relevant documents in the original order
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
        score_array = [0.0] * len(document_array)
    else:
        score_array = [
            (float(score) - f_min) / (f_max - f_min) for score, _ in document_array
        ]

    # sort documents by score and get top_k
    document_list = [
        t[0][1]
        for t in sorted(
            zip(document_array, score_array), key=lambda x: x[1], reverse=True
        )
    ][:top_k]

    # restore the original order of documents
    out_indices = [
        i for i, document in enumerate(documents) if document in document_list
    ]

    return out_indices
