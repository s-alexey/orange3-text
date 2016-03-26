from nltk.corpus import stopwords

__all__ = [
    "FILTERS", "StopWordsFilter", "LexiconFilter", "HashTagFilter", "UserNameFilter"
]


class BaseTokenFilter:

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

    @property
    def name(self):
        raise NotImplementedError("{} doesn't have name.".format(self.__class__))

    def __str__(self):
        return self.name


class StopWordsFilter(BaseTokenFilter):
    name = 'Stopwords'

    def __init__(self, language=None, stop_words=None):
        # TODO add language and corpus checker
        self.language = language
        self.stop_words = stop_words if stop_words else set()

        if self.language:
            self.stop_words.update(set(stopwords.words(language)))

    def check(self, token):
        return token not in self.stop_words


class LexiconFilter(BaseTokenFilter):
    name = 'Lexicon'

    def __init__(self, vocabulary):
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

FILTERS = [StopWordsFilter('english'), HashTagFilter(), UserNameFilter()]
