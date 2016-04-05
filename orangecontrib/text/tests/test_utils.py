import unittest

from PyQt4 import QtGui

from orangecontrib.text.utils import StringOption, IntegerOption, \
    BoolOption, FloatOption, RangeOption, BaseWrapper


class TestOptions(unittest.TestCase):

    def setUp(self):
        self.qApp = QtGui.QApplication([])

    def test_as_widget(self):
        class DummyObj:
            def __init__(self, **kwargs):
                pass

        class OptionHandler(BaseWrapper):
            options = (
                StringOption(name='string'),
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
