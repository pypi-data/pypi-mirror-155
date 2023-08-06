"""This module contains the implementation af an BNIndex"""
from typing import Optional, List, Set, Dict

from pybabelnet.resources import BabelSynsetID
from pybabelnet.language import Language
from pybabelnet.pos import POS
from pybabelnet.iterators.abstract_iter import (
    BabelSynsetIterator,
    BabelOffsetIterator,
    BabelLexiconIterator,
    WordNetSynsetIterator,
)
from pybabelnet.resources import _InternalBabelSynsetID, WordNetSynsetID, ResourceID
from pybabelnet.synset import BabelSynset
from pybabelnet.versions import WordNetVersion, BabelVersion


class BNIndex:
    """Implementation of a BNIndex"""
    def successors(self, id_: BabelSynsetID) -> Optional[List[str]]:
        """Given a Babel id, collects the successors of the concept denoted by the id.

        @param id_: A concept identifier (BabelSynsetID)
        @type id_: BabelSynsetID

        @return: Return a stringified representation of the edges departing from the Babel synset denoted by the input id.
        @rtype: Optional[List[str]]
        """
        raise NotImplementedError()

    def license_ids_for_word(
            self, word: str, poses: Set[POS], langs: Set[Language], normalizer: bool
    ) -> List[_InternalBabelSynsetID]:
        """Get the set of ids license for the word with the given constraints.

        @param word: The word whose senses are to be retrieved.
        @type word: str
        @param poses: The PoSes of the word to be retrieved.
        @type poses: Set[POS]
        @param langs: The search languages for the input word.
        @type langs: Set[Language]
        @param normalizer: True if normalization should be applied when searching.
        @type normalizer: bool

        @return: The list of InternalBabelSynsetIDs associated with the given constraints.
        @rtype: List[_InternalBabelSynsetID]
        """
        raise NotImplementedError()

    def synsets(
            self,
            id2license_ids: Dict[BabelSynsetID, List[_InternalBabelSynsetID]],
            target_languages: Set[Language],
    ) -> List[BabelSynset]:
        """Construct the list of BabelSynsets from a map of BabelSynsetIDs
        to list of InternalBabelSynsetID.

        @param id2license_ids: Map of BabelSynsetIDs to list of InternalBabelSynsetID.
        @type id2license_ids: Dict[BabelSynsetID, List[_InternalBabelSynsetID]]
        @param target_languages: The languages to include in the synsets.
        @type target_languages: Set[Language]

        @return: The list of constructed synsets.
        @rtype: List[BabelSynset]
        """
        raise NotImplementedError()

    def wordnet_offsets(
            self, offset: str, version: WordNetVersion
    ) -> List[WordNetSynsetID]:
        """Retrieve WordNet 3.0 offset from old-version WordNet offSet.

        @param offset: The wordnet offset
        @type offset: str

        @param version: the wordnet version
        @type version: WordNetVersion

        @return: A list of WordNetSynsetID at the specified offset for that specified version
        @rtype: List[WordNetSynsetID]

        @raises InvalidSynsetIDError:
        @raises JavaError:
        """
        raise NotImplementedError()

    def mapping_from_babelsynsetids(
            self,
            *ids: BabelSynsetID,
    ) -> Dict[BabelSynsetID, List[_InternalBabelSynsetID]]:
        """Get a mapping from a list of BabelSynsetIDs

        @param ids: Collection of BabelSynsetID
        @type ids: BabelSynsetID

        @return: For each BabelSynsetID returns the necessary indexes to create the BabelSynset
        @rtype: Dict[BabelSynsetID, List[_InternalBabelSynsetID]]
        """
        raise NotImplementedError()

    def synset_iterator(
            self,
    ) -> BabelSynsetIterator:
        """Create a new instance of a synset iterator.
        @return: An iterator over BabelNet's synsets
        @rtype: BabelSynsetIterator
        """
        raise NotImplementedError()

    def offset_iterator(
            self,
    ) -> BabelOffsetIterator:
        """Create a new instance of a offset iterator.
        @rtype: BabelOffsetIterator
        """
        raise NotImplementedError()

    def lexicon_iterator(
            self,
    ) -> BabelLexiconIterator:
        """Create a new instance of a lexicon iterator.
        @rtype: BabelLexiconIterator
        """
        raise NotImplementedError()

    def wordnet_iterator(
            self,
    ) -> WordNetSynsetIterator:
        """Create a new instance of a wordnet iterator.
        @return: an iterator over Wordnet's synsets
        @rtype: WordNetSynsetIterator
        """
        raise NotImplementedError()

    def licence_ids_from_resource_id(
            self,
            resource_id: ResourceID,
    ) -> List[_InternalBabelSynsetID]:
        """Given a ResourceID, get a list of InternalBabelSynsetIDs.

        @param resource_id: The resource.
        @type resource_id: ResourceID

        @return: The list of InternalBabelSynsetIDs associated to the given ResourceID.
        @rtype: List[_InternalBabelSynsetID]
        """
        raise NotImplementedError()

    def synsets_from_resource_id(
            self,
            id_: ResourceID,
            id2license_ids: Dict[BabelSynsetID, List[_InternalBabelSynsetID]],
            target_langs: Set[Language],
    ) -> List[BabelSynset]:
        """Get a list of BabelSynset from a given ResourceID.

        @param id_: The ResourceID.
        @type id_: ResourceID
        @param target_langs: The output language
        @type target_langs: Set[Language]
        @param id2license_ids: a dict that maps BabelSynsetID to a list of _InternalBabelSynsetID
        @type id2license_ids: Dict[BabelSynsetID, List[_InternalBabelSynsetID]]

        @return: The list of BabelSynsets associated to the given ResourceID.
        @rtype: List[BabelSynset]
        """
        raise NotImplementedError()

    def version(
            self,
    ) -> BabelVersion:
        """The version of BabelNet.

        @return: the version
        @rtype: BabelVersion
        """
        raise NotImplementedError()
