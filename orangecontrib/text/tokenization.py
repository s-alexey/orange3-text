import collections
from nltk import tokenize

from orangecontrib.text.utils import StringOption, BaseOption

__all__ = ["NltkTokenizer", "TOKENIZERS"]


class BaseTokenizer:
    """ Splits given string into sequence (tuple) of tokens.
    """
    def __call__(self, sent):
        if isinstance(sent, str):
            return self.tokenize(sent)
        return self.tokenize_sents(sent)

    @classmethod
    def tokenize(cls, string):
        raise NotImplementedError("Method 'tokenize' isn't implemented "
                                  "for '{cls}' class".format(cls=cls.__name__))

    def tokenize_sents(self, strings):
        self._check_iterable(strings)
        return [self.tokenize(string) for string in strings]

    @staticmethod
    def _check_iterable(obj):
        if not isinstance(obj, collections.Iterable):
            raise TypeError("'obj' must be iterable")

    @staticmethod
    def _check_str_type(string):
        if not isinstance(string, str):
            raise TypeError("'string' param must be a string")


class NltkTokenizer(BaseTokenizer):
    """ Holds tokenizer object (nltk.tokenize.api.TokenizeI)
    """
    def __init__(self, tokenizer, name="Tokenizer", options=None):
        """
        :param tokenizer: nltk tokenizer class or tokenize-function
        :type tokenizer: nltk.tokenize.api.TokenizeI or function
        :param name: verbose tokenizer name
        :type name: str
        :param options: options to given tokenizer
        :return:
        """
        self._check_str_type(name)
        self.name = name

        if hasattr(tokenizer, 'tokenize'):
            self.tokenizer_cls = tokenizer
            self.tokenizer = None
        elif callable(tokenizer):
            self.tokenizer_cls = None
            self.tokenizer = tokenizer

        self.options = options if options else tuple()

        for option in self.options:
            if not isinstance(option, BaseOption):
                raise TypeError('Options should be an BaseOption subclass instance.')
            setattr(self, option.name, option.default)

        self._update_tokenizer()

    def _update_tokenizer(self):
        if self.tokenizer_cls is not None:
            kwargs = {opt.name: getattr(self, opt.name) for opt in self.options}
            self.tokenizer = self.tokenizer_cls(**kwargs).tokenize

    def tokenize(self, string):
        self._check_str_type(string)
        return self.tokenizer(string)

    def __str__(self):
        return self.name


TOKENIZERS = [
    ('Word & punctuation', tokenize.WordPunctTokenizer, None),
    ('Space', tokenize.SpaceTokenizer, None),
    ('Line', tokenize.LineTokenizer, None),
    ('Regex', tokenize.RegexpTokenizer,
     [StringOption(name='pattern', default='\w+', verbose_name='Pattern')]),
    ('Tweet', tokenize.TweetTokenizer, None),
    ('Blank line', tokenize.BlanklineTokenizer, None),
]

TOKENIZERS = list(NltkTokenizer(tokenizer, name, options)
                  for name, tokenizer, options in TOKENIZERS)
