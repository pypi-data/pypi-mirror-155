"""This module contains classes of ResourceID's related to BabelNet."""

import traceback
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Iterable, Optional, List, Dict, TYPE_CHECKING

from aenum import AutoNumberEnum

from babelnet import api
from babelnet._utils import cmp
from babelnet.data.license import BabelLicense
from babelnet.data.source import BabelSenseSource
from babelnet.language import Language
from babelnet.pos import POS
from babelnet.versions import WordNetVersion

if TYPE_CHECKING:
    from babelnet.data.relation import BabelSynsetRelation


class BabelExternalResource(AutoNumberEnum):
    """External res linked from BabelNet."""

    DBPEDIA = ()
    YAGO = ()
    GEONAMES = ()
    FRAMENET = ()
    VERBNET = ()

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class ResourceID(ABC):
    """A basic resource identifier.

    @ivar id: ID of a ResourceID.
    @type id: str
    @ivar source: Source of the resource ID.
    @type source: BabelSenseSource
    @ivar pos: POS of the resource ID, if available.
    @type pos: Optional[POS]
    @ivar language: Language of the resource ID, if available.
    @type language: Optional[Language]
    """

    @abstractmethod
    def __init__(self, id_str: str, source: BabelSenseSource):
        """init method
        @param id_str: ID of the resource.
        @param source: Source of the resource.
        """
        self.id = id_str.strip() if id_str else id_str
        self.source = source
        self.pos: Optional[POS] = None
        self.language: Optional[Language] = None

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.id

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    # riabilitare se serve, spostando __eq__ e __lt__ in InternalBabelSynsetID
    #
    #    def __eq__(self, other):
    #        if isinstance(other, ResourceID):
    #            return self.id == other.id
    #        return False

    def __eq__(self, other):
        if isinstance(other, ResourceID):
            return cmp(self.id.lower(), other.id.lower()) == 0
        return False

    def __lt__(self, other):
        if isinstance(other, ResourceID):
            return cmp(self.id.lower(), other.id.lower()) < 0
        else:
            return NotImplemented

    # TODO: NO TYPING
    def to_synsets(
            self, languages: Optional[Iterable[Language]] = None
    ) -> List["BabelSynset"]:
        """Convert the ID to a collection of BabelSynsets.

        @param languages: The languages to populate the synsets with (default is None).

        @return: The corresponding synsets (in most cases, it will be just a single synset).
        @rtype: List[L{BabelSynset <babelnet.synset.BabelSynset>}]
        """
        return api.get_synsets(self, to_langs=languages)


class ResourceWithLemmaID(ResourceID):
    """A resource identifier with multiple parameters.

    @ivar language: The item's language.
    @type language: Language
    @ivar pos: The item's part of speech (default None).
    @type pos: Optional[POS]
    """

    @abstractmethod
    def __init__(
            self,
            title: str,
            language: Language,
            source: BabelSenseSource,
            pos: Optional[POS] = None,
    ):
        """init method
        @param title: The item's title.
        @type title: str
        @param language: The item's language.
        @type language: Language
        @param source: The sense source.
        @type source: BabelSenseSource
        @param pos: The item's part of speech (default None).
        @type pos: Optional[POS]
        """
        super().__init__(title, source)
        self.language = language
        self.pos = pos

    @property
    def title(self) -> str:
        """The title of this ResourceWithLemmaID.
        @return: the title
        @rtype: str
        """
        return self.id


class InvalidSynsetIDError(RuntimeError):
    """Exception for an invalid synset ID. It is thrown when the format
    of the Babel synset identifier is invalid or is not well formed.
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: Synset ID.
        """
        super().__init__("Invalid SynsetID " + id_str)


