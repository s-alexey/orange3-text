import collections
from nltk import stem

from orangecontrib.text.utils import BaseWrapper, StringOption

__all__ = ['NltkStemNormalizer', 'DictionaryLookupNormalizer', 'NORMALIZERS']


class BaseTokenNormalizer(BaseWrapper):
    def __call__(self, tokens):
        """Normalizes given tokens.
        """
        if isinstance(tokens, str):
            return self.normalize(tokens)
        elif isinstance(tokens, collections.Iterable):
            return [self.normalize(token) for token in tokens]
        else:
            raise TypeError("Type {} is not supported.".format(type(tokens)))

    @classmethod
    def normalize(cls, token):
        raise NotImplementedError("Class '{name}' doesn't implement method "
                                  "'normalize'".format(name=cls.__name__))


class FunctionNormalizer(BaseTokenNormalizer):

    def __init__(self, function, name):
        super().__init__()
        self.function = function
        self.name = name

    def normalize(self, token):
        return self.function(token)


class DictionaryLookupNormalizer(BaseTokenNormalizer):
    """ Normalize token with dictionary (abbreviation, slang and ect.)
    """
    def __init__(self, dictionary):
        super().__init__()
        if not isinstance(dictionary, dict):
            raise TypeError("dictionary must be a 'dict' instance.")

        self.dictionary = dictionary

    def normalize(self, token):
        return self.dictionary.get(token, token)


class NltkStemNormalizer(BaseTokenNormalizer):
    """ A common class for token stemming (nltk.stem).
    """
    name = "Stemmer"
    wrapped_class = None

    @property
    def normalizer(self):
        return self.wrapped_object

    def normalize(self, token):
        self._check_str_type(token)
        return self.normalizer.stem(token)


class PorterStemmer(NltkStemNormalizer):

    name = "Porter stemmer"
    wrapped_class = stem.PorterStemmer


class SnowballStemmer(NltkStemNormalizer):

    name = "Snowball stemmer"
    wrapped_class = stem.SnowballStemmer
    options = (
        StringOption(name="language", default="english", verbose_name="Language",
                     choices=stem.SnowballStemmer.languages),
    )


NORMALIZERS = [
    PorterStemmer(), SnowballStemmer(),
    FunctionNormalizer(stem.WordNetLemmatizer().lemmatize, name='WordNet lemmatizer'),
]
