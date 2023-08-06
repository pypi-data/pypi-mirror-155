"""This module contains the BabelGloss class and the related comparator."""

from typing import Set, Optional

from pybabelnet.data.tokens import BabelTokenId
from pybabelnet.data.source import BabelSenseSource
from pybabelnet.data.license import BabelLicense
from pybabelnet._utils import comparator


class BabelGloss:
    """A gloss in BabelNet.

    @ivar source : The region of BabelNet from which this gloss comes from.
    @type source: BabelSenseSource
    @ivar source_sense : The WordNet or Wikipedia sense from which the sense is taken.
    @type source_sense: int
    @ivar language : The language of the gloss.
    @type language: Language
    @ivar gloss : The gloss string.
    @type gloss: str
    @ivar token_ids : A list of BabelTokenIds. Each BabelTokenId is the association between the lemma that appears in this Babel gloss, and the BabelSynset id that identifies the lemma in BabelNet.
    @type token_ids: Set[BabelTokenId]
    """

    def __init__(self, source, source_sense, language, gloss, tokens=None):
        """init method
        @param source: The gloss source.
        @type source: BabelSenseSource
        @param source_sense: The sense the gloss defines.
        @type source_sense: int
        @param language: The language the gloss is written in.
        @type language: Language
        @param gloss: The gloss string.
        @type gloss: str
        @param tokens: The tokens that belong to the gloss (default None)
        @type tokens: Optional[Set[BabelTokenId]]
        """
        self.source = source
        self.source_sense = source_sense
        self.language = language
        self.gloss = gloss
        if not tokens:
            self.token_ids = set()
        else:
            self.token_ids = tokens

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __str__(self):
        return self.gloss

    @property
    def license(self) -> BabelLicense:
        """The license for this Babel gloss.
        @return: The license for this Babel gloss.
        @rtype: BabelLicense
        """
        return self.source.get_license(self.language)


@comparator
class BabelGlossComparator:
    """
    Comparator for BabelGlosses which sorts by sources.
    """

    def __init__(self, main_sense=None):
        """init method
        @param main_sense: The sense the glosses refer to (default None).
        """
        self._main_sense = main_sense

    def compare(self, b1: BabelGloss, b2: BabelGloss) -> int:
        """
        Compare two BabelGlosses

        @param b1: First BabelGloss.
        @param b2: Second BabelGloss.

        @return: Compare result.

        @raise NotImplemented: If b1 xor b2 are not instance of BabelExample
        """
        if not isinstance(b1, BabelGloss) or not isinstance(b2, BabelGloss):
            return NotImplemented
        if self._main_sense:
            if (
                self._main_sense.source is b1.source
                and self._main_sense.full_lemma == b1.source_sense
                and self._main_sense.language is b1.language
            ):
                return -1
            if (
                self._main_sense.source is b2.source
                and self._main_sense.full_lemma == b2.source_sense
                and self._main_sense.language is b2.language
            ):
                return 1
        if b1.language is not b2.language:
            return b1.language.ordinal - b2.language.ordinal
        return b1.source.ordinal_for_sorting - b2.source.ordinal_for_sorting


__all__ = ["BabelGloss", "BabelGlossComparator"]
