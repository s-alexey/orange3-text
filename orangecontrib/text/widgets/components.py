from PyQt4 import QtGui, QtCore

from Orange.widgets import gui


class CheckList:

    def __init__(self, widget, items, owner, attribute, header='', callback=None):

        self.widget = widget
        self.owner = owner
        self.attribute = attribute
        self.callback = callback

        self.layout = QtGui.QVBoxLayout()
        option_box = gui.widgetBox(self.widget, header, addSpace=False)
        self.layout.addWidget(option_box)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.check_boxes = []

        checked = {item.name: item for item in getattr(self.owner, self.attribute, [])}
        self.items = [(item if item.name not in checked else checked[item.name]) for item in items]

        for item in items:
            check_box = QtGui.QCheckBox(str(item.name))
            check_box.setChecked(item.name in checked)
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

    def __init__(self, widget, items, owner, attribute, header='', callback=None):
        self.owner = owner
        self.attribute = attribute
        self.callback = callback

        if hasattr(self.owner, attribute):
            value = getattr(self.owner, attribute)
            self.selected_item_index = items.index(value) if value in items else 0
        else:
            self.selected_item_index = 0

        self.items = items

        widget_box = gui.widgetBox(widget, header, addSpace=False)

        gui.comboBox(widget_box, self, "selected_item_index", items=self.items,
                     callback=self.item_changed)

        self.options_layout = QtGui.QVBoxLayout()

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(widget_box)
        self.layout.addLayout(self.options_layout)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setEnabled(False)
        self.show_current_item_options()

    def show_current_item_options(self):
        self.clear_layout(self.options_layout)
        item = self.items[self.selected_item_index]
        if item and item.options:
            layout = item.options_layout(callback=self.callback)
            self.options_layout.addLayout(layout)

    def item_changed(self):
        item = self.items[self.selected_item_index]
        setattr(self.owner, self.attribute, item)
        self.show_current_item_options()
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
