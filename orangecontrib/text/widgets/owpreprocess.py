from PyQt4 import QtGui

from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from orangecontrib.text.preprocess import Preprocessor
from orangecontrib.text.string_transformation import TRANSFORMERS
from orangecontrib.text import tokenization
from orangecontrib.text.token_filtering import FILTERS
from orangecontrib.text.token_normalization import NORMALIZERS
from orangecontrib.text.utils import BaseOption
from orangecontrib.text.widgets.components import CheckList, ComboBox


class Output:
    PREPROCESSOR = "Preprocessor"


class OWPreprocess(OWWidget):
    name = "Preprocess"
    description = "Choose the pre-processing options and return a Preprocessor object."
    icon = "icons/TextPreprocess.svg"
    priority = 30

    outputs = [(Output.PREPROCESSOR, Preprocessor)]
    want_main_area = False

    TOKENIZERS = Setting([
        None, tokenization.WordPunctTokenizer(), tokenization.WhitespaceTokenizer(),
        tokenization.RegexpTokenizer(), tokenization.TweetTokenizer(),
        tokenization.LineTokenizer()
    ])
    NORMALIZERS = Setting([None] + NORMALIZERS)
    TRANSFORMERS = Setting(TRANSFORMERS)
    FILTERS = Setting(FILTERS)

    preprocessor = Setting(Preprocessor())

    def __init__(self):
        super().__init__()

        # gui
        self.setMinimumSize(500, 300)
        vbox = QtGui.QVBoxLayout()

        # Demo
        demo_layout = QtGui.QFormLayout()
        demo_layout.setMargin(10)

        self.line_edit = QtGui.QLineEdit(self.controlArea)
        self.line_edit.setText('Hello, world!')
        demo_layout.addRow("Demo:", self.line_edit)

        self.demo_result = gui.label(self.controlArea, self, "")
        self.line_edit.textChanged.connect(self.demo_changed)
        demo_layout.addRow("Result:", self.demo_result)

        vbox.addLayout(demo_layout)

        # Settings
        settings_layout = QtGui.QHBoxLayout()
        settings_layout.setMargin(10)

        # Transformation
        cl = CheckList(self.controlArea, self.TRANSFORMERS, self.preprocessor, 'string_transformers',
                       header='Text transformation', callback=self.demo_changed)

        settings_layout.addLayout(cl.layout)
        self.transformation_check_list = cl

        # Tokenization
        cb = ComboBox(self.controlArea, self.TOKENIZERS, self.preprocessor, 'tokenizer',
                      header='Tokenization', callback=self.demo_changed)

        settings_layout.addLayout(cb.layout)

        # Filtering
        cl = CheckList(self.controlArea, self.FILTERS, self.preprocessor, 'token_filters',
                       header='Filtering', callback=self.demo_changed)

        settings_layout.addLayout(cl.layout)
        self.filtering_check_list = cl

        # Normalization
        cb = ComboBox(self.controlArea, self.NORMALIZERS, self.preprocessor, 'token_normalizer',
                      header='Normalization', callback=self.demo_changed)
        settings_layout.addLayout(cb.layout)

        vbox.addLayout(settings_layout)

        self.apply_button = gui.button(self.controlArea, self, "&Apply", callback=self.apply)
        vbox.addWidget(self.apply_button)
        vbox.setMargin(10)
        self.layout().insertLayout(1, vbox)
        self.apply()
        self.demo_changed()

    def apply(self):
        self.send(Output.PREPROCESSOR, self.preprocessor)

    def demo_changed(self):
        try:
            self.preprocessor.apply_changes()

            self.demo_result.setText(
                str(self.preprocessor(self.line_edit.text()))
            )
            self.demo_result.setStyleSheet('color: black')
            self.apply_button.setEnabled(True)
        except BaseOption.ValidationError as e:
            self.demo_result.setText(
                'error: ' + str(e)
            )
            self.demo_result.setStyleSheet('color: red')
            self.apply_button.setEnabled(False)


if __name__ == "__main__":
    a = QtGui.QApplication([])
    ow = OWPreprocess()
    ow.show()
    a.exec_()
    ow.saveSettings()
