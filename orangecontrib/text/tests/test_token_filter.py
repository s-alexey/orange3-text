import unittest
from orangecontrib.text.token_filtering import BaseTokenFilter, StopwordsFilter, HashTagFilter, UserNameFilter, \
    LexiconFilter


class BaseFilterTests(unittest.TestCase):
    def test_call(self):
        class DigitsFilter(BaseTokenFilter):
            def check(self, token):
                return not token.isdigit()

        df = DigitsFilter()

        self.assertEqual(df([]), [])
        self.assertEqual(df(['a', '1']), ['a'])
        self.assertEqual(df([['a', '1']]), [['a']])


class TestFilters(unittest.TestCase):

    def test_stopwords(self):
        filter = StopwordsFilter()
        filter.language = 'english'
        filter.apply_changes()

        self.assertFalse(filter.check('a'))
        self.assertTrue(filter.check('filter'))

    def test_hashtag(self):
        filter = HashTagFilter()
        self.assertFalse(filter.check('#filter'))
        self.assertTrue(filter.check('filter'))

    def test_username(self):
        filter = UserNameFilter()
        self.assertFalse(filter.check('@filter'))
        self.assertTrue(filter.check('filter'))

    def test_lexicon(self):
        filter = LexiconFilter(['filter'])
        self.assertFalse(filter.check('false'))
        self.assertTrue(filter.check('filter'))
