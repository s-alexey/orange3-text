import unittest
from orangecontrib.text.token_normalization import NltkStemNormalizer, DictionaryLookupNormalizer, \
    PorterStemmer, SnowballStemmer, FunctionNormalizer
import nltk


class TokenNormalizerTests(unittest.TestCase):

    def setUp(self):
        self.stemmer = nltk.PorterStemmer().stem

    def test_str(self):
        stemmer = PorterStemmer()
        self.assertIn('porter', str(stemmer).lower())

    def test_init_without_stemmer(self):
        with self.assertRaises(TypeError):
            PorterStemmer("not a function")

    def test_call(self):
        word = "Testing"
        tokens = ["Testing", "tokenized", "Sentence"]
        stemmer = PorterStemmer()
        self.assertEqual(stemmer(word), self.stemmer(word))
        self.assertEqual(stemmer(tokens),
                         [self.stemmer(token) for token in tokens])

    def test_function(self):
        stemmer = FunctionNormalizer(lambda x: x[:-1], name='stupid normalizer')
        self.assertEqual(stemmer.normalize('token'), 'toke')

    def test_options(self):
        stemmer = SnowballStemmer()
        self.assertTrue(hasattr(stemmer, 'language'))
        stemmer.language = 'french'
        stemmer.apply_changes()
        token = 'voudrais'
        self.assertEqual(stemmer(token), nltk.SnowballStemmer(language='french').stem(token))

    def test_call_with_bad_input(self):
        stemmer = PorterStemmer()
        self.assertRaises(TypeError, stemmer, 10)


class DictionaryLookupNormalizerTests(unittest.TestCase):

    def test_init(self):
        self.assertRaises(TypeError, DictionaryLookupNormalizer, 'not a dictionary')

    def test_normalize(self):
        dln = DictionaryLookupNormalizer(dictionary={'aka': 'also known as'})
        self.assertEqual(dln.normalize('aka'), 'also known as')
