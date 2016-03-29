import unittest

from Orange.data import Table
from orangecontrib.text.vectorizer import CountVectorizerWrapper
from orangecontrib.text.corpus import Corpus


class VectorizerTest(unittest.TestCase):

    def test_call(self):
        corpus = Corpus.from_file('bookexcerpts')
        cv = CountVectorizerWrapper()
        transformed = cv(corpus)
        self.assertIsInstance(transformed, Table)
        self.assertEqual(len(corpus), len(transformed))

