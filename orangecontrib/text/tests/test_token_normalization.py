import unittest
from orangecontrib.text.token_normalization import StemNormalizer, DictionaryLookupNormalizer
from nltk import PorterStemmer, SnowballStemmer

from orangecontrib.text.utils import StringOption


class TokenNormalizerTests(unittest.TestCase):

    def setUp(self):
        self.stemmer = PorterStemmer().stem

    def test_str(self):
        stemmatizer = StemNormalizer(self.stemmer, name='porter')
        self.assertIn('porter', str(stemmatizer))

    def test_init_without_stemmer(self):
        with self.assertRaises(TypeError):
            StemNormalizer("not a function")

    def test_call(self):
        word = "Testing"
        tokens = ["Testing", "tokenized", "Sentence"]

        stemmer = StemNormalizer(self.stemmer, name='porter')

        self.assertEqual(stemmer(word), self.stemmer(word))

        self.assertEqual(stemmer(tokens),
                         [self.stemmer(token) for token in tokens])

    def test_function(self):
        stemmer = StemNormalizer(lambda x: x[:-1])
        self.assertEqual(stemmer.normalize('token'), 'toke')

    def test_options(self):
        stemmer = StemNormalizer(SnowballStemmer, name='snowball',
                                 options=[StringOption(name='language', default='french')])

        self.assertEqual(getattr(stemmer, 'language', None), 'french')
        token = 'voudrais'
        self.assertEqual(stemmer(token), SnowballStemmer(language='french').stem(token))

    def test_call_with_bad_input(self):
        stemmatizer = StemNormalizer(self.stemmer, name='porter')
        self.assertRaises(TypeError, stemmatizer, 10)


class DictionaryLookupNormalizerTests(unittest.TestCase):

    def test_normalize(self):
        dln = DictionaryLookupNormalizer(dictionary={'aka': 'also known as'})
        self.assertEqual(dln.normalize('aka'), 'also known as')
