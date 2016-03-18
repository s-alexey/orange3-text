import collections


class Preprocessor:
    """ Holds document processing objects
    """
    def __init__(self, string_processor=None, tokenizer=None,
                 token_normalizer=None, token_filter=None):
        self.string_processor = string_processor
        self.tokenizer = tokenizer
        self.token_filter = token_filter
        self.token_normalizer = token_normalizer

    def __call__(self, data):
        if isinstance(data, str):
            return self.preprocess(data)
        if isinstance(data, collections.Iterable):
            return [self.preprocess(string) for string in data]
        else:
            raise TypeError("Type '{}' not supported.".format(type(data)))

    def preprocess(self, string):
        if self.string_processor:
            string = self.string_processor(string)
        if self.tokenizer:
            tokens = self.tokenizer(string)
        else:
            tokens = string
        if self.token_filter:
            tokens = self.token_filter(tokens)
        if self.token_normalizer:
            tokens = self.token_normalizer(tokens)
        return tokens
