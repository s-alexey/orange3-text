from PyQt4 import QtGui
import collections


class BaseWrapper:
    name = ''
    options = tuple()

    def __init__(self):
        self.options = self.options
        for option in self.options:
            if not isinstance(option, BaseOption):
                raise TypeError('Options should be a BaseOption subclass instance.')
            setattr(self, option.name, option.default)
            option.set_owner(self)

        self.update_configuration()

    @staticmethod
    def _check_iterable(obj):
        if not isinstance(obj, collections.Iterable):
            raise TypeError("'obj' must be iterable")

    @staticmethod
    def _check_str_type(string):
        if not isinstance(string, str):
            raise TypeError("'string' param must be a string")

    def __str__(self):
        return self.name

    def options_layout(self, parent=None, callback=None):
        layout = QtGui.QVBoxLayout(parent)
        for option in self.options:
            layout.addWidget(option.as_widget(callback=callback))

        return layout

    def update_configuration(self):
        pass

    def on_change(self):
        pass

    def validate(self):
        for option in self.options:
            option.validate()


class BaseOption:

    def __init__(self, name, default=None, verbose_name=None, validator=None):
        """
        :param name: option name (should be a valid identifier)
        :param default:
        :param verbose_name:
        """
        if not isinstance(name, str) and not name.isidentifier():
            raise ValueError("'name' should be a valid identifier.")

        self.owner = None
        self.name = name
        self.default = default
        self.verbose_name = verbose_name if verbose_name else name
        self.validator = validator
        self.callback = None

    def as_widget(self, callback=None):
        raise NotImplementedError()

    def set_owner(self, owner):
        self.owner = owner

    class ValidationError(Exception):
        pass

    def validate(self):
        if self.validator:
            self.validator(getattr(self.owner, self.name))

    def on_change(self, string):
        setattr(self.owner, self.name, string)
        self.owner.update_configuration()
        if self.callback:
            self.callback()


class StringOption(BaseOption):
    def __init__(self, name, default=None, verbose_name=None, validator=None, choices=None):
        super().__init__(name, default, verbose_name, validator)
        if choices:
            if isinstance(choices[0], str):
                self.choices = choices
                self.choice_values = choices
            else:
                self.choices = [c[0] for c in choices]
                self.choice_values = [c[1] for c in choices]

    def as_widget(self, callback=None):
        self.callback = callback
        if self.choices:
            combo_box = QtGui.QComboBox()
            combo_box.addItems(self.choices)
            combo_box.setCurrentIndex(self.choice_values.index(self.default))

            combo_box.currentIndexChanged.connect(self.selected_choice_changed)
            return combo_box
        else:
            line = QtGui.QLineEdit()
            line.setText(self.default)
            line.textChanged.connect(self.on_change)

            return line

    def selected_choice_changed(self, i):
        self.on_change(self.choice_values[i])


class BoolOption(BaseOption):
    def as_widget(self, callback=None):
        self.callback = callback
        checkbox = QtGui.QCheckBox(self.verbose_name)
        if callback:
            checkbox.stateChanged.connect(self.on_change)
        return checkbox


class IntegerOption(BaseOption):
    def __init__(self, name, default=None, verbose_name=None, validator=None, range=(0, 100), step=1):
        super().__init__(name, default, verbose_name, validator)
        self.step = step
        self.range = range

    def as_widget(self, callback=None):
        self.callback = callback

        spin_box = QtGui.QSpinBox()
        spin_box.setRange(*self.range)
        spin_box.setSingleStep(1)
        spin_box.setValue(self.default)
        spin_box.valueChanged.connect(self.on_change)
        return spin_box


class FloatOption(BaseOption):
    def __init__(self, name, default=None, verbose_name=None, validator=None, range=(0, 1), step=.1):
        super().__init__(name, default, verbose_name, validator)
        self.step = step
        self.range = range

    def as_widget(self, callback=None):
        self.callback = callback
        spin_box = QtGui.QDoubleSpinBox()
        spin_box.setRange(*self.range)
        spin_box.setSingleStep(self.step)
        spin_box.setValue(self.default)
        spin_box.valueChanged.connect(self.on_change)
        return spin_box