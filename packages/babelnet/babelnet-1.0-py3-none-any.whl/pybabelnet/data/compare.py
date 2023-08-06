"""This module contains comparators for BabelSynsets and BabelSynsetRelations."""

from pybabelnet.data.source import BabelSenseSource
from pybabelnet.data.relation import BabelSynsetRelation
from pybabelnet.language import Language
from pybabelnet.synset import BabelSynset, BabelSynsetComparator
from pybabelnet._utils import comparator, cmp
from pybabelnet.sense import BabelSenseComparator, BabelWordSenseComparator


@comparator
class BabelSynsetGlossComparator:
    """
    Comparator for BabelSynset.

    It does the following:
        - sorts Babel synsets using their glosses number
        - sorts using BabelSynsetComparator
    """

    def __init__(self, word, language=Language.EN):
        """init method
        @param word: The word whose sense numbers are used to sort the BabelSynsets corresponding to WordNet synsets.
        @type word: str
        @param language: The language used to sort senses (default Language.EN).
        @type language: Language
        """
        self._word = word
        self._language = language

    @staticmethod
    def _compare_by_gloss_then_main_sense(b1: BabelSynset, b2: BabelSynset) -> int:
        """
        @param b1: First BabelSynset.
        @type b1: BabelSynset
        @param b2: Second BabelSynset.
        @type b2: BabelSynset

        @return: Compare result.
        @rtype: int
        """
        bsc = BabelSenseComparator()
        result = len(b2.glosses()) - len(b1.glosses())
        if result != 0:
            return result
        # Potrebbe tornare None, ma i comparatori non permettono di comparare con None
        return bsc.compare(b1.main_sense(Language.EN), b2.main_sense(Language.EN))

    def compare(self, b1: BabelSynset, b2: BabelSynset) -> int:
        """
        Compare two BabelSynsets

        @param b1: First BabelSynset.
        @type b1: BabelSynset
        @param b2: Second BabelSynset.
        @type b2: BabelSynset

        @return: Compare result.
        @rtype: int

        @raise NotImplemented: If b1 xor b2 are not instance of BabelSynset
        """
        if not isinstance(b1, BabelSynset) or not isinstance(b2, BabelSynset):
            return NotImplemented

        # compare the remaining types of senses
        bsc = BabelWordSenseComparator(self._word)

        b1_senses = b1.senses_by_word(
            self._word,
            self._language,
            BabelSenseSource.OMWN,
            BabelSenseSource.WONEF,
            BabelSenseSource.WIKI,
            BabelSenseSource.WIKIRED,
            BabelSenseSource.OMWIKI,
            BabelSenseSource.WIKIDATA,
            BabelSenseSource.WIKT,
            BabelSenseSource.MSTERM,
            BabelSenseSource.GEONM,
            BabelSenseSource.VERBNET,
        )
        b1_senses.sort(key=bsc)

        b2_senses = b2.senses_by_word(
            self._word,
            self._language,
            BabelSenseSource.OMWN,
            BabelSenseSource.WONEF,
            BabelSenseSource.WIKI,
            BabelSenseSource.WIKIRED,
            BabelSenseSource.OMWIKI,
            BabelSenseSource.WIKIDATA,
            BabelSenseSource.WIKT,
            BabelSenseSource.MSTERM,
            BabelSenseSource.GEONM,
            BabelSenseSource.VERBNET,
        )
        b2_senses.sort(key=bsc)
        if b1_senses and b2_senses and b1_senses[0].source is b2_senses[0].source:
            result = self._compare_by_gloss_then_main_sense(b1, b2)
            if result != 0:
                return result
            else:
                return BabelSynsetComparator(self._word, self._language).compare(b1, b2)
        return BabelSynsetComparator(self._word, self._language).compare(b1, b2)


