from functools import partial

from PyQt4 import QtGui, QtCore
import collections


class WrapperMetaclass(type):
    def __init__(cls, name, bases, nmspc):
        # TODO: check bases for options and update cls.options
        super().__init__(name, bases, nmspc)

        if 'Meta' in nmspc:
            Meta = nmspc['Meta']
            if getattr(Meta, 'abstract', False):
                return

        cls._option_names = set()
        cls._options = dict()
        for option in cls.options:
            if not isinstance(option, BaseOption):
                raise TypeError('Options should be a BaseOption subclass instance.')
            cls._option_names.add(option.name)
            cls._options[option.name] = option
            setattr(cls, option.name, property(
                fget=partial(WrapperMetaclass.getter, option=option.name),
                fset=partial(WrapperMetaclass.setter, option=option.name)
            ))

    @staticmethod
    def getter(self, option):
        return self.get_option(option).value

    @staticmethod
    def setter(self, value, option):
        self.get_option(option).value = value


class BaseWrapper(metaclass=WrapperMetaclass):
    """Wraps a class and provides a mutable instance.

    Attributes:
        name (str): Human readable name of wrapped object.
        wrapped_class (type): A class that will be wrapped
        wrapped_object (object): An instance of the wrapped class
        options: (List[BaseOption]): A list of options that will be passed
            to `wrapped_class` constructor call.
    """

    name = ''
    wrapped_class = object
    wrapped_object = None
    options = tuple()

    class Meta:
        abstract = True

    def __init__(self, **kwargs):
        # overwrites default values
        for arg, value in kwargs.items():
            if arg in self._option_names:
                setattr(self, arg, value)
            else:
                raise ValueError('Unknown argument `{}`'.format(arg))

        self.apply_changes()

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
        layout = QtGui.QFormLayout(parent)
        for option in self.options:
            layout.addRow(option.verbose_name, option.as_widget(callback=callback))
        layout.setLabelAlignment(QtCore.Qt.AlignRight)
        return layout

    def apply_changes(self):
        # TODO: if no option item mustn't be changed
        kwargs = {opt.name: opt.value for opt in self.options}
        self.validate()
        self.wrapped_object = self.wrapped_class(**kwargs)

    def on_change(self):
        pass

    def validate(self):
        for option in self.options:
            option.validate()

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name

    def get_option(self, name):
        return self._options[name]

    def __getstate__(self):
        state = self.__dict__.copy()
        state['__values'] = {
            option.name: option.value
            for option in self.options
        }
        return state

    def __setstate__(self, newstate):
        values = newstate.pop('__values')
        self.__dict__.update(newstate)
        for name, value in values.items():
            setattr(self, name, value)


