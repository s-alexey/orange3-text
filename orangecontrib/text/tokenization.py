import re

from nltk import tokenize

from orangecontrib.text.utils import StringOption, BaseWrapper

__all__ = ["NltkTokenizer", "TOKENIZERS"]


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
    tokenizer_cls = None
    tokenizer = None
    name = 'Tokenizer'

    def __init__(self):
        super().__init__()
        self.update_configuration()

    def update_configuration(self):
        if self.tokenizer_cls is not None:
            kwargs = {opt.name: getattr(self, opt.name) for opt in self.options}
            self.tokenizer = self.tokenizer_cls(**kwargs).tokenize

    def tokenize(self, string):
        self._check_str_type(string)
        return self.tokenizer(string)


class WordPunctTokenizer(NltkTokenizer):
    tokenizer_cls = tokenize.WordPunctTokenizer
    name = 'Word & punctuation'


class WhitespaceTokenizer(NltkTokenizer):
    tokenizer_cls = tokenize.WhitespaceTokenizer
    name = 'Whitespace'


class LineTokenizer(NltkTokenizer):
    tokenizer_cls = tokenize.LineTokenizer
    name = 'Line'


def validate_regexp(regexp):
    try:
        re.compile(regexp)
        return True
    except re.error as e:
        raise StringOption.ValidationError(str(e))


class RegexpTokenizer(NltkTokenizer):

    tokenizer_cls = tokenize.RegexpTokenizer
    name = 'Regexp'
    options = (
        StringOption(name='pattern', default='\w+', verbose_name='Pattern',
                     validator=validate_regexp),
    )


class TweetTokenizer(NltkTokenizer):
    tokenizer_cls = tokenize.TweetTokenizer
    name = 'Tweet'


TOKENIZERS = [WordPunctTokenizer(), WhitespaceTokenizer(), RegexpTokenizer(),
              TweetTokenizer(), LineTokenizer()]