@comparator
class BabelSynsetRelationComparator:
    """
    Comparator for BabelSynsets.

    It does the following:
        - sorts Babel synsets using theirs relations number
        - sorts using BabelSynsetComparator

    @ivar _word: The word whose sense numbers are used to sort the BabelSynsets corresponding to WordNet synsets.
    @ivar _language: The language used to sort senses (default Language.EN).
    """

    def __init__(self, word, language=Language.EN):
        """init method
        @param word: The word whose sense numbers are used to sort the BabelSynsets corresponding to WordNet synsets.
        @type word: str
        @param language: The language used to sort senses (default English).
        @type language: Language
        """
        self._word = word
        self._language = language

    @staticmethod
    def _compare_by_relation_then_main_sense(b1: BabelSynset, b2: BabelSynset) -> int:
        """
        @param b1: First BabelSynset.
        @type b1: BabelSynset
        @param b2: Second BabelSynset.
        @type b2: BabelSynset

        @return: Compare result.
        @rtype: int
        """
        bsc = BabelSenseComparator()
        result = len(b2.outgoing_edges()) - len(b1.outgoing_edges())
        if result != 0:
            return result
        # Potrebbe tornare None, ma i comparatori non permettono di comparare con None
        return bsc.compare(b1.main_sense(Language.EN), b2.main_sense(Language.EN))

    def compare(self, b1: BabelSynset, b2: BabelSynset) -> int:
        """
        Compare two BabelSynsets

        @param b1: First BabelSynset.
        @type b1: BabelSynset
        @param b2: Second BabelSynset.
        @type b2: BabelSynset

        @return: Compare result.
        @rtype: int
        """
        if not isinstance(b1, BabelSynset) or not isinstance(b2, BabelSynset):
            return NotImplemented

        bsc = BabelWordSenseComparator(self._word)
        b1senses = b1.senses_by_word(
            self._word,
            self._language,
            BabelSenseSource.OMWN,
            BabelSenseSource.WONEF,
            BabelSenseSource.WIKI,
            BabelSenseSource.WIKIRED,
            BabelSenseSource.OMWIKI,
            BabelSenseSource.WIKIDATA,
            BabelSenseSource.WIKT,
            BabelSenseSource.MSTERM,
            BabelSenseSource.GEONM,
            BabelSenseSource.VERBNET,
        )
        b1senses.sort(key=bsc)
        b2senses = b2.senses_by_word(
            self._word,
            self._language,
            BabelSenseSource.OMWN,
            BabelSenseSource.WONEF,
            BabelSenseSource.WIKI,
            BabelSenseSource.WIKIRED,
            BabelSenseSource.OMWIKI,
            BabelSenseSource.WIKIDATA,
            BabelSenseSource.WIKT,
            BabelSenseSource.MSTERM,
            BabelSenseSource.GEONM,
            BabelSenseSource.VERBNET,
        )
        b2senses.sort(key=bsc)
        if b1senses and b2senses and b1senses[0].source is b2senses[0].source:
            result = self._compare_by_relation_then_main_sense(b1, b2)
            if result != 0:
                return result
            else:
                return BabelSynsetComparator(self._word, self._language).compare(b1, b2)
        return BabelSynsetComparator(self._word, self._language).compare(b1, b2)


@comparator
class BabelSynsetIDRelationComparator:
    """
    Comparator for BabelSynsetRelations.

    It does the following:
        - puts manual relations first
        - sorts relations using their relation type (HYPERNYM, HYPONYM and MERONYM)
        - sorts lexicographically using their relation name
        - sorts lexicographically using their id target
    """

    @staticmethod
    def compare(rel1: BabelSynsetRelation, rel2: BabelSynsetRelation) -> int:
        """
        Compare two BabelSynstRelations

        @param rel1: First BabelSynsetRelation.
        @type rel1: BabelSynsetRelation
        @param rel2: Second BabelSynsetRelation.
        @type rel2: BabelSynsetRelation

        @return: Compare result.
        @rtype: int

        @raise NotImplemented: If b1 xor b2 are not instance of BabelSynset
        """
        if not isinstance(rel1, BabelSynsetRelation) or not isinstance(
            rel2, BabelSynsetRelation
        ):
            return NotImplemented

        r1 = rel1.pointer
        r2 = rel2.pointer

        is_automatic1 = r1.is_automatic
        is_automatic2 = r2.is_automatic

        # se e' automatica
        if is_automatic1 and not is_automatic2:
            return 1
        if not is_automatic1 and is_automatic2:
            return -1

        # se appartiene ad un gruppo
        if r1.relation_group is not r2.relation_group:
            return r2.relation_group.ordinal - r1.relation_group.ordinal

        # se e' generica
        is_generic1 = r1.symbol == "r"
        is_generic2 = r2.symbol == "r"

        if is_generic1 and not is_generic2:
            return 1
        if not is_generic1 and is_generic2:
            return -1

        # ordinata per nome della relazione
        if not r1.symbol == r2.symbol:
            return cmp(r1.name.lower(), r2.name.lower())

        # ordinata per id target
        if rel1.target == rel2.target:
            return rel2.language.ordinal - rel1.language.ordinal
        return cmp(rel1.target.lower(), rel2.target.lower())


__all__ = [
    "BabelSynsetGlossComparator",
    "BabelSynsetRelationComparator",
    "BabelSynsetIDRelationComparator",
]