class SynsetID(ResourceID):
    """A unique identifier for a Synset.

    @ivar pos: the POS
    @type pos: POS
    """

    def __init__(self, id_str: str, source):
        """init method
        @param id_str: Synset ID.
        @type id_str: str
        @param source: Source

        @raises InvalidSynsetIDError: Raised if the ID is invalid
        """
        super().__init__(id_str, source)
        if not self.is_valid:
            raise InvalidSynsetIDError(str(self))
        self.pos = POS.from_tag(id_str[-1])

    @property
    def simple_offset(self) -> str:
        """The offset without prefix (e.g. C{`wn:`} or C{`bn:`}).
        @return: the offset of the Synset.
        @rtype: str
        """
        
        prefix_length = 3
        if self.source == BabelSenseSource.WN2020: prefix_length = 7
        elif self.source == BabelSenseSource.OEWN: prefix_length = 5

        return self.id[prefix_length:]

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        """
        True if the SynsetID is valid, False otherwise

        @return: True or False
        @rtype: bool
        """
        ...


class BabelSynsetID(SynsetID):
    """A resource identifier with the specified BabelSynset ID.
    To obtain the corresponding synset, call to_synset().
    """

    _BABELNET_ID_PREFIX = "bn:"
    """The BabelNet ID prefix (str)."""

    _WORDATLAS_ID_PREFIX = "wa:"
    """The WordAtlas ID prefix (str)."""

    _BABELNET_ID_LENGTH = 12
    """The BabelNet ID prefix (int)."""

    _WORDATLAS_ID_LENGTH = 10
    """The WordAtlas ID length e.g: wa:tqlms5n"""

    def __init__(self, id_str: str):
        """init method
        Examples of BabelSynsetID::
            rid = BabelSynsetID('bn:03083790n')

        @param id_str: ID of the resource.
        @raise InvalidSynsetIDError: Raise if the ID is invalid.
        """
        super().__init__(
            id_str,
            BabelSenseSource.BABELNET
            if id_str.startswith(self._BABELNET_ID_PREFIX)
            else BabelSenseSource.WORD_ATLAS,
        )

    @property
    def is_valid(self) -> bool:
        return (
                       self.id.startswith(self._BABELNET_ID_PREFIX)
                       and len(self.id) == self._BABELNET_ID_LENGTH
               ) or (
                       self.id.startswith(self._WORDATLAS_ID_PREFIX)
                       and len(self.id) == self._WORDATLAS_ID_LENGTH
               )

    # TODO: NO TYPING
    def to_synset(self) -> "BabelSynset":
        """From a lightweight BabelSynsetID, create the corresponding
        BabelSynset.

        @return: The BabelSynset corresponding to this ID.
        """
        synsets = self.to_synsets()
        return synsets[0] if synsets else None

    @property
    def outgoing_edges(self) -> List["BabelSynsetRelation"]:
        """The edges (BabelSynsetRelations) which connect the current synset.

        @return: the outgoing edges
        """
        return api.get_outgoing_edges(self)


@total_ordering
class _InternalBabelSynsetID(BabelSynsetID):
    """Internal version of a BabelSynsetID"""
    def __init__(self, id_str: str):
        """init method
        @param id_str: the id as a string
        @type id_str: str
        """
        super().__init__(id_str)

    @property
    def is_valid(self) -> bool:
        return True

    @property
    def babel_license(self) -> Optional[BabelLicense]:
        """Return the BabelLicense associated with the given ID.
        @return: If the BabelLicense is present, returns it
        @rtype: Optional[BabelLicense]
        """
        return BabelLicense.long_name(self.id.split(":")[0])


