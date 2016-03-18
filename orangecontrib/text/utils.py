

class BaseOption:

    def __init__(self, name, default=None, verbose_name=None):
        """
        :param name: option name (should be a valid identifier)
        :param default:
        :param verbose_name:
        """
        if not isinstance(name, str) and not name.isidentifier():
            raise ValueError("'name' should be a valid identifier.")

        self.name = name
        self.default = default
        self.verbose_name = verbose_name if verbose_name else name


class StringOption(BaseOption):
    pass


class BoolOption(BaseOption):
    pass
