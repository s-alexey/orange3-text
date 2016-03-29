from PyQt4 import QtGui, QtCore

from Orange.widgets import gui


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
        self.layout.setAlignment(QtCore.Qt.AlignTop)
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
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setEnabled(False)
        self.item_changed()

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
