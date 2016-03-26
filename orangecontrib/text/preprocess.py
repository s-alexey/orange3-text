import collections

__all__ = ["Preprocessor"]


class Preprocessor:
    """Holds document processing objects
    """
    def __init__(self, string_transformers=None, tokenizer=None,
                 token_normalizer=None, token_filters=None):

        if string_transformers is None:
            self.string_transformers = None
        elif callable(string_transformers):
            self.string_transformers = [string_transformers]
        elif isinstance(string_transformers, collections.Iterable):
            self.string_transformers = string_transformers
        else:
            raise TypeError("Type '{}' not supported.".format(type(string_transformers)))

        if token_filters is None:
            self.token_filters = None
        elif callable(token_filters):
            self.token_filters = [token_filters]
        elif isinstance(token_filters, collections.Iterable):
            self.token_filters = token_filters
        else:
            raise TypeError("Type '{}' is not supported.".format(type(token_filters)))

        self.tokenizer = tokenizer
        self.token_normalizer = token_normalizer

    def __call__(self, data):
        if isinstance(data, str):
            return self.process(data)
        if isinstance(data, collections.Iterable):
            return [self.process(string) for string in data]
        else:
            raise TypeError("Type '{}' is not supported.".format(type(data)))

    def process(self, string):
        if self.string_transformers:
            for transformer in self.string_transformers:
                string = transformer(string)
        if self.tokenizer:
            tokens = self.tokenizer(string)
        else:
            tokens = string
        if self.token_filters:
            for filter in self.token_filters:
                tokens = filter(tokens)
        if self.token_normalizer:
            tokens = self.token_normalizer(tokens)
        return tokens
