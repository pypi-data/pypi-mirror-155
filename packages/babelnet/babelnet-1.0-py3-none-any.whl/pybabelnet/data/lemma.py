"""This module contains the BabelLemma class and related data."""
from typing import Optional

from aenum import OrderedEnum
from dataclasses import dataclass

from pybabelnet.data.source import BabelSenseSource
from pybabelnet.language import Language


class BabelLemmaType(OrderedEnum):
    """Types of lemmas in BabelNet."""

    HIGH_QUALITY: "BabelLemmaType" = 1
    """High quality lemmas, coming from professionally-curated res (such as WordNet or WordAtlas) or reliable crowdsources res."""

    POTENTIAL_NEAR_SYNONYM_OR_WORSE: "BabelLemmaType" = 2
    """Mostly Wikipedia redirections, which might be synonyms, near synonyms or related terms."""

    AUTOMATIC_TRANSLATION: "BabelLemmaType" = 3
    """Lemmas resulting from automatic translations (suggested use only for automatic text processing)."""

    @classmethod
    def from_babel_sense_source(
        cls, source: BabelSenseSource, language: Optional[Language] = None
    ) -> "BabelLemmaType":
        """Get the lemma type from a BabelSenseSource and its Language.

        @param source: The sense source.
        @param language: The sense language.

        @return: The lemma type.
        """
        auto = source.is_automatic_translation(language)
        if auto:
            return cls.AUTOMATIC_TRANSLATION
        elif source.is_redirection or source is BabelSenseSource.WIKIDATA_ALIAS:
            return cls.POTENTIAL_NEAR_SYNONYM_OR_WORSE
        return cls.HIGH_QUALITY

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


@dataclass(frozen=True, unsafe_hash=True)
class BabelLemma:
    """ A class representing the lemma in a BabelSynset.

    @ivar lemma: the lemma
    @ivar lemma_type: the type of the lemma
    """

    lemma: str
    """The lemma"""

    lemma_type: BabelLemmaType
    """The lemma type"""

    def __str__(self):
        return self.lemma

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)