class WordNetSynsetID(SynsetID):
    """A resource identifier with the specified WordNet synset id.

    Examples of WordNetSynsetID::
        rid = WordNetSynsetID('wn:06879521n')

    @ivar version: WordNet version.
    @type version: WordNetVersion
    @ivar version_mapping: Cross-version mapping.
    @type version_mapping: Dict[WordNetVersion, List[str]]
    """

    _ID_PREFIX = "wn:"
    """The WordNet offset prefix (str)."""

    _WN2020_ID_PREFIX: str = "wn2020:"
    """The WordNet 2020 offset prefix"""

    _OEWN_ID_PREFIX: str = "oewn:"
    """The Open English WordNet offset prefix"""

    _ID_LENGTH = 12
    """ID string length (int)."""

    _WN2020_ID_LENGTH: int = 16
    """ID lenght for WN2020"""

    _OEWN_ID_LENGTH: int = 14
    """ID lenght for OEWN"""

    def __init__(
            self,
            id_str: str,
            version: Optional[WordNetVersion] = None,
            mapping: Optional[Dict[WordNetVersion, List[str]]] = None,
    ):
        """init method
        @param id_str: The synset ID string.
        @param version: The WordNet version (default WordNetVersion.WN_30).
        @param mapping: Cross-version mapping (default None).

        @raise InvalidSynsetIDError: Raised if the synset ID is invalid.
        """
        if version is None and mapping is None:
            self.__init__(
                id_str=id_str,
                version=self._check_prefix_WN(id_str),
            )
        if version is not None:
            super().__init__(
                id_str,
                self._check_prefix_BS(id_str),
            )
            self.version: WordNetVersion = version

        self.version_mapping = mapping if mapping is not None else {}

    @property
    def is_valid(self) -> bool:
        return (
            self.id.startswith(WordNetSynsetID._ID_PREFIX)
            and len(self.id) == WordNetSynsetID._ID_LENGTH
        ) or (
            self.id.startswith(WordNetSynsetID._WN2020_ID_PREFIX)
            and len(self.id) == WordNetSynsetID._WN2020_ID_LENGTH
        ) or (
            self.id.startswith(WordNetSynsetID._OEWN_ID_PREFIX)
            and len(self.id) == WordNetSynsetID._OEWN_ID_LENGTH
        )

    def to_version(self, target_version: WordNetVersion) -> List["WordNetSynsetID"]:
        """Obtain a list of WordNetSynsetIDs corresponding to this
        WordNetSynsetID in the input WordNetVersion.

        @param target_version: The target version to convert to.

        @return: Corresponding IDs.
        """
        if not self.version_mapping:
            return []
        lst = self.version_mapping[target_version]
        if not lst:
            return []
        lst_wn = []
        if (
                self.version is WordNetVersion.WN_30
                or target_version is WordNetVersion.WN_30
        ):
            for wn in lst:
                try:
                    lst_wn.append(
                        WordNetSynsetID(
                            "wn:" + wn, target_version, self.version_mapping
                        )
                    )
                except InvalidSynsetIDError:
                    traceback.print_exc()
        return lst_wn

    def _check_prefix_WN(self, prefix):
        """check the prefix and return a wordnet version
        @param prefix: the prefix to check
        @type prefix: str
        @return: a WordNetVersion
        @rtype: WordNetVersion
        """
        if prefix.startswith(WordNetSynsetID._WN2020_ID_PREFIX):
            return WordNetVersion.WN_2020
        elif prefix.startswith(WordNetSynsetID._OEWN_ID_PREFIX):
            return WordNetVersion.OEWN
        else:
            return WordNetVersion.WN_30

    def _check_prefix_BS(self, prefix):
        """check the prefix and return a babel sense source version

        @param prefix: the prefix to check
        @type prefix: str

        @return: a BabelSenseSource
        @rtype: BabelSenseSource
        """
        if prefix.startswith(WordNetSynsetID._WN2020_ID_PREFIX):
            return BabelSenseSource.WN2020
        elif prefix.startswith(WordNetSynsetID._OEWN_ID_PREFIX):
            return BabelSenseSource.OEWN
        else:
            return BabelSenseSource.WN


class FrameNetID(ResourceID):
    """A resource identifier with the specified U{FrameNet
    <https://framenet.icsi.berkeley.edu>} resource id.

    Example of FrameNetID::
        rid = FrameNet('4183')
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: ID of the resource.
        @type id_str: str
        """
        super().__init__(id_str, BabelSenseSource.FRAMENET)