class BaseOption:

    def __init__(self, name, default=None, verbose_name=None, validator=None):
        """Option is a proxy between gui and wrapped object.

        Arguments:
            name (str): An option identifier.
            default: A default option value.
            verbose_name (Optional[str]): Human readable description of the option.
            validator (Optional[Callable]): An option values validator.
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

    def as_layout(self, callback=None):
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(self.verbose_name))
        layout.addWidget(self.as_widget(callback))
        return layout

    @property
    def value(self):
        return getattr(self, '_value', self.default)

    @value.setter
    def value(self, value):
        # allows gui temporary invalid state
        # self.validate_value(value)
        self._value = value

    class ValidationError(Exception):
        pass

    def validate_value(self, value):
        if self.validator:
            self.validator(value)

    def validate(self):
        self.validate_value(self.value)

    def on_change(self, value):
        self.value = value
        if self.callback:
            self.callback()

    @staticmethod
    def setter(self, value):
        self._value = value

    @staticmethod
    def getter(self):
        return self._value


class StringOption(BaseOption):
    def __init__(self, name, default=None, verbose_name=None, validator=None, choices=None):
        super().__init__(name, default, verbose_name, validator)

        self.choices = choices
        if self.choices:
            if isinstance(choices[0], str):
                self.choices = choices
                self.choice_values = choices
            else:
                self.choices = [c[0] for c in choices]
                self.choice_values = [c[1] for c in choices]

            if self.default is None:
                self.default = self.choice_values[0]

    def as_widget(self, callback=None):
        self.callback = callback
        if self.choices:
            combo_box = QtGui.QComboBox()
            combo_box.addItems(self.choices)
            combo_box.setCurrentIndex(self.choice_values.index(self.value))

            combo_box.currentIndexChanged.connect(
                    lambda i: self.on_change(self.choice_values[i]))
            return combo_box
        else:
            line = QtGui.QLineEdit()
            line.setText(self.value)
            line.textChanged.connect(self.on_change)
            return line


class BoolOption(BaseOption):
    def __init__(self, name, default=False, verbose_name=None, validator=None):
        super().__init__(name=name, default=default, verbose_name=verbose_name, validator=validator)

    def as_widget(self, callback=None):
        self.callback = callback
        checkbox = QtGui.QCheckBox()
        checkbox.setChecked(self.value)
        checkbox.stateChanged.connect(self.on_change)
        return checkbox


class IntegerOption(BaseOption):
    def __init__(self, name, default=0, verbose_name=None, validator=None, range=(0, 100), step=1):
        super().__init__(name, default, verbose_name, validator)
        self.step = step
        self.range = range

    def as_widget(self, callback=None):
        self.callback = callback
        spin_box = QtGui.QSpinBox()
        spin_box.setRange(*self.range)
        spin_box.setSingleStep(1)
        spin_box.setValue(self.value)
        spin_box.valueChanged.connect(self.on_change)
        return spin_box


class FloatOption(BaseOption):
    def __init__(self, name, default=0., verbose_name=None, validator=None, range=(0, 1), step=.01):
        super().__init__(name, default, verbose_name, validator)
        self.step = step
        self.range = range

    def as_widget(self, callback=None):
        self.callback = callback
        spin_box = QtGui.QDoubleSpinBox()
        spin_box.setRange(*self.range)
        spin_box.setSingleStep(self.step)
        spin_box.setValue(self.value)
        spin_box.valueChanged.connect(self.on_change)
        return spin_box


class RangeOption(BaseOption):
    def __init__(self, name, default=(0., 1.), verbose_name=None,
                 validator=None, range=(0, 1), step=.01, min_size=None):
        super().__init__(name, default, verbose_name, validator)
        self.step = step
        self.range = range
        self.min_size = min_size if min_size else self.step

    def as_widget(self, callback=None):
        self.callback = callback
        group_box = QtGui.QGroupBox()
        group_box.setContentsMargins(0,0, 0, 0)
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)

        layout.setStretch(0, 0)
        lower_bound = QtGui.QDoubleSpinBox()
        lower_bound.setRange(self.range[0], self.value[1])
        lower_bound.setSingleStep(self.step)
        lower_bound.setValue(self.value[0])
        lower_bound.valueChanged.connect(self.lower_bound_changed)

        layout.addWidget(lower_bound)
        self.lower_bound = lower_bound

        upper_bound = QtGui.QDoubleSpinBox()
        upper_bound.setRange(self.value[0], self.range[1])
        upper_bound.setSingleStep(self.step)
        upper_bound.setValue(self.value[1])
        upper_bound.valueChanged.connect(self.upper_bound_changed)
        layout.addWidget(upper_bound)
        self.upper_bound = upper_bound
        group_box.setLayout(layout)
        return group_box

    def lower_bound_changed(self, value):
        self.upper_bound.setMinimum(value + self.min_size)
        self.on_change((self.lower_bound.value(), self.upper_bound.value()))

    def upper_bound_changed(self, value):
        self.lower_bound.setMaximum(value - self.min_size)
        self.on_change((self.lower_bound.value(), self.upper_bound.value()))

    def set_step(self, step):
        self.upper_bound.setSingleStep(step)
        self.lower_bound.setSingleStep(step)
