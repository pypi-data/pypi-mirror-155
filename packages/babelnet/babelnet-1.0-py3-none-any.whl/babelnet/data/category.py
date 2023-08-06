"""This module contains the BabelCategory class."""
from typing import Optional

from babelnet.data.license import BabelLicense
from babelnet.data.tag import Tag
from babelnet.language import Language
from babelnet.conf import _config


class BabelCategory(Tag):
    """
    A Wikipedia category associated with a BabelSynset.

    @ivar _category: the category
    @type _category: str
    @ivar language: the language
    @type language: Language
    """

    _BABEL_CATEGORY_PREFIX = "BNCAT:"
    """Category prefix (str)"""

    license = BabelLicense.CC_BY_SA_30
    """The license for this Babel category."""

    _WIKIPEDIA_URL_INFIX = "wikipedia.org/wiki/"
    """Wikipedia infix"""

    def __init__(self, category: str, language: Language):
        """
        init method

        @param category :The category string.
        @param language :The category language.
        """
        self._category = category
        self._language = language if type(language) == Language else Language[language]

    @property
    def category(self) -> str:
        """The category itself, e.g. C{Scientists who commited suicide}."""
        return self._category

    @property
    def language(self) -> Language:
        """The language of the category label, English, Italian, etc."""
        return self._language

    @property
    def value(self) -> str:
        return self.category

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __str__(self):
        return self._BABEL_CATEGORY_PREFIX + str(self.language) + ":" + self.category

    @property
    def wikipedia_uri(self) -> str:
        """The URI of the Wikipedia page this BabelCategory corresponds to.

        Examples:
            - for the English category C{Mathematicians_who_committed_suicide}:
              C{http://en.wikipedia.org/wiki/Category:Mathematicians_who_committed_suicide}
            - for the German category C{Kategorie:Mitglied der Royal Society}:
              C{http://de.wikipedia.org/wiki/Kategorie:Mitglied_der_Royal_Society}

        @return: the URI of the Wikipedia page
        @rtype: str
        """
        language_category_name = self.category_prefix(self.language)
        return (
                "http://"
                + str(self.language).lower()
                + "."
                + self._WIKIPEDIA_URL_INFIX
                + language_category_name
                + self.category
        )

    @staticmethod
    def from_string(category_string: str) -> Optional["BabelCategory"]:
        """Create a new instance of a BabelCategory from a string with
        format C{<language_id>:<category_label>}, e.g. C{EN:Scientist_who_committed_suicide}.

        @param category_string : The string of the category to be retrieved.
        @type category_string: str

        @return: An instance of a BabelCategory from an input string.
        @rtype: Optional[BabelCategory]
        """
        if ":" not in category_string:
            return None
        idx = category_string.index(":")
        category = category_string[idx + 1:]
        language = Language[category_string[:idx]]
        return BabelCategory(category, language)

    @staticmethod
    def category_prefix(language: Language) -> Optional[str]:
        """Get the prefix of a category in the selected language.

        @param language : The prefix language.
        @type language: Language

        @return: The prefix.
        @rtype: Optional[str]
        """
        try:
            cat_prefix = _config.CATEGORY_PREFIXES[language][0]
            if not cat_prefix.endswith(":"):
                cat_prefix += ":"
            return cat_prefix
        except KeyError:
            return None
        except TypeError:
            return None


__all__ = ["BabelCategory"]
