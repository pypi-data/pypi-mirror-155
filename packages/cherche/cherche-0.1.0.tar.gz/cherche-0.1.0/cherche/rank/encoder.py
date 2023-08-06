from __future__ import annotations

__all__ = ["Encoder"]

import typing

import numpy as np
from cherche import similarity

from ..similarity import cosine
from .base import Ranker


class Encoder(Ranker):
    """SentenceBert Ranker.

    Parameters
    ----------
    key
        Field identifier of each document.
    on
        Fields to use to match the query to the documents.
    encoder
        Encoding function dedicated to documents and query.
    k
        Number of documents to reorder. The default value is None, i.e. all documents will be
        reordered and returned.
    path
        Path to the file dedicated to storing the embeddings. The ranker will read this file if it
        already exists to load the embeddings and will update it when documents are added.
    similarity
        Similarity measure to compare documents embeddings and query embedding (similarity.cosine
        or similarity.dot).

    Examples
    --------

    >>> from pprint import pprint as print
    >>> from cherche import rank
    >>> from sentence_transformers import SentenceTransformer

    >>> documents = [
    ...    {"id": 0, "title": "Paris", "article": "This town is the capital of France", "author": "Wiki"},
    ...    {"id": 1, "title": "Eiffel tower", "article": "Eiffel tower is based in Paris", "author": "Wiki"},
    ...    {"id": 2, "title": "Montreal", "article": "Montreal is in Canada.", "author": "Wiki"},
    ... ]

    >>> ranker = rank.Encoder(
    ...    encoder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2").encode,
    ...    key = "id",
    ...    on = ["title", "article"],
    ...    k = 2,
    ...    path = "encoder.pkl"
    ... )

    >>> ranker.add(documents=documents)
    Encoder ranker
         key: id
         on: title, article
         k: 2
         similarity: cosine
         embeddings stored at: encoder.pkl

    >>> print(ranker(q="Paris", documents=[{"id": 0}, {"id": 1}, {"id": 2}]))
    [{'id': 0, 'similarity': 0.66051394}, {'id': 1, 'similarity': 0.5142564}]

    >>> print(ranker(q="Paris", documents=documents))
    [{'article': 'This town is the capital of France',
      'author': 'Wiki',
      'id': 0,
      'similarity': 0.66051394,
      'title': 'Paris'},
     {'article': 'Eiffel tower is based in Paris',
      'author': 'Wiki',
      'id': 1,
      'similarity': 0.5142564,
      'title': 'Eiffel tower'}]

    >>> ranker += documents

    >>> print(ranker(q="Paris", documents=[{"id": 0}, {"id": 1}, {"id": 2}]))
    [{'article': 'This town is the capital of France',
      'author': 'Wiki',
      'id': 0,
      'similarity': 0.66051394,
      'title': 'Paris'},
     {'article': 'Eiffel tower is based in Paris',
      'author': 'Wiki',
      'id': 1,
      'similarity': 0.5142564,
      'title': 'Eiffel tower'}]

    """

    def __init__(
        self,
        on: str | list,
        key: str,
        encoder,
        k: int | typing.Optionnal = None,
        path: str | typing.Optionnal = None,
        similarity=cosine,
    ) -> None:
        super().__init__(key=key, on=on, encoder=encoder, k=k, path=path, similarity=similarity)

    def __call__(self, q: str, documents: list, **kwargs) -> list:
        """Encode input query and ranks documents based on the similarity between the query and
        the selected field of the documents.

        Parameters
        ----------
        q
            Input query.
        documents
            List of documents to rank.

        """
        if not documents:
            return []

        emb_q = self.encoder(q) if q not in self.embeddings else self.embeddings[q]
        emb_documents = self._emb_documents(documents=documents)
        return self._rank(
            similarities=self.similarity(emb_q=emb_q, emb_documents=emb_documents),
            documents=documents,
        )