class GeoNamesID(ResourceID):
    """A resource identifier with the specified U{GeoNames <http://www.geonames.org>} resource id.

    Example of GeoNamesID::
        rid = GeoNamesID('3169071')
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: ID of the resource.
        @type id_str: str
        """
        super().__init__(id_str, BabelSenseSource.GEONM)


class MSTermID(ResourceID):
    """A resource identifier with the specified U{Microsoft Terminology
    <https://www.microsoft.com/en-us/language>} resource id.

    Example of MSTermID::
        rid = MSTermID('ms:63131')
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: ID of the resource.
        @type id_str: str
        """
        super().__init__(id_str, BabelSenseSource.MSTERM)


class OmegaWikiID(ResourceID):
    """
    A resource identifier with the specified U{OmegaWiki <http://omegawiki.org>} resource id.

    Example of OmegaWikiID::
        rid = OmegaWikiID('ow:1499705')
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: ID of the resource.
        """
        super().__init__(id_str, BabelSenseSource.OMWIKI)


class VerbNetID(ResourceID):
    """A resource identifier with the specified U{VerbNet
    <http://verbs.colorado.edu/~mpalmer/projects/verbnet.html>} resource id.

    Example of VerbNetID::
        rid = VerbNetID('vn:estimate-34.2')
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: ID of the resource.
        """
        super().__init__(id_str, BabelSenseSource.VERBNET)


class WikidataID(ResourceID):
    """A resource identifier with the specified U{Wikidata
    <http://wikidata.org>} resource id.

    Example of WikiDataID::
        rid = WikidataID('Q4837690')
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: ID of the resource.
        """
        super().__init__(id_str, BabelSenseSource.WIKIDATA)


class WikipediaID(ResourceWithLemmaID):
    """A resource identifier with the specified U{Wikipedia <http://wikipedia.org>} page title, language and POS.

    Example of WikipediaID::
        rid = WikipediaID('BabelNet', Language.EN)
        rid = WikipediaID('BabelNet', Language.EN, POS.NOUN)
    """

    def __init__(self, title: str, language: Language, pos: Optional[POS] = None):
        """init method
        @param title: The Wikipedia page title.
        @param language: The Wikipedia page language.
        @param pos: The POS (always noun) (default None).
        """
        super().__init__(title, language, BabelSenseSource.WIKI, pos)


class WikiquoteID(ResourceWithLemmaID):
    """A resource identifier with the specified U{Wikiquote <http://wikiquote.org>} page title, language and POS.

    Example of WikiquoteID::
        rid = WikiquoteID('Rome', Language.EN)
        rid = WikiquoteID('Rome', Language.EN, POS.NOUN)
    """

    def __init__(self, title: str, language: Language, pos: Optional[POS] = None):
        """init method
        @param title: The Wikipedia page title.
        @type title: str
        @param language: The Wikipedia page language.
        @type language: Language
        @param pos: The POS (default None).
        @type pos: Optional[POS]

        """
        super().__init__(title, language, BabelSenseSource.WIKIQU, pos)


class WiktionaryID(ResourceID):
    """A resource identifier with the specified U{Wiktionary <https://wiktionary.org>} id.

    Example of WikitionaryID::
        rid = WiktionaryID('90930s1e1')
    """

    def __init__(self, id_str: str):
        """init method
        @param id_str: ID of the resource.
        @type id_str: str
        """
        super().__init__(id_str, BabelSenseSource.WIKT)


__all__ = [
    "BabelExternalResource",
    "ResourceID",
    "ResourceWithLemmaID",
    "SynsetID",
    "InvalidSynsetIDError",
    "BabelSynsetID",
    "WordNetSynsetID",
    "FrameNetID",
    "GeoNamesID",
    "MSTermID",
    "OmegaWikiID",
    "VerbNetID",
    "WikidataID",
    "WikipediaID",
    "WikiquoteID",
    "WiktionaryID",
]
