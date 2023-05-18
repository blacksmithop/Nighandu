import Stemmer
import re
import string


class ProcessText(object):
    STEMMER = Stemmer.Stemmer("english")
    PUNCTUATION = re.compile("[%s]" % re.escape(string.punctuation))
    # top 25 most common words in English and "wikipedia":
    STOPWORDS = set(
        [
            "the",
            "be",
            "to",
            "of",
            "and",
            "a",
            "in",
            "that",
            "have",
            "I",
            "it",
            "for",
            "not",
            "on",
            "with",
            "he",
            "as",
            "you",
            "do",
            "at",
            "this",
            "but",
            "his",
            "by",
            "from",
            "wikipedia",
        ]
    )

    def __init__(self) -> None:
        self._text = ""

    @property
    def text(self):
        """text property"""
        return self._text

    @text.setter
    def text(self, value):
        """text setter"""
        self._text = value

    @text.getter
    def text(self):
        """text getter"""
        return self._text

    def tokenize(self):
        return self.text.split()

    def lowercase_filter(self):
        self.tokens = [token.lower() for token in self.tokenize()]

    def punctuation_filter(self):
        self.tokens = [self.PUNCTUATION.sub("", token) for token in self.tokens]

    def stopword_filter(self):
        self.tokens = [token for token in self.tokens if token not in self.STOPWORDS]

    def stem_filter(self):
        self.tokens = self.STEMMER.stemWords(self.tokens)

    def check_truthiness(self):
        self.tokens = [token for token in self.tokens if token]

    def clean_and_stem(self):
        self.lowercase_filter()
        self.punctuation_filter()
        self.stopword_filter()
        self.check_truthiness()

        return self.tokens
