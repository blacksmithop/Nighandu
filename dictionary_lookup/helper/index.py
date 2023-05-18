from .clean import ProcessText
from .definition import Definition
from .loaddata import Data

import pandas as pd
import pickle
from math import log10
from tqdm import tqdm
from os import path


class Engine:
    process = ProcessText()

    def __init__(self, file_path: str = "./dataset/olam-enml.csv"):
        self.index = {}
        self.documents = {}

        self.file_path = file_path

        if not self._check_for_index_cache():
            self._load_data()
            self.index_document()
            self._cache_data()
        else:
            print("Loading indexed dataset from memory")
            self._load_index_cache()

    def _check_for_index_cache(self):
        return path.isfile("./dataset/olam-enml-index.pkl") and path.isfile(
            "./dataset/olam-enml-documents.pkl"
        )

    def _load_index_cache(self):
        with open("./dataset/olam-enml-index.pkl", "rb") as f:
            self.index = pickle.load(f)

        with open("./dataset/olam-enml-documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

    def _cache_data(self):
        with open("./dataset/olam-enml-index.pkl", "wb") as f:
            pickle.dump(self.index, f)

        with open("./dataset/olam-enml-documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def _load_data(self):
        dataframe = Data(file_path=self.file_path)
        self.df = dataframe.load()

    def _index_doc(self, row: pd.Series):
        document = Definition(**row)

        if document.id not in self.documents:
            self.documents[document.id] = document
            document.analyze()

        self.process.text = document.english_word

        for token in self.process.clean_and_stem():
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.id)

    def index_document(self):
        for i in tqdm(range(self.df.shape[0]), desc="Indexing dataset", ascii="░▒█"):
            try:
                self._index_doc(self.df.loc[i])
            except AttributeError:
                continue

    def _results(self, analyzed_query):
        return [self.index.get(token, set()) for token in analyzed_query]

    def document_frequency(self, token):
        return len(self.index.get(token, set()))

    def inverse_document_frequency(self, token):
        """
        Manning, Hinrich and Schütze use log10, so we do too, even though it
        doesn't really matter which log we use anyway
        https://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html
        """
        return log10(len(self.documents) / self.document_frequency(token))

    def search(self, query, search_type="AND", rank=True):
        """
        Boolean search; this will return documents that contain all words from the
        query, but not rank them (sets are fast, but unordered).
        """
        if search_type not in ("AND", "OR"):
            return []

        self.process.text = query

        analyzed_query = self.process.clean_and_stem()
        results = self._results(analyzed_query)
        documents = [self.documents[doc_id] for doc_id in set.intersection(*results)]

        if rank:
            return self.rank(analyzed_query, documents)

        if search_type == "AND":
            # all tokens must be in the document
            documents = [
                self.documents[doc_id] for doc_id in set.intersection(*results)
            ]
        elif search_type == "OR":
            # only one token has to be in the document
            documents = [self.documents[doc_id] for doc_id in set.union(*results)]

        return documents

    def rank(self, analyzed_query, documents):
        results = []
        if not documents:
            return results
        for document in documents:
            #     score = sum([document.term_frequency(token) for token in analyzed_query])
            #     results.append((document, score))
            # return sorted(results, key=lambda doc: doc[1], reverse=True)
            score = 0.0

            for token in analyzed_query:
                tf = document.term_frequency(token)
                idf = self.inverse_document_frequency(token)
                score += tf * idf
            results.append((document, score))

        return sorted(results, key=lambda doc: doc[1], reverse=True)
