"""The Abstract api. It has all the abstract methods that the api needs"""
from abc import abstractmethod
from typing import List, Optional, Iterable, Dict, Callable, Set, Union

from ordered_set import OrderedSet

from pybabelnet.data.relation import BabelSynsetRelation
from pybabelnet.iterators.abstract_iter import (
    BabelSynsetIterator,
    BabelOffsetIterator,
    BabelLexiconIterator,
    WordNetSynsetIterator,
)
from pybabelnet.language import Language
from pybabelnet.pos import POS
from pybabelnet.resources import (
    ResourceID,
    BabelSynsetID,
    _InternalBabelSynsetID,
)
from pybabelnet.sense import BabelSense
from pybabelnet.synset import BabelSynset
from pybabelnet.versions import BabelVersion


class AbstractAPI(object):
    """The Abstract api."""
    def get_senses_containing(
        self,
        word: str,
        language: Optional[Language] = None,
        pos: Optional[POS] = None,
        to_langs: Optional[Set[Language]] = None
    ) -> List[BabelSense]:
        """
        Get the senses of synsets containing the word with the given constraints.

        @param word:  The word whose senses are to be retrieved.
        @type word: str
        @param language: The language of the input word.
        @type language: Optional[Language]
        @param pos: The Part of Speech of the word.
        @type pos: Optional[POS]
        @param to_langs: An iterable collection of Languages in which the senses are to be retrieved.
        @type to_langs: Optional[Set[Language]]

        @return: The senses of the word.
        @rtype: List[BabelSense]

        """
        return self.get_senses(
            word,
            from_langs=[language] if language else None,
            containing=True,
            poses=[pos] if pos else None,
            to_langs=to_langs if to_langs else None
        )

    def get_senses_from(
        self,
        word: str,
        language: Optional[Language] = None,
        pos: Optional[POS] = None,
        to_langs: Optional[Set[Language]] = None
    ) -> List[BabelSense]:
        """Get the senses of synsets from the word with the given constraints.

        @param word: The word whose senses are to be retrieved.
        @type word: str
        @param language: The language of the input word.
        @type language: Optional[Language]
        @param pos: The Part of Speech of the word.
        @type pos: Optional[POS]
        @param to_langs: An iterable collection of Languages in which the senses are to be retrieved.
        @type to_langs: Optional[Set[Language]]

        @return: The senses of the word.
        @rtype: List[BabelSense]

        """
        return self.get_senses(
            word,
            from_langs=[language] if language else None,
            poses=[pos] if pos else None,
            to_langs=to_langs if to_langs else None
        )

    def get_senses(self, *args: Union[str, ResourceID], **kwargs) -> List[BabelSense]:
        """Get the senses of synsets searched by words or by ResourceIDs,
        satisfying the optional constraints.

        @param args: A homogeneous collection of words (str) or ResourceIDs used to search for senses in synsets.
        @type args: Union[str, ResourceID]

        @keyword containing: Used if the senses are searched by words: if it is True, the words have to be contained in the sense (default False).
        @type containing: bool

        @keyword from_langs: An iterable collection of Languages used for searching the senses.
        @type from_langs: Iterable[Language]

        @keyword to_langs: An iterable collection of Languages in which the senses are to be retrieved.
        @type to_langs: Iterable[Language]

        @keyword poses: An iterable collection of Parts of Speech of the senses.
        @type poses: Iterable[POS]

        @keyword normalized: True if the search is insensitive to accents, etc. (default True).
        @type normalized: bool

        @keyword sources: An iterable collection of BabelSenseSources used to restrict the search.
        @type sources: Iterable[BabelSenseSource]

        @keyword synset_filters: An iterable collection of filters (functions accepting a BabelSynset and returning bool) to be applied to each synset retrieved.
        @type synset_filters: Iterable[Callable[[BabelSynset], bool]]

        @keyword sense_filters: An iterable collection of filters (functions accepting a BabelSense and returning bool) to be applied to each sense retrieved.
        @type sense_filters: Iterable[Callable[[BabelSynset], bool]]

        @return: The resulting senses.
        @rtype: List[BabelSense]

        @raise ValueError: If arg is not an homogeneous collection
        """
        self._prepare_kwargs(kwargs)

        if all(isinstance(arg, str) for arg in args):
            words = OrderedSet(args)
            return self._get_senses(words=words, **kwargs)
        if all(isinstance(arg, ResourceID) for arg in args):
            resource_ids = OrderedSet(args)
            return self._get_senses(resource_ids=resource_ids, **kwargs)
        else:
            raise ValueError("The arguments have to be homogeneous.")

    def get_synsets(self, *args: Union[str, ResourceID], **kwargs) -> List[BabelSynset]:
        """Get synsets by words or by ResourceIDs, satisfying the optional constraints.

        @param args: A homogeneous collection of words (str) or ResourceIDs used to search for synsets or senses in synsets.
        @type args: Union[str, ResourceID]

        @keyword containing: Used if the senses are searched by words: if it is True, the words have to be contained in the sense (default False).
        @type containing: bool

        @keyword from_langs: An iterable collection of Languages used for searching the senses.
        @type from_langs: Iterable[Language]

        @keyword to_langs: An iterable collection of Languages in which the senses are to be retrieved.
        @type to_langs: Iterable[Language]

        @keyword poses: An iterable collection of Parts of Speech of the senses.
        @type poses: Iterable[POS]

        @keyword normalized: True if the search is insensitive to accents, etc. (default True).
        @type normalized: bool

        @keyword sources: An iterable collection of BabelSenseSources used to restrict the search.
        @type sources: Iterable[BabelSenseSource]

        @keyword synset_filters: An iterable collection of filters (functions accepting a BabelSynset and returning bool) to be applied to each synset retrieved.
        @type synset_filters: Iterable[Callable[[BabelSynset], bool]]

        @keyword sense_filters: An iterable collection of filters (functions accepting a BabelSense and returning bool) to be applied to each sense retrieved.
        @type sense_filters: Iterable[Callable[[BabelSynset], bool]]

        @return: The resulting synsets.
        @rtype: List[BabelSynset]

        @raise ValueError: If arg is not an homogeneous collection
        """
        self._prepare_kwargs(kwargs)

        if all(isinstance(arg, str) for arg in args):
            words = OrderedSet(args)
            result = self._get_synsets(words=words, **kwargs)
            return result
        if all(isinstance(arg, ResourceID) for arg in args):
            resource_ids = OrderedSet(args)
            return self._get_synsets(resource_ids=resource_ids, **kwargs)
        else:
            raise ValueError("The arguments have to be homogeneous.")

    def get_synset(self, resource_id: ResourceID, to_langs: Optional[Set[Language]] = None) -> Optional[BabelSynset]:
        """Return the synset identified by the ResourceID in input.

        Some examples that can be used follow::
            import pybabelnet as pb

            # Retrieving BabelSynset from a Wikipedia page title:
            synset = pb.get_synset(WikipediaID('BabelNet', Language.EN, POS.NOUN))

            # Retrieving BabelSynset from a WordNet id:
            synset = pb.get_synset(WordNetSynsetID('wn:03544360n'))

            # Retrieving BabelSynset from a Wikidata page id:
            synset = pb.get_synset(WikidataID('Q4837690'))

            # Retrieving BabelSynset from a OmegaWiki page id:
            synset = pb.get_synset(OmegaWikiID('1499705'))

        @param resource_id: The resource identifier.
        @type resource_id: ResourceID
        @param to_langs: A set of languages to use. If passed as input, the results in those languages will be returned.
        @type to_langs: Optional[Set[Language]]

        @return: The synset identified by the ResourceID.
        @rtype: Optional[BabelSynset]
        """
        syns = self.get_synsets(resource_id, to_langs=to_langs if to_langs else None)
        return syns[0] if syns else None

    def _prepare_kwargs(self, kwargs):
        """Prepare the input data by trasforming each iterable in an ordered set."""
        if "from_langs" in kwargs and kwargs["from_langs"]:
            kwargs["from_langs"] = OrderedSet(kwargs["from_langs"])
        if "to_langs" in kwargs and kwargs["to_langs"]:
            kwargs["to_langs"] = OrderedSet(kwargs["to_langs"])
        if "poses" in kwargs and kwargs["poses"]:
            kwargs["poses"] = OrderedSet(kwargs["poses"])
        if "sources" in kwargs and kwargs["sources"]:
            kwargs["sources"] = OrderedSet(kwargs["sources"])
        if "sense_filters" in kwargs and kwargs["sense_filters"]:
            kwargs["sense_filters"] = OrderedSet(kwargs["sense_filters"])
        if "synset_filters" in kwargs and kwargs["synset_filters"]:
            kwargs["synset_filters"] = OrderedSet(kwargs["synset_filters"])

    @abstractmethod
    def _get_senses(
        self,
        words: Optional[Set[str]] = None,
        resource_ids: Optional[Set[ResourceID]] = None,
        containing: Optional[bool] = False,
        to_langs: Optional[Set[Language]] = None,
        sources: Optional[Set["BabelSenseSource"]] = None,
        **kwargs,
    ) -> List[BabelSense]:
        """
        Private version of get_senses().

        @param words:
        @param resource_ids:
        @param containing:
        @param to_langs:
        @param sources:
        @param kwargs:

        @return: the list of BabelSenses
        @rtype: List[BabelSense]

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    @abstractmethod
    def version(self) -> BabelVersion:
        """Get the version of loaded BabelNet indices.

        @return: The BabelVersion of BabelNet indices.

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    @abstractmethod
    def _get_synsets(
        self,
        words: Optional[Set[str]] = None,
        resource_ids: Optional[Set[ResourceID]] = None,
        from_langs: Optional[Set[Language]] = None,
        to_langs: Optional[Set[Language]] = None,
        poses: Set[Set[POS]] = None,
        normalized: Optional[bool] = True,
        sources: Optional[Set["BabelSenseSource"]] = None,
        synset_filters: Optional[Set[Callable[[BabelSynset], bool]]] = None,
        sense_filters: Optional[Set[Callable[[BabelSense], bool]]] = None,
    ) -> List[BabelSynset]:
        """
        Private version of get_synsets()

        @param words:
        @param resource_ids:
        @param from_langs:
        @param to_langs:
        @param poses:
        @param normalized
        @param sources:
        @param synset_filters:
        @param sense_filters:

        @return: the list of BabelSynset.
        @rtype: List[BabelSynset]

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    @abstractmethod
    def _mapping_from_ids(
        self,
        *ids: BabelSynsetID,
    ) -> Dict[BabelSynsetID, List["_InternalBabelSynsetID"]]:
        """
        Get the mapping from BabelSynsetID to _InternalBabelSynsetID.

        @param ids: a tuple of BabelSynsetID to use.
        @type ids: BabelSynsetID
        @return: The mapping from BabelSynsetID to a list of _InternalBabelSynsetID
        @rtype: Dict[BabelSynsetID, List["_InternalBabelSynsetID"]

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    def get_outgoing_edges(
        self, *args, **kwargs
    ) -> List[BabelSynsetRelation]:
        """
        Return the outgoing edges from a given BabelSynsetID

        @keyword synset_id: The BabelSynsetID whose outgoing edges we want to retrieve.
        @type synset_id: BabelSynsetID
        @return: The list of relation edges.
        @rtype: List[BabelSynsetRelation]
        """
        return self._get_outgoing_edges(*args, **kwargs)

    @abstractmethod
    def _get_outgoing_edges(
        self, synset_id: BabelSynsetID
    ) -> List[BabelSynsetRelation]:
        """
        Return the outgoing edges from a given BabelSynsetID

        @param synset_id: The BabelSynsetID whose outgoing edges we want to retrieve.
        @type synset_id: BabelSynsetID
        @return: The list of relation edges.
        @rtype: List[BabelSynsetRelation]

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    @abstractmethod
    def to_babelnet_synsets(self, id_: BabelSynsetID, languages: Set[Language]):
        """
        Get a BabelSytnset using the languages passed as input and an id_.
        @param id_: the id that needs to be converted
        @param languages: the languages to use.

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    @abstractmethod
    def _to_wordnet_synsets(self, id_: 'WordNetSynsetID', languages: Set[Language]):
        raise NotImplementedError

    @abstractmethod
    def to_synsets(
        self, resource_id: ResourceID, languages: Optional[Iterable[Language]] = None
    ) -> List[BabelSynset]:
        """Convert from ResourceID to the corresponding BabelSynset.

        @param resource_id: The input ID.
        @type resource_id: ResourceID
        @param languages: The target languages to populate synsets with (default None).
        @type languages: Optional[Iterable[Language]]

        @return: The list of corresponding synsets.
        @rtype: List[BabelSynset]

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    @abstractmethod
    def iterator(self) -> BabelSynsetIterator:
        """Create a new instance of BabelSynset iterator.

        @return: An instance of a BabelSynset iterator.
        @rtype: BabelSynsetIterator

        @raise NotImplementedError: Raised if the function is called using online APIs.
        """
        raise NotImplementedError

    @abstractmethod
    def wordnet_iterator(self) -> WordNetSynsetIterator:
        """Create a new instance of a WordNet iterator.

        @return: An instance of a WordNetSynset iterator.
        @rtype: WordNetSynsetIterator

        @raise NotImplementedError: Raised if the function is called using online APIs.
        """
        raise NotImplementedError

    @abstractmethod
    def offset_iterator(self) -> BabelOffsetIterator:
        """Create a new instance of an offset iterator.

        @return: An instance of a offset iterator.
        @rtype: BabelOffsetIterator
        @raise NotImplementedError: Raised if the function is called using online APIs.
        """
        raise NotImplementedError

    @abstractmethod
    def lexicon_iterator(self) -> BabelLexiconIterator:
        """Create a new instance of a lexicon iterator.

        @return: An instance of a lexicon iterator.
        @rtype: BabelLexiconIterator
        @raise NotImplementedError: Raised if the function is called using online APIs.
        """
        raise NotImplementedError

    @abstractmethod
    def images(self, id: BabelSynsetID):
        """
        Get the images of a BabelSynsetID.

        @param id: the BabelSynsetID to use
        @type id: BabelSynsetID

        @return: A list of BabelImages
        @rtype: List[BabelImage]

        @raise NotImplementedError: Raised if the function is called using online APIs.
        """
        raise NotImplementedError

    @abstractmethod
    def examples(
        self,
        synset_id: BabelSynsetID,
        filter_langs: Set[Language],
        *ids: _InternalBabelSynsetID,
    ):
        """
        Get the examples (in the specified languages) of a BabelSynsetID.

        @param synset_id: The BabelSynsetID to use
        @type synset_id: BabelSynsetID
        @param filter_langs: The set of language to use
        @type filter_langs: Set[Language]
        @param ids: the ids
        @type ids: _InternalBabelSynsetID

        @return: A list of BabelExamples
        @rtype: List[BabelExample]

        @raise NotImplementedError: Raised if not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def glosses(
        self,
        synset_id: BabelSynsetID,
        filter_langs: Set[Language],
        *ids: _InternalBabelSynsetID,
    ):
        """
        Get the glosses (in the specified languages) of a BabelSysetID.

        @param synset_id: the BabelSynsetID from where the glosses will be retreived
        @type synset_id: BabelSynsetID
        @param filter_langs: The set of language to use.
        @type filter_langs: Set[Language]
        @param ids: the _InternalBabelSynsetID
        @type ids: _InternalBabelSynsetID

        @return: A list of BabelGlosses
        @rtype: List[BabelGloss]

        @raise NotImplementedError: Raised if not implemented.
        """
        raise NotImplementedError
