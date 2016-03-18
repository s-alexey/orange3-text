import unittest
from orangecontrib.text.preprocess import Preprocessor
from orangecontrib.text.string_transformation import BaseStringTransformer
from orangecontrib.text.token_filtering import BaseTokenFilter, HashTagFilter
from orangecontrib.text.tokenization import BaseTokenizer
from orangecontrib.text.token_normalization import BaseTokenNormalizer, DictionaryLookupNormalizer


class PreprocessTests(unittest.TestCase):
    sentence = "Human machine interface for lab abc computer applications"
    corpus = [
        "Human machine interface for lab abc computer applications",
        "A survey of user opinion of computer system response time",
        "The EPS user interface management system",
        "System and human system engineering testing of EPS",
        "Relation of user perceived response time to error measurement",
        "The generation of random binary unordered trees",
        "The intersection graph of paths in trees",
        "Graph minors IV Widths of trees and well quasi ordering",
        "Graph minors A survey",
    ]

    def test_string_processor(self):
        class StripStringTransformer(BaseStringTransformer):
            @classmethod
            def process(cls, string):
                return string.strip()
        p = Preprocessor(string_processor=StripStringTransformer())

        self.assertEqual(p(' ' + self.sentence + ' \n'), self.sentence)
        self.assertEqual(p([' ' + self.sentence + ' \n']), [self.sentence])

    def test_tokenizer(self):
        class SpaceTokenizer(BaseTokenizer):
            @classmethod
            def tokenize(cls, string):
                return string.split()
        p = Preprocessor(tokenizer=SpaceTokenizer())

        self.assertEqual(p(self.sentence), self.sentence.split())
        self.assertEqual(p(self.corpus), [sent.split() for sent in self.corpus])

    def test_token_normalizer(self):
        class CapTokenNormalizer(BaseTokenNormalizer):
            @classmethod
            def normalize(cls, token):
                return token.capitalize()
        p = Preprocessor(token_normalizer=CapTokenNormalizer())

        self.assertEqual(p(self.sentence), self.sentence.capitalize())
        self.assertEqual(p(self.corpus), [sent.capitalize() for sent in self.corpus])

    def test_token_filter(self):
        class SpaceTokenizer(BaseTokenizer):
            @classmethod
            def tokenize(cls, string):
                return string.split()

        class LengthFilter(BaseTokenFilter):
            @classmethod
            def check(self, token):
                return len(token) <= 3

        htf = LengthFilter()

        p = Preprocessor(tokenizer=SpaceTokenizer(), token_filter=LengthFilter())
        self.assertEqual(p(self.sentence), ['for', 'lab', 'abc'])


