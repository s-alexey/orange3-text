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


class StringOption(BaseOption):
    def as_widget(self, callback=None):
        self.callback = callback

        line = QtGui.QLineEdit()
        line.setText(self.default)
        line.textChanged.connect(self.on_change)

        return line

    def on_change(self, string):
        setattr(self.owner, self.name, string)
        self.owner.update_configuration()
        if self.callback:
            self.callback()


class BoolOption(BaseOption):
    pass
