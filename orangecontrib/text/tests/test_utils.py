import pickle
import tempfile
import unittest

from PyQt4 import QtGui

from orangecontrib.text.utils import StringOption, IntegerOption, \
    BoolOption, FloatOption, RangeOption, BaseWrapper, BaseOption


class DumpObj:
    def __init__(self, *args, **kwargs):
        pass




class TestMetaclass(unittest.TestCase):

    def test_options_are_properties(self):
        class Wrapper(BaseWrapper):
            options = (
                StringOption(name='string'),
                BoolOption(name='boolean'),
                IntegerOption(name='integer'),
                FloatOption(name='fl'),
                RangeOption(name='range'),
            )
            wrapped_class = DumpObj

        self.assertIsInstance(Wrapper.string, property)
        self.assertIsInstance(Wrapper.boolean, property)
        self.assertIsInstance(Wrapper.integer, property)
        self.assertIsInstance(Wrapper.fl, property)
        self.assertIsInstance(Wrapper.range, property)

    def test_set_option(self):
        class Wrapper(BaseWrapper):
            options = (
                StringOption(name='string'),
            )
            wrapped_class = DumpObj

        w = Wrapper()
        w.string = 'test'
        self.assertEqual(w.get_option('string').value, 'test')

        w.get_option('string').value = 'new value'
        self.assertEqual(w.get_option('string').value, 'new value')

    def test_bad_option(self):
        with self.assertRaises(TypeError):
            class BadWrapper(BaseWrapper):
                options = (
                    1, 1
                )


class TestWrapper(unittest.TestCase):

    def test_init(self):
        class Wrapper(BaseWrapper):
            options = (
                IntegerOption(name='int_value'),
            )
            wrapped_class = DumpObj

        w = Wrapper(int_value=5)
        self.assertEqual(w.int_value, 5)

        self.assertRaises(ValueError, Wrapper, unknown_value=0)

    def test_validation(self):
        def positive_validator(value):
            if value < 0:
                raise FloatOption.ValidationError

        class Wrapper(BaseWrapper):
            options = (
                FloatOption(name='fl', validator=positive_validator),
            )
            wrapped_class = DumpObj
        w = Wrapper()
        w.fl = -1
        with self.assertRaises(BaseOption.ValidationError):
            w.apply_changes()

    class Wrapper(BaseWrapper):
        options = (
            StringOption(name='string'),
        )
        wrapped_class = DumpObj

    def test_pickle(self):
        # to be pickled Wrapper should be a global object
        item = TestWrapper.Wrapper()
        item.string = 'value'
        temp_file = tempfile.TemporaryFile()
        pickle.dump({"setting": item}, temp_file, -1)

        item.string = 'new value'

        temp_file.seek(0)
        loaded = pickle.load(temp_file)
        loaded_item = loaded['setting']
        self.assertEqual(item, loaded_item)
        self.assertEqual(loaded_item.string, 'value')


class TestOptions(unittest.TestCase):

    def setUp(self):
        self.qApp = QtGui.QApplication([], True)

    def test_as_widget(self):
        class DummyObj:
            def __init__(self, **kwargs):
                pass

        class OptionHandler(BaseWrapper):
            options = (
                StringOption(name='string'),
                StringOption(name='string', choices=(('first', '1'), ('second', '2'))),
                BoolOption(name='boolean'),
                IntegerOption(name='integer'),
                FloatOption(name='fl'),
                RangeOption(name='range'),
            )
            wrapped_class = DummyObj

        handler = OptionHandler()
        for option in handler.options:
            w = option.as_widget()
            self.assertIsInstance(w, QtGui.QWidget)
