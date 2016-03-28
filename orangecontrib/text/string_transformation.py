import collections
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import strip_accents_unicode

from orangecontrib.text.utils import BaseWrapper

__all__ = [
    "HtmlStringTransformer", "WhitespaceStringTransformer",
    "LowercaseStringTransformer", "StripAccentsStringTransformer"
]


class BaseStringTransformer(BaseWrapper):
    def __call__(self, data):
        """Transforms strings in given object.

        Arguments:
            data (str or iterable): Items to transform

        Returns:
            str or list: Transformed items

        """
        if isinstance(data, str):
            return self.transform(data)
        elif isinstance(data, collections.Iterable):
            return [self.transform(string) for string in data]
        raise TypeError("Param 'data' has unknown type.")

    @classmethod
    def transform(cls, string):
        """Process given string.

        Arguments:
            string (str): String to transform

        Returns:
            str: Transformed string

        """
        raise NotImplementedError("Method 'transform' isn't implemented "
                                  "for '{cls}' class".format(cls=cls.__name__))


class LowercaseStringTransformer(BaseStringTransformer):
    """Convert all characters to lowercase.
    """
    name = 'Lowercase'

    @classmethod
    def transform(cls, string):
        cls._check_str_type(string)
        return string.lower()


class StripAccentsStringTransformer(BaseStringTransformer):
    """Remove accents.
    """
    name = "Remove accents"

    @classmethod
    def transform(cls, string):
        cls._check_str_type(string)
        return strip_accents_unicode(string)


class WhitespaceStringTransformer(BaseStringTransformer):
    """Substitutes multiple whitespace with single one.
    """
    name = "Remove multiple spaces"

    @classmethod
    def transform(cls, string):
        cls._check_str_type(string)
        return re.sub('\s\s+', ' ', string)


class HtmlStringTransformer(BaseStringTransformer):
    """Removes all tags from string.
    """
    name = "Parse html"

    @classmethod
    def transform(cls, string):
        cls._check_str_type(string)
        return BeautifulSoup(string, 'html.parser').getText()


TRANSFORMERS = [
    LowercaseStringTransformer(), HtmlStringTransformer(),
    WhitespaceStringTransformer(), StripAccentsStringTransformer()
]
