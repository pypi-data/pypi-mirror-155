"""This module contains the BabelExample class and the related comparator."""

from typing import Set, Optional

from pybabelnet.data.tokens import BabelTokenWord
from pybabelnet.data.source import BabelSenseSource
from pybabelnet.data.license import BabelLicense
from pybabelnet.language import Language
from pybabelnet._utils import comparator
from pybabelnet.sense import BabelSense


class BabelExample:
    """
    An example sentence in BabelNet.

    @ivar source : The region of BabelNet from which this example comes from.
    @type source : BabelSenseSource
    @ivar source_sense : The WordNet or Wikipedia sense from which the sense is taken.
    @type source_sense : str
    @ivar language : The language of the example.
    @type language : Language
    @ivar example : The example itself.
    @type example : str
    @ivar tokens_word_example : A set of BabelTokenWords. Each BabelTokenWord corresponds to the lemma that appears in this Babel example and for which it is an usage example.
    @type tokens_word_example : Set[BabelTokenWord]
    """

    def __init__(self, source: BabelSenseSource, source_sense: str, language: Language, example: str,
                 tokens: Optional[Set[BabelTokenWord]] = None):
        """init method
        @param source: The example source.
        @param source_sense: The sense of the example.
        @param language: The language the example is written in.
        @param example: the example.
        @param tokens: The tokens that belong to the example (default None).
        """
        self.source = source
        self.source_sense = source_sense
        self.language = language
        self.example = example
        if tokens is None:
            self.tokens_word_example = set()
        else:
            self.tokens_word_example = tokens

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __str__(self):
        return self.example

    @property
    def license(self) -> BabelLicense:
        """The license for this Babel example."""
        return self.source.get_license(self.language)


@comparator
class BabelExampleComparator:
    """
    Comparator for BabelExamples which sorts by sources.
    """

    def __init__(self, main_sense: BabelSense = None):
        """init method
        @param main_sense: The sense the examples refer to (default None).
        """
        self._main_sense = main_sense

    def compare(self, b1: BabelExample, b2: BabelExample) -> int:
        """
        Compare two BabelExamples
        @param b1: First BabelExample.
        @param b2: Second BabelExample

        @return: Compare result.

        @raise NotImplemented: If b1 xor b2 are not instance of BabelExample
        """
        if not isinstance(b1, BabelExample) or not isinstance(b2, BabelExample):
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


__all__ = ["BabelExample", "BabelExampleComparator"]
