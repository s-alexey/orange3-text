import collections
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

from orangecontrib.text.utils import BaseOption


__all__ = ['StemNormalizer', 'DictionaryLookupNormalizer', 'NORMALIZERS']


class BaseTokenNormalizer:
    def __call__(self, tokens):
        """
        :param tokens: token or collection of token to transform.
        :type tokens: str or Iterable
        :return: str or Iterable
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

    @staticmethod
    def _check_iterable(obj):
        if not isinstance(obj, collections.Iterable):
            raise TypeError("'obj' must be iterable")

    @staticmethod
    def _check_str_type(string):
        if not isinstance(string, str):
            raise TypeError("'string' param must be a string")


class StemNormalizer(BaseTokenNormalizer):
    """ A common class for token normalisation (stemming/lemmatization).
    """
    def __init__(self, normalizer, name='Stemmatizer', options=None):
        """
        :param normalizer: The method that will perform transformation on the tokens.
        :type normalizer: Callable (function or method)
        :param name: The name of the transformation object.
        :type name: verbose method name
        :param options: additional arguments
        """
        self._check_str_type(name)
        self.name = name

        if hasattr(normalizer, 'stem'):
            self.normalizer_cls = normalizer
            self.normalizer = None
        elif not callable(normalizer):
            raise TypeError("normalizer must be callable")
        else:
            self.normalizer_cls = None
            self.normalizer = normalizer

        self.options = options if options else tuple()

        for option in self.options:
            if not isinstance(option, BaseOption):
                raise TypeError('Options should be an BaseOption subclass instance.')
            setattr(self, option.name, option.default)

        self._update_normalizer()

    def _update_normalizer(self):
        if self.normalizer_cls is not None:
            kwargs = {opt.name: getattr(self, opt.name) for opt in self.options}
            self.normalizer = self.normalizer_cls(**kwargs).stem

    def normalize(self, token):
        self._check_str_type(token)
        return self.normalizer(token)

    def __str__(self):
        return self.name


class DictionaryLookupNormalizer(BaseTokenNormalizer):
    """ Normalize token with dictionary (abbreviation, slang and ect.)
    """
    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            raise ValueError("dictionary must be a 'dict' instance.")

        self.dictionary = dictionary

    def normalize(self, token):
        return self.dictionary.get(token, token)


NORMALIZERS = [
    StemNormalizer(PorterStemmer, name='Porter stemmer'),
    StemNormalizer(WordNetLemmatizer().lemmatize, name='WordNet lemmatizer'),
]
