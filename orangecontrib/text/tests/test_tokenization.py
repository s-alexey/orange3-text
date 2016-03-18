import unittest
from orangecontrib.text.tokenization import BaseTokenizer, NltkTokenizer
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer, sent_tokenize

from orangecontrib.text.utils import StringOption


class BaseTokenizerTests(unittest.TestCase):
    def test_call(self):
        class DashTokenizer(BaseTokenizer):
            @classmethod
            def tokenize(cls, string):
                return string.split('-')

        tokenizer = DashTokenizer()
        self.assertEqual(list(tokenizer('dashed-sentence')), ['dashed', 'sentence'])
        self.assertEqual(list(tokenizer(['1-2-3', '-'])), [['1', '2', '3'], ['', '']])

        self.assertRaises(TypeError, tokenizer, 1)


class NltkTokenizerTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_str(self):
        tokenizer = NltkTokenizer(WhitespaceTokenizer, name='Space')
        self.assertIn('space', str(tokenizer).lower())

    def test_tokenizer_instance(self):
        tokenizer = NltkTokenizer(WhitespaceTokenizer, name='Space')
        sent = "Test \t tokenizer"
        self.assertEqual(tokenizer.tokenize(sent), WhitespaceTokenizer().tokenize(sent))

    def test_stem_function(self):
        tokenizer = NltkTokenizer(sent_tokenize, name='sent')
        sent = "Test tokenizer."
        self.assertEqual(tokenizer.tokenize(sent), sent_tokenize(sent))

    def test_options(self):
        tokenizer = NltkTokenizer(RegexpTokenizer, name='regex',
                                  options=[StringOption(name='pattern', default='\w+')])
        sent = "Test tokenizer ."
        self.assertEqual(tokenizer.tokenize(sent), ['Test', 'tokenizer'])
        self.assertTrue(hasattr(tokenizer, 'pattern'))

    def test_call_with_bad_input(self):
        tokenizer = NltkTokenizer(WhitespaceTokenizer, name='Space')
        self.assertRaises(TypeError, tokenizer.tokenize, 1)
        self.assertRaises(TypeError, tokenizer.tokenize, ['1', 2])
