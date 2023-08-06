"""A PyBabelNet utility module. Mainly for internal use."""

import unicodedata
from functools import total_ordering
from typing import Optional, Sequence

import text_unidecode


class UnsupportedOnlineError(RuntimeError):
    """Exception raised when is used a feature unavailable in the online API"""
    pass


def comparator(cls):
    """Decorator that turns a class in a Java style comparator, in
    order to use inheritance and custom arguments for sorting.
    The class needs to declare a compare(obj1, obj2) method that returns an int.
    """

    def on_call(self1, *args):
        @total_ordering
        class K:
            def __init__(self, obj):
                """init method"""
                self.obj = obj

            def __eq__(self, other):
                return self1.compare(self.obj, other.obj) == 0

            def __lt__(self, other):
                return self1.compare(self.obj, other.obj) < 0

        return K(args[0])

    cls.__call__ = on_call
    return cls


# def ordinal(cls):
#     """Enum decorator that adds an ordinal property, specifying the
#     order of the name."""
#
#     cls.ordinal = property(lambda self: list(cls).index(self))
#     return cls


def flatten_to_ascii(string: str) -> str:
    """Transliterate input string to ascii.

    @param string: The input string.
    @type string: str

    @return: str
    @rtype: str
    """
    return text_unidecode.unidecode(string).strip()


def flatten_to_ascii_light(string: str) -> Optional[str]:
    """Transliterate input string to ascii using unicodedata.

    @param string: The input string.
    @type string: str

    @return: the flattened version of the input string
    @rtype: Optional[str]
    """
    outstring = "".join(
        (
            c
            for c in unicodedata.normalize("NFD", string.strip())
            if unicodedata.category(c) != "Mn"
        )
    )
    if outstring.lower() == string.lower():
        return None
    if len(outstring) != len(string):
        return None
    return outstring


def lemma_to_string(lemma: str) -> str:
    """Cleans up a full lemma. It filters the input by removing the annotations inside the parenthesis at
    the end of the lemma (if present)

    @param lemma: the input lemma
    @type lemma: str

    @return: the simple string
    @rtype: str
    """
    # sets the simpleLemma field
    if "(" in lemma and lemma.endswith(")"):
        idx = lemma.index("(")
        if lemma[idx - 1] == "_":
            return lemma[: idx - 1]
        else:
            # this is to handle malformed titles like e.g. 'Comber(fish)'
            return lemma[:idx]
    else:
        return lemma


def normalized_lemma_to_string(lemma: str) -> str:
    """Normalizes a full lemma. It filters the input by removing the annotations inside the parenthesis at the
    end of the lemma (if present) and converts it to lowercase.

    @param lemma: the input simpleLemma
    @type lemma: str

    @return: the string
    @rtype: str

    """
    return lemma_to_string(lemma.lower())


def cmp(a, b):
    """Old school comparator function.
    @param a: the first object to compare
    @param b: the second object to compare
    """
    return (a > b) - (a < b)


def java_split(string: str, char: str) -> Sequence[str]:
    """A version of the split that behaves like the java one.

    @param string: the string to split
    @type string: str
    @param char: the character to use for splitting
    @type char: str

    @return: the initial string split in a sequence.
    @rtype: Sequence[str]
    """
    if string == "":
        return [""]
    split = string.split(char)
    i = len(split) - 1
    while i >= 0 and split[i] == "":
        split.pop(i)
        i -= 1
    return split
