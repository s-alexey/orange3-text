import collections

__all__ = ["Preprocessor"]


class Preprocessor:
    """Holds document processing objects

    Attributes:
        string_transformers (List([BaseStringTransformer]): transforms strings
        tokenizer (BaseTokenizer): tokenizes string
        token_normalizer (BaseNormalizer): normalizes tokens
        token_filters (List[BaseTokenFilter]): filters unneeded tokens
    """

    def __init__(self, string_transformers=None, tokenizer=None,
                 token_normalizer=None, token_filters=None):

        if callable(string_transformers):
            string_transformers = [string_transformers]
        if callable(token_filters):
            token_filters = [token_filters]

        if isinstance(string_transformers, collections.Iterable) \
                or string_transformers is None:
            self.string_transformers = string_transformers or []
        else:
            raise TypeError("Unknown type '{}' for string transformers."
                            .format(type(string_transformers)))

        if isinstance(token_filters, collections.Iterable) \
                or token_filters is None:
            self.token_filters = token_filters or []
        else:
            raise TypeError("Unknown Type '{}' for token filters."
                            .format(type(token_filters)))

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

    def __str__(self):
        return '\n'.join([
            "Transformers: " + ', '.join(str(tr) for tr in self.string_transformers),
            "Tokenizer: " + str(self.tokenizer),
            "Filters: " + ', '.join(str(f) for f in self.token_filters),
            "Normalizer: " + str(self.token_normalizer),
        ])

    def apply_changes(self):
        for transformer in self.string_transformers:
            transformer.apply_changes()
        if self.tokenizer:
            self.tokenizer.apply_changes()
        if self.token_normalizer:
            self.token_normalizer.apply_changes()
        for filter in self.token_filters:
            filter.apply_changes()
