from PyQt4 import QtGui

from Orange.widgets.widget import OWWidget
from Orange.widgets.settings import Setting
from Orange.widgets import gui
from Orange.data import Table
from orangecontrib.text.corpus import Corpus
from orangecontrib.text.preprocess import Preprocessor
from orangecontrib.text.vectorizer import TfidfVectorizerWrapper, CountVectorizerWrapper
from orangecontrib.text.widgets.components import ComboBox


class Output:
    DATA = "Data"


class OWBagOfWords(OWWidget):
    # Basic widget info
    name = "Bag of Words"
    description = "Generates a bag of words from the input corpus."
    icon = "icons/BagOfWords.svg"
    priority = 40

    # Input/output
    inputs = [("Corpus", Corpus, "set_corpus"),
              ("Preprocessor", Preprocessor, "set_preprocessor")]
    outputs = [(Output.DATA, Table)]
    want_main_area = False

    VECTORIZERS = [CountVectorizerWrapper(), TfidfVectorizerWrapper()]

    vectorizer = Setting(VECTORIZERS[0])

    def __init__(self):
        super().__init__()

        self.corpus = None
        self.preprocessor = Preprocessor()
        self.normalization = None

        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(10)

        # Pre-processing info.
        pp_info_layout = QtGui.QVBoxLayout()

        pp_info_box = gui.widgetBox(self.controlArea, "Pre-processing info",
                                    addSpace=False)
        pp_info_layout.addWidget(pp_info_box)

        pp_info = str(self.preprocessor)

        self.pp_info_label = QtGui.QLabel()
        self.pp_info_label.setWordWrap(True)
        self.pp_info_label.setText(pp_info)

        pp_info_layout.addWidget(self.pp_info_label)

        vbox.addLayout(pp_info_layout)

        combo_box = ComboBox(self.controlArea, items=self.VECTORIZERS,
                             owner=self, attribute='vectorizer', header='Vectorizer',
                             callback=self.configuration_changed)

        self.vectorizers_layout = combo_box.layout
        vbox.addLayout(self.vectorizers_layout)

        button = gui.button(self.controlArea, self, "&Apply", callback=self.apply, default=True)
        vbox.addWidget(button)
        self.layout().insertLayout(1, vbox)

    def set_preprocessor(self, data):
        self.preprocessor = data
        self.vectorizer.preprocessor = self.preprocessor
        self.pp_info_label.setText(str(self.preprocessor))

    def set_corpus(self, data):
        self.corpus = data
        self.apply()

    def apply(self):
        new_table = None
        if self.corpus:
            new_table = self.vectorizer.fit_transform(self.corpus)

        self.send("Data", new_table)

    def configuration_changed(self):
        pass


if __name__ == "__main__":
    a = QtGui.QApplication([])
    ow = OWBagOfWords()
    ow.show()
    a.exec_()
    ow.saveSettings()
