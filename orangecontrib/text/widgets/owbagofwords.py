from PyQt4 import QtGui, QtCore

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

    VECTORIZERS = Setting([CountVectorizerWrapper(), TfidfVectorizerWrapper()])
    vectorizer = Setting(VECTORIZERS.default[0])

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
        self.pp_info_label = QtGui.QLabel()
        self.pp_info_label.setWordWrap(True)
        self.pp_info_label.setText(str(self.preprocessor))
        pp_info_layout.addWidget(self.pp_info_label)

        vbox.addLayout(pp_info_layout)

        # Vectorizer
        combo_box = ComboBox(self.controlArea, items=self.VECTORIZERS,
                             owner=self, attribute='vectorizer', header='Vectorizer',
                             callback=self.configuration_changed)
        vbox.addLayout(combo_box.layout)

        # Apply button
        button = gui.button(self.controlArea, self, "&Apply", callback=self.apply)
        vbox.addWidget(button, 0, QtCore.Qt.AlignTop)

        # Info label
        self.summary_label = QtGui.QLabel()
        vbox.addWidget(self.summary_label)

        self.layout().insertLayout(0, vbox)

    def set_preprocessor(self, data):
        self.preprocessor = data
        self.vectorizer.preprocessor = self.preprocessor
        self.pp_info_label.setText(str(self.preprocessor))

    def set_corpus(self, data):
        self.corpus = data
        self.apply()

    def apply(self):
        self.vectorizer.apply_changes()

        if self.corpus:
            new_table = self.vectorizer.fit_transform(self.corpus)
        else:
            new_table = None

        self.update_summary(new_table)
        self.send(Output.DATA, new_table)

    def update_summary(self, table):
        if table:
            self.summary_label.setText("Table with {n_rows} rows and {n_cols} columns was created"
                                       .format(n_rows=len(table), n_cols=len(table.domain)))
        else:
            self.summary_label.setText("No input corpus.")

    def configuration_changed(self):
        pass


if __name__ == "__main__":
    from orangecontrib.text.tokenization import WordPunctTokenizer
    a = QtGui.QApplication([])
    ow = OWBagOfWords()
    ow.set_preprocessor(Preprocessor(tokenizer=WordPunctTokenizer()))
    ow.set_corpus(Corpus.from_file('bookexcerpts'))
    ow.show()
    a.exec_()
    ow.saveSettings()
