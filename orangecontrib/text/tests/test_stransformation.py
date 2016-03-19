import unittest
from orangecontrib.text.string_transformation import BaseStringTransformer, \
    HtmlStringTransformer, WhitespaceStringTransformer, StripAccentsStringTransformer, \
    LowercaseStringTransformer


class BaseStringTransformerTests(unittest.TestCase):
    def test_call(self):

        class ReverseStringTransformer(BaseStringTransformer):
            name = "Reverse"

            def transform(self, string):
                return string[::-1]

        transformer = ReverseStringTransformer()

        self.assertEqual(transformer('abracadabra'), 'arbadacarba')
        self.assertEqual(transformer(['abra', 'cadabra']), ['arba', 'arbadac'])

        self.assertRaises(TypeError, transformer, 1)

    def test_str(self):
        class ReverseStringTransformer(BaseStringTransformer):
            name = 'reverse'

            def transform(self, string):
                return string[::-1]

        transformer = ReverseStringTransformer()

        self.assertIn('reverse', str(transformer))


class LowercaseStringTransformerTests(unittest.TestCase):

    def test_transform(self):
        transformer = LowercaseStringTransformer()
        self.assertEqual(transformer.transform('Abra'), 'abra')
        self.assertEqual(transformer.transform('\u00C0bra'), '\u00E0bra')


class StripAccentsStringTransformerTests(unittest.TestCase):

    def test_transform(self):
        transformer = StripAccentsStringTransformer()
        self.assertEqual(transformer.transform('Abra'), 'Abra')
        self.assertEqual(transformer.transform('\u00C0bra'), 'Abra')


class HtmlStringProcessorTests(unittest.TestCase):

    def test_transform(self):
        transformer = HtmlStringTransformer()
        self.assertEqual(transformer('<p>abra<b>cadabra</b><p>'), 'abracadabra')


class WhitespaceStringProcessorTests(unittest.TestCase):

    def test_transform(self):
        transformer = WhitespaceStringTransformer()
        self.assertEqual(transformer('Hello, \t\t world   !'), 'Hello, world !')
