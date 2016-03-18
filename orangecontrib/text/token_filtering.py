from nltk.corpus import stopwords

__all__ = ["StopWordsFilter", "VocabularyFilter", "HashTagFilter", "UserNameFilter"]


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


class StopWordsFilter(BaseTokenFilter):

    def __init__(self, language=None, stop_words=None):
        # TODO add language and corpus checker
        self.language = language
        self.stop_words = stop_words if stop_words else set()

        if self.language:
            self.stop_words.update(set(stopwords.words(language)))

    def check(self, token):
        return token not in self.stop_words


class VocabularyFilter(BaseTokenFilter):

    def __init__(self, vocabulary):
        self.vocabulary = vocabulary

    def check(self, token):
        return token in self.vocabulary


class HashTagFilter(BaseTokenFilter):

    @classmethod
    def check(cls, token):
        return not token.startswith('#')


class UserNameFilter(BaseTokenFilter):

    @classmethod
    def check(cls, token):
        return not token.startswith('@')
