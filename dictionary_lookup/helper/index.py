from .clean import ProcessText
from .definition import Definition
import pandas as pd
from math import log10
from tqdm import tqdm


class Index:
    process = ProcessText()

    def __init__(self):
        self.index = {}
        self.documents = {}

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

    def index_document(self, df: pd.DataFrame):
        for i in tqdm(range(df.shape[0]), desc='Indexing dataset', ascii="░▒█"):
            try:
                self._index_doc(df.loc[i])
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

    def search(self, query, search_type='AND', rank=True):
        """
        Boolean search; this will return documents that contain all words from the
        query, but not rank them (sets are fast, but unordered).
        """
        if search_type not in ('AND', 'OR'):
            return []
        
        self.process.text = query

        analyzed_query = self.process.clean_and_stem()
        results = self._results(analyzed_query)
        documents = [self.documents[doc_id] for doc_id in set.intersection(*results)]
        
        if rank:
            return self.rank(analyzed_query, documents)
    
        if search_type == 'AND':
            # all tokens must be in the document
            documents = [self.documents[doc_id] for doc_id in set.intersection(*results)]
        elif search_type == 'OR':
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