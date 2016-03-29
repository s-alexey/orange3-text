import os

from nltk.corpus import stopwords

from orangecontrib.text.utils import BaseWrapper, StringOption

__all__ = [
    "FILTERS", "StopwordsFilter", "LexiconFilter", "HashTagFilter", "UserNameFilter"
]


class BaseTokenFilter(BaseWrapper):

    def __call__(self, corpus):
        if len(corpus) == 0:
            return corpus
        if isinstance(corpus[0], str):
            return self.filter(corpus)
        return [self.filter(tokens) for tokens in corpus]

    def filter(self, tokens):
        return list(filter(self.check, tokens))

    def check(self, token):
        raise NotImplementedError("This method isn't implemented yet.")


def nltk_languages():
    return [(file.capitalize(), file) for file in os.listdir(stopwords._get_root())
            if file.islower()]


class StopwordsFilter(BaseTokenFilter):
    name = 'Stopwords'

    options = (
        StringOption('language', 'english', 'Language', choices=nltk_languages()),
    )

    def __init__(self):
        super().__init__()
        self.stopwords = set()

    def update_configuration(self):
        self.stopwords = set(stopwords.words(self.language.lower()))

    def check(self, token):
        return token not in self.stopwords


class LexiconFilter(BaseTokenFilter):
    name = 'Lexicon'

    def __init__(self, vocabulary):
        super().__init__()
        self.vocabulary = vocabulary

    def check(self, token):
        return token in self.vocabulary


class HashTagFilter(BaseTokenFilter):
    name = "Hash tags"

    @classmethod
    def check(cls, token):
        return not token.startswith('#')


class UserNameFilter(BaseTokenFilter):
    name = "User names"

    @classmethod
    def check(cls, token):
        return not token.startswith('@')

FILTERS = [StopwordsFilter(), HashTagFilter(), UserNameFilter()]
