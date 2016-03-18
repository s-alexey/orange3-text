import unittest
from orangecontrib.text.token_filtering import BaseTokenFilter


class BaseFilterTests(unittest.TestCase):
    def test_call(self):
        class DigitsFilter(BaseTokenFilter):
            def check(self, token):
                return not token.isdigit()

        df = DigitsFilter()

        self.assertEqual(df(['a', '1']), ['a'])
