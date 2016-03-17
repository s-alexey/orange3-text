import unittest
from orangecontrib.text.string_transformation import BaseStringTransformer, \
    TextStringTransformer, HtmlStringTransformer, WhitespaceStringTransformer


class BaseStringProcessorTests(unittest.TestCase):
    def test_call(self):

        class ReverseStringTransformer(BaseStringTransformer):
            def process(self, string):
                return string[::-1]

        reverse_processor = ReverseStringTransformer()

        self.assertEqual(reverse_processor('abracadabra'), 'arbadacarba')
        self.assertEqual(reverse_processor(['abra', 'cadabra']), ['arba', 'arbadac'])

        self.assertRaises(TypeError, reverse_processor, 1)


class TextStringProcessorTests(unittest.TestCase):

    def test_process(self):
        processor = TextStringTransformer(lowercase=True, strip_accents=False)
        self.assertEqual(processor.process('Abra'), 'abra')
        self.assertEqual(processor.process('\u00C0bra'), '\u00E0bra')

        processor = TextStringTransformer(lowercase=False, strip_accents=True)
        self.assertEqual(processor.process('Abra'), 'Abra')
        self.assertEqual(processor.process('\u00C0bra'), 'Abra')


class HtmlStringProcessorTests(unittest.TestCase):

    def test_process(self):
        processor = HtmlStringTransformer()
        self.assertEqual(processor('<p>abra<b>cadabra</b><p>'), 'abracadabra')


class WhitespaceStringProcessorTests(unittest.TestCase):

    def test_process(self):
        processor = WhitespaceStringTransformer()
        self.assertEqual(processor('Hello, \t\t world   !'), 'Hello, world !')
