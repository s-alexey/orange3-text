import unittest
from orangecontrib.text.tokenization import BaseTokenizer, NltkTokenizer, \
    RegexpTokenizer, validate_regexp

from nltk import tokenize

from orangecontrib.text.utils import BaseOption


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

    def test_tokenizer_instance(self):
        class WhitespaceTokenizer(NltkTokenizer):
            tokenizer_cls = tokenize.WhitespaceTokenizer
            name = 'whitespace'

        tokenizer = WhitespaceTokenizer()

        sent = "Test \t tokenizer"
        self.assertEqual(tokenizer.tokenize(sent),
                         tokenize.WhitespaceTokenizer().tokenize(sent))

    def test_options(self):
        tokenizer = RegexpTokenizer()
        self.assertTrue(hasattr(tokenizer, 'pattern'))
        tokenizer.pattern = r'\w+'
        tokenizer.update_configuration()
        sent = "Test tokenizer ."
        self.assertEqual(tokenizer.tokenize(sent), ['Test', 'tokenizer'])

    def test_call_with_bad_input(self):
        tokenizer = RegexpTokenizer()
        self.assertRaises(TypeError, tokenizer.tokenize, 1)
        self.assertRaises(TypeError, tokenizer.tokenize, ['1', 2])


class TestRegexpValidator(unittest.TestCase):
    def test_valid_regexp(self):
        self.assertTrue(validate_regexp('\w+'))

    def test_ivalid_regext(self):
        self.assertRaises(BaseOption.ValidationError, validate_regexp, '\\')
        self.assertRaises(BaseOption.ValidationError, validate_regexp, '[')
        self.assertRaises(BaseOption.ValidationError, validate_regexp, ')?')