import collections
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import strip_accents_unicode

__all__ = ["TextStringTransformer", "HtmlStringTransformer",
           "WhitespaceStringTransformer"]


class BaseStringTransformer:
    def __call__(self, data):
        """ Transforms strings in given object.
        :param data: string or string collection.
        :type data: str or Iterable
        """
        if isinstance(data, str):
            return self.process(data)
        elif isinstance(data, collections.Iterable):
            return [self.process(string) for string in data]
        raise TypeError("Param 'data' has unknown type.")

    @classmethod
    def process(cls, string):
        """ Process given string.
        :param string: string to transform
        :type string: str
        :return: tranformed string
        """
        raise NotImplementedError("Method 'process' isn't implemented "
                                  "for '{cls}' class".format(cls=cls.__name__))

    @staticmethod
    def _check_str_type(string):
        if not isinstance(string, str):
            raise TypeError("'string' argument must be a string")


class TextStringTransformer(BaseStringTransformer):
    def __init__(self, lowercase=True, strip_accents=False):
        """
        :param lowercase: convert all characters to lowercase.
        :type lowercase: bool
        :param strip_accents: remove accents.
        :type strip_accents: bool
        """
        self.lowercase = lowercase
        self.strip_accents = strip_accents

    def process(self, string):
        if self.lowercase:
            string = string.lower()
        if self.strip_accents:
            string = strip_accents_unicode(string)
        return string


class WhitespaceStringTransformer(BaseStringTransformer):
    """ Substitutes multiple whitespace with single one.
    """
    @classmethod
    def process(cls, string):
        cls._check_str_type(string)
        return re.sub('\s\s+', ' ', string)


class HtmlStringTransformer(BaseStringTransformer):
    """ Removes all tags from string.
    """
    @classmethod
    def process(cls, string):
        cls._check_str_type(string)
        return BeautifulSoup(string, 'html.parser').getText()
