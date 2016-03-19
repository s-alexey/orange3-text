import collections

__all__ = ["Preprocessor"]


class Preprocessor:
    """Holds document processing objects
    """
    def __init__(self, string_transformers=None, tokenizer=None,
                 token_normalizer=None, token_filter=None):

        if string_transformers is None:
            self.string_transformers = None
        elif callable(string_transformers):
            self.string_transformers = [string_transformers]
        elif isinstance(string_transformers, collections.Iterable):
            self.string_transformers = string_transformers
        else:
            raise TypeError("Type '{}' not supported.".format(type(string_transformers)))

        self.tokenizer = tokenizer
        self.token_filter = token_filter
        self.token_normalizer = token_normalizer

    def __call__(self, data):
        if isinstance(data, str):
            return self.process(data)
        if isinstance(data, collections.Iterable):
            return [self.process(string) for string in data]
        else:
            raise TypeError("Type '{}' not supported.".format(type(data)))

    def process(self, string):
        if self.string_transformers:
            for transformer in self.string_transformers:
                string = transformer(string)
        if self.tokenizer:
            tokens = self.tokenizer(string)
        else:
            tokens = string
        if self.token_filter:
            tokens = self.token_filter(tokens)
        if self.token_normalizer:
            tokens = self.token_normalizer(tokens)
        return tokens
