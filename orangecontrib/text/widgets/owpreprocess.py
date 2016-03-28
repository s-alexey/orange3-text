from PyQt4 import QtGui

from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from orangecontrib.text.preprocess import Preprocessor
from orangecontrib.text.string_transformation import TRANSFORMERS
from orangecontrib.text.tokenization import TOKENIZERS
from orangecontrib.text.token_filtering import FILTERS
from orangecontrib.text.token_normalization import NORMALIZERS
from orangecontrib.text.utils import BaseOption


class CheckList:

    def __init__(self, widget, items, owner, attribute, header='', callback=None):

        self.widget = widget
        self.items = items
        self.owner = owner
        self.attribute = attribute
        self.callback = callback

        self.layout = QtGui.QVBoxLayout()
        option_box = gui.widgetBox(self.widget, header, addSpace=False)
        self.layout.addWidget(option_box)

        self.check_boxes = []

        for item in items:
            check_box = QtGui.QCheckBox(str(item.name))
            check_box.setChecked(False)
            check_box.stateChanged.connect(self.change_options)
            self.layout.addWidget(check_box)
            self.check_boxes.append(check_box)
            if item.options:
                self.layout.addLayout(item.options_layout(option_box,
                                                          callback=self.callback))

    def change_options(self):
        items = []
        for item, check_box in zip(self.items, self.check_boxes):
            if check_box.isChecked():
                items.append(item)

        setattr(self.owner, self.attribute, items)
        if self.callback:
            self.callback()


class ComboBox:

    selected_item_index = 0

    def __init__(self, widget, items, owner, attribute, header='', callback=None):
        self.items = items
        self.owner = owner
        self.attribute = attribute
        self.callback = callback

        widget_box = gui.widgetBox(widget, header, addSpace=False)

        gui.comboBox(widget_box, self, "selected_item_index", items=self.items,
                     callback=self.item_changed)

        self.options_layout = QtGui.QVBoxLayout()

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(widget_box)
        self.layout.addLayout(self.options_layout)

    def item_changed(self):
        item = self.items[self.selected_item_index]
        setattr(self.owner, self.attribute, item)

        self.clear_layout(self.options_layout)

        if item and item.options:
            layout = item.options_layout(callback=self.callback)
            self.options_layout.addLayout(layout)

        if self.callback:
            self.callback()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())


class Output:
    PREPROCESSOR = "Preprocessor"


class OWPreprocess(OWWidget):
    name = "Preprocess"
    description = "Choose the pre-processing options and return a Preprocessor object."
    icon = "icons/TextPreprocess.svg"
    priority = 30

    outputs = [(Output.PREPROCESSOR, Preprocessor)]
    want_main_area = False

    TOKENIZERS = [None] + TOKENIZERS
    NORMALIZERS = [None] + NORMALIZERS
    TRANSFORMERS = TRANSFORMERS
    FILTERS = FILTERS

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

        button = gui.button(self.controlArea, self, "&Apply", callback=self.apply, default=True)
        vbox.addWidget(button)

        self.layout().insertLayout(1, vbox)
        self.apply()
        self.demo_changed()

    def apply(self):
        self.send(Output.PREPROCESSOR, self.preprocessor)

    def demo_changed(self):
        try:
            if self.preprocessor.tokenizer:
                self.preprocessor.tokenizer.validate()

            self.demo_result.setText(
                str(self.preprocessor(self.line_edit.text()))
            )
            self.demo_result.setStyleSheet('color: black')
        except BaseOption.ValidationError as e:
            self.demo_result.setText(
                'error: ' + str(e)
            )
            self.demo_result.setStyleSheet('color: red')
