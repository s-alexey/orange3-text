import re

from nltk import tokenize

from orangecontrib.text.utils import StringOption, BaseWrapper

__all__ = ["NltkTokenizer", "WordPunctTokenizer", "RegexpTokenizer"
           "WhitespaceTokenizer", "TweetTokenizer", "LineTokenizer"]


class BaseTokenizer(BaseWrapper):
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


class NltkTokenizer(BaseTokenizer):
    """ Holds tokenizer object (nltk.tokenize.api.TokenizeI)
    """
    name = 'Tokenizer'

    @property
    def tokenizer(self):
        return self.wrapped_object

    def __init__(self):
        super().__init__()
        self.apply_changes()

    def tokenize(self, string):
        self._check_str_type(string)
        return self.tokenizer.tokenize(string)


class WordPunctTokenizer(NltkTokenizer):
    wrapped_class = tokenize.WordPunctTokenizer
    name = 'Word & punctuation'


class WhitespaceTokenizer(NltkTokenizer):
    wrapped_class = tokenize.WhitespaceTokenizer
    name = 'Whitespace'


class LineTokenizer(NltkTokenizer):
    wrapped_class = tokenize.LineTokenizer
    name = 'Line'


def validate_regexp(regexp):
    try:
        re.compile(regexp)
        return True
    except re.error as e:
        raise StringOption.ValidationError(str(e))


class RegexpTokenizer(NltkTokenizer):

    wrapped_class = tokenize.RegexpTokenizer
    name = 'Regexp'
    options = (
        StringOption(name='pattern', default='\w+', verbose_name='Pattern',
                     validator=validate_regexp),
    )


class TweetTokenizer(NltkTokenizer):
    wrapped_class = tokenize.TweetTokenizer
    name = 'Tweet'
