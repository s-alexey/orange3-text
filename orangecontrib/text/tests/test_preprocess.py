import unittest
from orangecontrib.text.preprocess import Preprocessor
from orangecontrib.text.string_transformation import BaseStringTransformer, \
    LowercaseStringTransformer
from orangecontrib.text.token_filtering import BaseTokenFilter
from orangecontrib.text.tokenization import BaseTokenizer
from orangecontrib.text.token_normalization import BaseTokenNormalizer


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
    def test_call(self):
        p = Preprocessor()
        self.assertEqual(p(self.sentence), self.sentence)
        self.assertEqual(p(self.corpus), self.corpus)
        self.assertRaises(TypeError, p, 1)

    def test_string_processor(self):
        class StripStringTransformer(BaseStringTransformer):
            @classmethod
            def transform(cls, string):
                return string.strip()
        p = Preprocessor(string_transformers=StripStringTransformer())

        self.assertEqual(p(' ' + self.sentence + ' \n'), self.sentence)
        self.assertEqual(p([' ' + self.sentence + ' \n']), [self.sentence])

        p = Preprocessor(string_transformers=[StripStringTransformer(),
                                              LowercaseStringTransformer()])

        self.assertEqual(p(' ' + self.sentence + ' \n'), self.sentence.lower())
        self.assertEqual(p([' ' + self.sentence + ' \n']), [self.sentence.lower()])

        self.assertRaises(TypeError, Preprocessor, string_transformers=1)

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
            def check(cls, token):
                return len(token) <= 3

        p = Preprocessor(tokenizer=SpaceTokenizer(), token_filters=LengthFilter())
        self.assertEqual(p(self.sentence), ['for', 'lab', 'abc'])


