from PyQt4 import QtCore, QtGui

from Orange.widgets.widget import OWWidget
from Orange.widgets.settings import Setting
from Orange.widgets import gui
from orangecontrib.text.preprocess import Preprocessor
from orangecontrib.text.string_transformation import TRANSFORMERS
from orangecontrib.text.tokenization import TOKENIZERS
from orangecontrib.text.token_filtering import *
from orangecontrib.text.token_normalization import NORMALIZERS
from orangecontrib.text.utils import StringOption


class Output:
    PREPROCESSOR = "Preprocessor"


class OWPreprocess(OWWidget):
    name = "Preprocess"
    description = "Choose the pre-processing options and return a Preprocessor object."
    icon = "icons/TextPreprocess.svg"
    priority = 30

    outputs = [(Output.PREPROCESSOR, Preprocessor)]
    want_main_area = False

    tokenizer_ind = Setting(0)
    TOKENIZERS = [None] + TOKENIZERS

    filter_ind = Setting(0)
    FILTERS = [
        ('None', None),
        ('Stop Words', StopWordsFilter('english')),
        ('Hash tag', HashTagFilter()),
    ]

    normalizer_ind = Setting(0)
    NORMALIZERS = [None] + NORMALIZERS

    TRANSFORMERS = TRANSFORMERS

    def __init__(self):

        super().__init__()

        self.preprocessor = Preprocessor()

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
        self.transformers = set()
        self.preprocessor.string_processor = self.transformers

        transformation_layout = QtGui.QVBoxLayout()
        transformation_box = gui.widgetBox(self.controlArea, "Text transformation",
                                           addSpace=False)
        transformation_layout.addWidget(transformation_box)
        for transformer in self.TRANSFORMERS:
            check_box = QtGui.QCheckBox(str(transformer.name))
            check_box.setChecked(False)
            check_box.stateChanged.connect(lambda: self.change_transformers(transformer))
            transformation_layout.addWidget(check_box)

        settings_layout.addLayout(transformation_layout)

        # Tokenization
        self.tokenizer = None
        tokenization_box = gui.widgetBox(self.controlArea, "Tokenization", addSpace=False)

        combo_box = gui.comboBox(tokenization_box, self, "tokenizer_ind", items=self.TOKENIZERS,
                                 callback=self.tokenizer_changed)
        # self.tokenizer_options = QtGui.QBoxLayout(0)
        self.tokenizer_option_box = gui.widgetBox(tokenization_box)
        self.tokenizer_options = []

        settings_layout.addWidget(tokenization_box)

        # Filtering
        self.filter = None
        filtering_box = gui.widgetBox(self.controlArea, "Filtering",
                                         addSpace=False)
        combo_box = gui.comboBox(filtering_box, self, "filter_ind", items=self.FILTERS,
                                 callback=self.filter_changed)
        settings_layout.addWidget(filtering_box)

        # Normalization
        self.normalizer = None
        normalization_box = gui.widgetBox(self.controlArea, "Normalization", addSpace=False)
        settings_layout.addWidget(normalization_box)

        combo_box = gui.comboBox(normalization_box, self, "normalizer_ind", items=self.NORMALIZERS,
                                 callback=self.normalizer_changed)

        vbox.addLayout(settings_layout)

        button = gui.button(self.controlArea, self, "&Apply", callback=self.apply, default=True)
        vbox.addWidget(button)

        self.layout().insertLayout(1, vbox)
        self.apply()

    def change_transformers(self, transformer):
        if transformer in self.transformers:
            self.transformers.remove(transformer)
        else:
            self.transformers.add(transformer)

    def tokenizer_changed(self):
        self.tokenizer = self.TOKENIZERS[self.tokenizer_ind]
        self.preprocessor.tokenizer = self.tokenizer
        self.clear_options(self.tokenizer_options)
        self.tokenizer_options = []
        if self.tokenizer:
            if self.tokenizer.options:
                for option in self.tokenizer.options:
                    if isinstance(option, StringOption):
                        lab = gui.lineEdit(self.tokenizer_option_box, self.tokenizer,
                                           option.name)
                        lab.setPlaceholderText(option.verbose_name)
                        self.tokenizer_options.append(lab)

        self.demo_changed()

    def filter_changed(self):
        self.filter = self.FILTERS[self.filter_ind][1]
        self.preprocessor.token_filter = self.filter
        self.demo_changed()

    def normalizer_changed(self):
        self.normalizer = self.NORMALIZERS[self.normalizer_ind]
        self.preprocessor.token_normalizer = self.normalizer
        self.demo_changed()

    def apply(self):
        self.send(Output.PREPROCESSOR, self.preprocessor)

    def demo_changed(self, **args):
        self.demo_result.setText(
            str(self.preprocessor(self.line_edit.text()))
        )

    def clear_options(self, option_list):
        for option_widget in option_list:
            option_widget.setParent(None)
            option_widget.deleteLater()
