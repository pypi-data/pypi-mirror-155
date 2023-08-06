"""This module defines BabelSynsets and related data."""
import json
import logging
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from functools import cmp_to_key
from typing import Dict, List, Set, Optional, Callable, Mapping, Type, Union, Sequence

from aenum import Enum
from ordered_set import OrderedSet

from pybabelnet import _restful, api
from pybabelnet._utils import comparator, flatten_to_ascii, cmp, UnsupportedOnlineError
from pybabelnet.data.category import BabelCategory
from pybabelnet.data.domain import BabelDomain
from pybabelnet.data.example import BabelExample, BabelExampleComparator
from pybabelnet.data.frame import FrameID
from pybabelnet.data.gloss import BabelGloss, BabelGlossComparator
from pybabelnet.data.image import BabelImage, BabelImageComparator
from pybabelnet.data.lemma import BabelLemmaType, BabelLemma
from pybabelnet.data.phonetics import BabelSensePhonetics, BabelAudio
from pybabelnet.data.qcode import QcodeID
from pybabelnet.data.relation import BabelPointer, BabelSynsetRelation
from pybabelnet.data.source import BabelSenseSource
from pybabelnet.data.tag import StringTag, Tag
from pybabelnet.data.tokens import BabelTokenId, BabelTokenWord
from pybabelnet.data.usage import Usage
from pybabelnet.language import Language
from pybabelnet.pos import POS
from pybabelnet.resources import WordNetSynsetID, BabelExternalResource, BabelSynsetID
from pybabelnet.sense import (
    BabelSense,
    WordNetSense,
    BabelWordSenseComparator,
    BabelSenseComparator,
)
from pybabelnet.versions import WordNetVersion

_log = logging.getLogger(__name__)


class SynsetType(Enum):
    """A kind of Synset -- namely, named entity, concept or unknown."""

    NAMED_ENTITY: "SynsetType" = "Named Entity"
    """Named Entity is a word that clearly identifies one item."""

    CONCEPT: "SynsetType" = "Concept"
    """A concept is an abstraction or generalization from experience."""

    UNKNOWN: "SynsetType" = "Unknown"
    """Unknown."""

    def __str__(self):
        return self.value.name

    def __repr__(self):
        return str(self)

    @property
    def value(self) -> "SynsetType":
        return self


class BabelSynset(ABC):
    """A Babel synset in BabelNet with all the operations.

    @ivar id: The id of the synset.
    @type id: BabelSynsetID
    """

    def __init__(self, synset_id: BabelSynsetID, target_langs: Set[Language]):
        """init method
        @param synset_id: the BabelSynsetID
        @param target_langs: the target languages
        """
        self.id = synset_id
        self._target_langs = target_langs

        self._is_loaded = False

        self._contained_sense_sources = None
        self._senses = None
        self._domains = None
        self._wn_offsets = None
        self._main_senses = {}
        self._edges = None
        self._glosses = None
        self._examples = None
        self._images = None
        self._main_image = None
        self._type = None
        self._translations = None
        self._key_concept = False
        self._frame_id: Optional[FrameID] = None
        self._tags: Optional[Mapping[Type[Tag], Union[SynsetType, List[Tag]]]] = None,
        self._synset_degree: Optional[int] = -1
        self._qcode_ids: Optional[List[QcodeID]] = None

    def __str__(self):
        if not self._is_loaded:
            self._load()
        if not self._senses:
            return self.id.id
        bs = self.main_sense_preferably_in(Language.EN)
        if bs.source is BabelSenseSource.WN:
            return f"{bs.id}__{bs.sense_str}"
        return f"{bs.id}__{bs.source}:{bs.language}:{bs.full_lemma}"

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __iter__(self):
        if not self._is_loaded:
            self._load()
        return iter(self._senses)

    def __len__(self):
        if not self._is_loaded:
            self._load()
        return len(self._senses)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, BabelSynset):
            return self.id == other.id
        return False

    def _valid_degree(self) -> int:
        """The synset degree associated with this synset, or the number of outgoing edges if the synset degree
        is not available.

        @return: the synset degree of this synset
        @rtype: int
        """
        if not self._is_loaded:
            self._load()
        if self._synset_degree != -1:
            return self._synset_degree

        return len(
            [
                g
                for g in self.outgoing_edges()
                if g.language not in [Language.CEB, Language.SH, Language.SR]
            ]
        )

    @abstractmethod
    def _load(self):
        return ...

    @abstractmethod
    def _get_glosses(self):
        return ...

    @abstractmethod
    def _get_examples(self):
        return ...

    @property
    @abstractmethod
    def translations(self) -> Dict[BabelSense, Set[BabelSense]]:
        """
        All translations between senses found in this BabelSynset.

        @return: A dict from BabelSense to his translation.
        @rtype: Dict[BabelSense, Set[BabelSense]]
        """
        return ...

    @property
    @abstractmethod
    def images(self) -> List[BabelImage]:
        """
        The images (BabelImages) of this BabelSynset.

        @return: All the images of the Synset.
        @rtype: List[BabelImage]
        """
        return ...

    @property
    def languages(self) -> Set[Language]:
        """
        The set of languages used in this Synset.

        @return: the languages used in this Synset.
        @rtype: Set[Language]
        """
        return {s.language for s in self.senses()}

    @property
    def pos(self) -> POS:
        """The part of speech of this Synset.

        @return: the pos of this Synset.
        @rtype: Set[Language]
        """
        return self.id.pos

    @property
    def sense_sources(self) -> List[BabelSenseSource]:
        """The list of sense sources contained in the synset.

        @return: the sense sources of this Synset.
        @rtype: List[BabelSenseSource]
        """
        if not self._is_loaded:
            self._load()
        if self._contained_sense_sources is None:
            distinct_sources = OrderedSet(s.source for s in self.senses())
            self._contained_sense_sources = list(distinct_sources)
        return self._contained_sense_sources

    @property
    def domains(self) -> Dict[BabelDomain, float]:
        """The BabelDomains of this BabelSynset.

        @return: the domains of this Synset.
        @rtype: Dict[BabelDomain, float]
        """
        if not self._is_loaded:
            self._load()
        return self._domains

    @property
    def wordnet_offsets(self) -> List[WordNetSynsetID]:
        """The WordNet offsets (version 3.0) whose corresponding synsets this
        BabelSynset covers, if any.

        @return: the wordnet offset of this Synset.
        @rtype: List[WordNetSynsetID]
        """
        if not self._is_loaded:
            self._load()
        return self._wn_offsets.copy()

    @property
    def is_key_concept(self) -> bool:
        """True if the synset is a key concept.

        @return: True or False
        @rtype: bool
        """
        if not self._is_loaded:
            self._load()
        return self._key_concept

    @property
    def frame_id(self) -> Optional[FrameID]:
        """Return the FrameID associated with this synset.

        @return: the FrameID of this synset
        @rtype: Optional[FrameID]
        """
        if not self._is_loaded:
            self._load()
        return self._frame_id

    @property
    @abstractmethod
    def synset_degree(self) -> int:
        """The synset degree associated with this synset.

        @return: the synset degree of this synset
        @rtype: int
        """
        return ...

    @property
    def qcode_ids(self) -> List[QcodeID]:
        """The qcode identifier associated with this synset.

        @return: the qcode of this synset
        @rtype: List[QcodeID]
        """
        if not self._is_loaded:
            self._load()
        return self._qcode_ids

    @property
    def main_image(self) -> Optional[BabelImage]:
        """The best image (BabelImage) of this BabelSynset.

        @return: the best image of this synset
        @rtype: Optional[BabelImage]
        """
        if not self._is_loaded:
            self._load()
        if not self._main_image and self.images:
            self._images.sort(key=BabelImageComparator())
            self._main_image = self._images[0]
        return self._main_image

    def categories(self, *languages: Language) -> List[BabelCategory]:
        """Get the categories (BabelCategory) of this BabelSynset
        in the specified languages (if not specified, return all categories).

        @param languages: The search languages.

        @return: The categories (BabelCategory) of this BabelSynset
        @rtype: List[BabelCategory]
        """
        if not self._is_loaded:
            self._load()
        categories: List[BabelCategory] = self.tags[BabelCategory]
        if not languages:
            return categories
        else:
            return [c for c in categories if c.language in languages]

    def main_sense(self, language: Optional[Language] = None) -> Optional[BabelSense]:
        """Get the main BabelSense by importance of this BabelSynset.

        @param language: The language of the the main sense (default None).
        @type language: Optional[Language]

        @return: The main sense of this Babel synset.
        @rtype: Optional[BabelSense]
        """
        if not language:
            return self.main_sense_preferably_in(None)
        if not self._is_loaded:
            self._load()
        main_senses = self.main_senses(language)
        return main_senses[0] if main_senses else None

    def main_sense_preferably_in(
        self, language: Optional[Language]
    ) -> Optional[BabelSense]:
        """Get the main BabelSense by importance of this BabelSynset, preferrably
        in the given language.

        @param language: The preferred language of the main sense.
        @type language: Optional[Language]

        @return: The senses of this Babel synset in a specific language sorted by importance.
        @rtype: Optional[BabelSense]
        """
        if not self._is_loaded:
            self._load()
        if language:
            main_senses_by_language = self.main_senses(language)
            if main_senses_by_language:
                return main_senses_by_language[0]
            if language is not Language.EN:
                main_senses_by_language = self.main_senses(Language.EN)
                if main_senses_by_language:
                    return main_senses_by_language[0]
        if self._target_langs:
            for other_language in self._target_langs:
                main_senses_by_language = self.main_senses(other_language)
                if main_senses_by_language:
                    return main_senses_by_language[0]
        for other_language in Language:
            main_senses_by_language = self.main_senses(other_language)
            if main_senses_by_language:
                return main_senses_by_language[0]
        return None

    def main_senses(self, language: Language) -> List[BabelSense]:
        """Collect distinct BabelSenses sorted by importance to this
        BabelSynset for a given language.

        @param language: The search language.
        @type language: Language

        @return: The senses of this Babel synset in a specific language sorted by importance.
        @rtype: List[BabelSense]
        """
        if not self._is_loaded:
            self._load()
        if language not in self._main_senses:
            senses_by_language = self.senses(language)
            main_senses_by_language = []

            # crea un'associazione lemma -> elenco di sensi associati a quel lemma
            lemma2senses = defaultdict(list)

            # alla fine aggiungo i lemmi dalle redirezioni nel caso non sia mai stato conteggiato
            redirections = set()

            # aggiungo i lemmi dalle automatiche
            automatic_senses = set()

            word_atlas_senses = set()

            for bs in senses_by_language:

                if bs.source is BabelSenseSource.WORD_ATLAS:
                    word_atlas_senses.add(bs)
                    continue
                if bs.source.is_redirection:
                    redirections.add(bs)
                    continue
                if bs.source.is_automatic_translation(bs.language):
                    automatic_senses.add(bs)
                    continue
                normalized_lemma_lc = bs.normalized_lemma.lower()
                lemma2senses[normalized_lemma_lc].append(bs)

            # crea un'associazione lemma -> elenco delle redirezioni associate a quel lemma
            lemma2redisenses = defaultdict(list)
            for bs in redirections:
                normalized_lemma_lc = bs.normalized_lemma.lower()
                if normalized_lemma_lc in lemma2senses:
                    continue
                lemma2redisenses[normalized_lemma_lc].append(bs)

            lemma2senses.update(lemma2redisenses)

            lemma2auto = defaultdict(list)
            all_lemma2auto = defaultdict(list)

            for bs in automatic_senses:
                normalized_lemma_lc = bs.normalized_lemma.lower()
                all_lemma2auto[normalized_lemma_lc].append(bs)
                if normalized_lemma_lc in lemma2senses:
                    continue
                lemma2auto[normalized_lemma_lc].append(bs)

            lemma2senses.update(lemma2auto)

            for bs in word_atlas_senses:
                normalized_lemma_lc = bs.normalized_lemma.lower()
                lemma2senses[normalized_lemma_lc].append(bs)

            lemmas = list(lemma2senses.keys())

            # crea la lista di sensi rappresentativi (main senses), uno per ogni lemma
            for lemma in lemmas:
                l = lemma2senses[lemma]

                l.sort(key=BabelSenseComparator())
                main_senses_by_language.append(l[0])

            # Sort by BabelSenseSource
            # ordina i lemmi del synset per numero di sensi associati
            # (prima quelli con piu' sensi, poi quelli con meno sensi)
            def compare(a: BabelSense, b: BabelSense):
                a_weight = 3 if a.source is BabelSenseSource.WN else 0
                b_weight = 3 if b.source is BabelSenseSource.WN else 0
                a_freq = len(lemma2senses[a.normalized_lemma.lower()]) + a_weight
                b_freq = len(lemma2senses[b.normalized_lemma.lower()]) + b_weight

                b_word_atlas1 = a.source is BabelSenseSource.WORD_ATLAS
                b_word_atlas2 = b.source is BabelSenseSource.WORD_ATLAS

                if not b_word_atlas1 and b_word_atlas2:
                    return 1
                if b_word_atlas1 and not b_word_atlas2:
                    return -1

                quality = a.lemma.lemma_type.value - b.lemma.lemma_type.value
                if quality != 0:
                    return quality

                if a_freq > b_freq:
                    return -1
                if a_freq < b_freq:
                    return 1

                a_weight_tr = (
                    len(all_lemma2auto[a.normalized_lemma.lower()])
                    if a.normalized_lemma.lower() in all_lemma2auto
                    else 0
                )
                b_weight_tr = (
                    len(all_lemma2auto[b.normalized_lemma.lower()])
                    if b.normalized_lemma.lower() in all_lemma2auto
                    else 0
                )

                if a_weight_tr > b_weight_tr:
                    return -1
                if a_weight_tr < b_weight_tr:
                    return 1
                return cmp(a.normalized_lemma.lower(), b.normalized_lemma.lower())

            main_senses_by_language.sort(key=cmp_to_key(compare))
            self._main_senses[language] = main_senses_by_language
        return self._main_senses[language]

    def senses(
        self,
        language: Optional[Language] = None,
        source: Optional[BabelSenseSource] = None,
    ) -> List[BabelSense]:
        """Get the senses contained in this Synset.

        @param language: The language used to search (default None).
        @type language: Optional[Language]
        @param source: The source of the senses to be retrieved (default None).
        @type source: Optional[BabelSenseSource]

        @return: The senses of this synset.
        @rtype: List[BabelSense]
        """
        if not self._is_loaded:
            self._load()

        return [
            s
            for s in self._senses
            if (not source or s.source is source)
            and (not language or s.language is language)
        ]

    def senses_by_word(
        self,
        lemma: str,
        language: Language,
        *sources: BabelSenseSource,
        normalized: Optional[bool] = False,
    ) -> List[BabelSense]:
        """Gets the Senses for the input word in the given language.

        @param lemma: Lemma of the sense.
        @type lemma: str
        @param language: Language of the sense.
        @type language: Language
        @param sources: Possible sources for the sense.
        @type sources: BabelSenseSource

        @param normalized: Use normalization? (default False)
        @type normalized: Optional[bool]

        @return: The Senses for the input word in the given language.
        @rtype: List[BabelSense]
        """
        if not self._is_loaded:
            self._load()
        lemma = lemma.replace(" ", "_")
        result = []
        for sense in self._senses:
            lemma_normalized = None
            if normalized:
                lemma_normalized = flatten_to_ascii(sense.normalized_lemma)

            if (
                (
                    sense.normalized_lemma.lower() == lemma.lower()
                    or (lemma_normalized and lemma_normalized.lower() == lemma.lower())
                )
                and (not language or sense.language == language)
                and (not sources or sense.source in sources)
            ):
                result.append(sense)
        return result

    def to_uris(
        self, resource: BabelExternalResource, *languages: Language
    ) -> List[str]:
        """Return the URIs of the various senses in the given languages
        in the synset for a given ExternalResource.

        @param resource: The external resource.
        @type resource: BabelExternalResource
        @param languages: The languages of interest.
        @type languages: Language

        @return: The URIs to the external resource.
        @rtype: List[str]
        """
        if not self._is_loaded:
            self._load()
        uris = []
        for s in self.senses():
            uri = s.to_uri(resource)
            if uri and (not languages or s.language in languages):
                uris.append(uri)
        return uris

    def to_str(self, *languages: Language) -> str:
        """Return the string representation of the BabelSenses of
        this BabelSynset only for a specific set of languages.

        @param languages: The languages to use for the string representation.
        @type languages: Language

        @return: A stringified representation of this Babel synset using only the senses in a specific set of languages.
        @rtype: str
        """
        if not self._is_loaded:
            self._load()
        return (
            "{ "
            + ", ".join(
                [
                    str(s)
                    for s in self._senses
                    if not languages or s.language in languages
                ]
            )
            + " }"
        )

    def lemmas(
        self, language: Language, *admitted_types: BabelLemmaType
    ) -> List[BabelLemma]:
        """Return the lemmas in this BabelSynset sorted by relevance and type.

        @param language: The language of interest.
        @param admitted_types: The types for the requested synset lemmas.

        @return: The lemmas in the synset sorted by relevance and type.
        """
        if not self._is_loaded:
            self._load()
        admitted_type_set = set(admitted_types if admitted_types else BabelLemmaType)
        types = {}
        filtered_senses = self.senses(language)
        filtered_senses.sort(key=BabelSenseComparator())

        counter = Counter()

        for s in filtered_senses:
            counter.update([s.normalized_lemma])
            if s.normalized_lemma not in types:
                types[s.normalized_lemma] = BabelLemmaType.from_babel_sense_source(
                    s.source, s.language
                )
        lemmas = [
            l[0] for l in counter.most_common() if types[l[0]] in admitted_type_set
        ]
        lemmas.sort(key=lambda l: types[l])
        return [BabelLemma(l, types[l]) for l in lemmas]

    def main_gloss(self, language: Optional[Language] = None) -> Optional[BabelGloss]:
        """Get the main Gloss in the given language, if any.

        @param language: The gloss language (default None).

        @return: The main Gloss of the synset.
        """
        if not self._is_loaded:
            self._load()
        glosses = self.glosses(language)
        return glosses[0] if len(glosses) > 0 else None

    def glosses(
        self,
        language: Optional[Language] = None,
        source: Optional[BabelSenseSource] = None,
    ) -> List[BabelGloss]:
        """Collect all Glosses for this Synset.

        @param language: The gloss language (default None).
        @param source: The gloss source (default None).

        @return: A list of BabelGlosses.
        """
        if not self._is_loaded:
            self._load()
        return [
            g
            for g in self._get_glosses()
            if (not language or g.language == language)
            and (not source or g.source == source)
        ]

    def main_example(
        self, language: Optional[Language] = None
    ) -> Optional[BabelExample]:
        """Get the main Example for this Synset.

        @param language: The example language (default None).

        @return: The main Example.
        """
        if not self._is_loaded:
            self._load()
        try:
            return self.examples(language)[0]
        except IndexError:
            return None

    def examples(
        self,
        language: Optional[Language] = None,
        source: Optional[BabelSenseSource] = None,
    ) -> List[BabelExample]:
        """Collect all Examples for this Synset.

        @param language: The example language (default None).
        @param source: The example source (default None).
        """
        if not self._is_loaded:
            self._load()
        return [
            e
            for e in self._get_examples()
            if (not language or e.language == language)
            and (not source or e.source == source)
        ]

    def wordnet_offset_map_from(
        self, from_version: WordNetVersion
    ) -> Dict[WordNetSynsetID, List[WordNetSynsetID]]:
        """Obtain a map from WordNetSynsetID of the input WordNetVersion to
        the current version of WordNet (3.0 as of 2016).

        @param from_version: The source WordNet version.

        @return: A map from WordNetSynsetID to list of WordNetSynsetID.
        """
        if not self._is_loaded:
            self._load()
        mapping = {}
        for wn in self._wn_offsets:
            for wn_from in wn.to_version(from_version):
                mapping[wn_from] = wn_from.to_version(WordNetVersion.WN_30)
        return mapping

    def wordnet_offset_map_to(
        self, to_version: WordNetVersion
    ) -> Dict[WordNetSynsetID, List[WordNetSynsetID]]:
        """Obtain a map from the current version of WordNet (3.0 as of 2016) to
        WordNetSynsetIDs of the input WordNetVersion.

        @param to_version: The target WordNet version.

        @return: A map from WordNetSynsetID to list of WordNetSynsetID.
        """
        if not self._is_loaded:
            self._load()
        mapping = {}
        for wn in self._wn_offsets:
            mapping[wn] = wn.to_version(to_version)
        return mapping

    def outgoing_edges(
        self, *relation_types: BabelPointer
    ) -> List[BabelSynsetRelation]:
        """Collect all Synset edges incident on this Synset.

        @param relation_types: The types of the edges connecting this synset to other synsets

        @return: The SynsetRelations incident on this Synset
        """
        if not self._is_loaded:
            self._load()
        output_edges = []
        if self._edges is None:
            # noinspection PyBroadException
            try:
                self._edges = self.id.outgoing_edges
            except Exception:
                self._edges = []
        if not relation_types:
            return self._edges

        for edge in self._edges:
            for p in relation_types:

                if (
                    p.relation_group == edge.pointer.relation_group
                    and (
                        p == BabelPointer.ANY_HYPERNYM
                        or p == BabelPointer.ANY_MERONYM
                        or p == BabelPointer.ANY_HOLONYM
                        or p == BabelPointer.ANY_HYPONYM
                    )
                ) or edge.pointer.symbol.lower() == p.symbol.lower():
                    output_edges.append(edge)
                    break

                # if p is BabelPointer.ANY_HYPERNYM:
                #     if edge.pointer.is_hypernym:
                #         output_edges.append(edge)
                #         break
                # elif p is BabelPointer.ANY_MERONYM:
                #     if edge.pointer.is_meronym:
                #         output_edges.append(edge)
                #         break
                # elif p is BabelPointer.ANY_HOLONYM:
                #     if edge.pointer.is_holonym:
                #         output_edges.append(edge)
                #         break
                # elif p is BabelPointer.ANY_HYPONYM:
                #     if edge.pointer.is_hyponym:
                #         output_edges.append(edge)
                #         break
                # elif edge.pointer is p:
                #     output_edges.append(edge)
                #     break
        return output_edges

    @property
    def type(self) -> SynsetType:
        """The kind of synset."""
        if not self._is_loaded:
            self._load()
        return self._type

    def retain_senses(self, *pred: Callable[[BabelSense], bool]) -> bool:
        """Retain all the senses which pass the predicate tests.

        @param pred: The predicates used to decide whether to keep each sense in the synset.

        @return: True if at least one sense is left in the synset, False otherwise.
        """
        if not self._is_loaded:
            self._load()
        self._senses = [s for s in self._senses if all(p(s) for p in pred)]
        return len(self._senses) > 0

    def get_string_tags(self) -> List[StringTag]:
        """The tags of this synset as string"""
        if not self._is_loaded:
            self._load()
        return [] if self._tags is None else self._tags.get(StringTag, [])

    @property
    def tags(self) -> Optional[Mapping[Type[Tag], Union[SynsetType, List[Tag]]]]:
        """The tags of this synset"""
        if not self._is_loaded:
            self._load()

        return self._tags


class _OnlineBabelSynset(BabelSynset):
    """Online implementation of a BabelSynset.

    @ivar synset_id: The id of the synset.
    @type synset_id: BabelSynsetID
    @ivar target_langs: The language filter.
    @type synset_id: Set[Language]
    """

    def __init__(self, synset_id: BabelSynsetID, target_langs: Set[Language]):
        """init method
        @param synset_id: The id of the synset.
        @param target_langs: The language filter.
        """
        super().__init__(synset_id, target_langs)

    def _get_examples(self):
        if not self._is_loaded:
            self._load()
        return self._examples

    def _get_glosses(self):
        if not self._is_loaded:
            self._load()
        return self._glosses

    @property
    def translations(self):
        if not self._is_loaded:
            self._load()
        return self._translations.copy()

    @property
    def images(self):
        if not self._is_loaded:
            self._load()
        return self._images

    def _load(self):
        from pybabelnet.tag_utils import parse_tag
        from pybabelnet.conf import _config

        key = _config.RESTFUL_KEY
        packet = _restful.RESTfulPacket(_restful.RESTfulCallType.GET_PRIVATESYNSET, key)
        packet.synset_ids = [self.id]
        packet.target_languages = list(self._target_langs)
        outserver = _restful.send_request(packet)
        if not outserver:
            raise RuntimeError("No response from BabelNet RESTful server")
        try:
            if not _restful.check_error_code(outserver):

                def synset_decoder(dct: dict):
                    if dct.keys() == {"id", "pos", "source"}:
                        sid = BabelSynsetID(dct["id"])
                        sid.pos = dct["pos"]
                        return sid

                    elif dct.keys() == {"audios", "transcriptions"}:
                        return BabelSensePhonetics(
                            set(dct["audios"]), set(dct["transcriptions"])
                        )

                    elif dct.keys() == {"lemma", "language", "filename"}:
                        return BabelAudio(
                            dct["lemma"], Language[dct["language"]], dct["filename"]
                        )

                    elif dct.keys() == {"start", "end", "id", "word"}:
                        dct["synset_id"] = dct["id"]
                        del dct["id"]
                        return BabelTokenId(**dct)

                    elif dct.keys() == {"start", "end", "lemma"}:
                        return BabelTokenWord(**dct)

                    elif dct.keys() == {
                        "versionMapping",
                        "version",
                        "id",
                        "pos",
                        "source",
                    }:
                        vm = {
                            WordNetVersion[k]: v
                            for k, v in dct["versionMapping"].items()
                        }
                        wn = WordNetSynsetID(
                            id_str=dct["id"], version=dct["version"], mapping=vm
                        )
                        wn.pos = dct["pos"]
                        return wn

                    elif dct.keys() == {
                        "source",
                        "sourceSense",
                        "language",
                        "gloss",
                        "tokens",
                    }:
                        return BabelGloss(
                            source=BabelSenseSource[dct["source"]],
                            source_sense=dct["sourceSense"],
                            language=Language[dct["language"]],
                            gloss=dct["gloss"],
                            tokens=set(dct["tokens"]),
                        )

                    elif dct.keys() == {
                        "source",
                        "sourceSense",
                        "language",
                        "example",
                        "tokens",
                    }:
                        return BabelExample(
                            source=BabelSenseSource[dct["source"]],
                            source_sense=dct["sourceSense"],
                            language=Language[dct["language"]],
                            example=dct["example"],
                            tokens=set(dct["tokens"]),
                        )
                    elif dct.keys() == {
                        "name",
                        "languages",
                        "urlSource",
                        "license",
                        "thumbUrl",
                        "url",
                        "badImage",
                    }:
                        languages = {Language[l] for l in dct["languages"]}
                        bi = BabelImage(
                            title=dct["name"],
                            language="EN",
                            source=dct["urlSource"],
                            license_=dct["license"],
                            thumb_url=dct["thumbUrl"],
                            url=dct["url"],
                            is_bad=dct["badImage"],
                        )
                        bi.languages = languages
                        return bi
                    # This is now handled by parse_tag
                    # elif dct.keys() == {"category", "language"}:
                    #     return BabelCategory(dct["category"], Language[dct["language"]])

                    elif dct.keys() == {"type", "properties"}:
                        if dct["type"] == "BabelSense":
                            dct = dct["properties"]
                            sense = BabelSense(
                                lemma=dct["fullLemma"],
                                language=Language[dct["language"]],
                                pos=POS[dct["pos"]],
                                source=BabelSenseSource[dct["source"]],
                                sensekey=dct["senseKey"],
                                synset=self,
                                yago_url=dct.get("YAGOURL", None),
                                key_sense=dct.get("bKeySense", False),
                                phonetics=dct.get("pronunciations", None),
                            )
                            if "idSense" in dct:
                                sense.id = dct["idSense"]
                            return sense
                        elif dct["type"] == "WordNetSense":
                            dct = dct["properties"]
                            sense = WordNetSense(
                                lemma=dct["fullLemma"],
                                language=Language[dct["language"]],
                                pos=POS[dct["pos"]],
                                sensekey=dct["senseKey"],
                                synset=self,
                                yago_url=dct.get("YAGOURL", None),
                                wordnet_sense_number=dct.get(
                                    "wordNetSenseNumber", None
                                ),
                                wordnet_offset=dct.get("wordNetOffset", None),
                                wordnet_synset_position=dct.get(
                                    "wordNetSynsetPosition", None
                                ),
                                key_sense=dct.get("bKeySense", False),
                                phonetics=dct.get("pronunciations", None),
                                source=BabelSenseSource[dct["source"]],
                            )
                            if "idSense" in dct:
                                sense.id = dct["idSense"]
                            return sense

                    elif dct.keys() >= {
                        "senses",
                        "wnOffsets",
                        "glosses",
                        "examples",
                        "images",
                        "synsetType",
                        "categories",
                        "translations",
                        "domains",
                        "lnToCompound",
                        "lnToOtherForm",
                        "filterLangs",
                        "bkeyConcepts",
                    }:

                        bs = _OnlineBabelSynset(self.id, self._target_langs)
                        bs._senses = dct["senses"]
                        bs._wn_offsets = dct["wnOffsets"]
                        bs._glosses = dct["glosses"]
                        bs._examples = dct["examples"]
                        bs._images = dct["images"]
                        bs._type = SynsetType[dct["synsetType"]]
                        bs._translations = dict(dct["translations"])
                        for k in bs._translations:
                            bs._translations[k] = OrderedSet(bs._translations[k])
                        bs._domains = {
                            BabelDomain[k]: v for k, v in dct["domains"].items()
                        }
                        bs._target_langs = OrderedSet(
                            Language[l] for l in dct["filterLangs"]
                        )
                        bs._key_concept = dct["bkeyConcepts"]
                        bs._frame_id = (
                            parse_tag(dct["frameID"]) if "frameID" in dct else None
                        )

                        bs._synset_degree = dct["synsetDegree"] if "synsetDegree" in dct else -1

                        # QcodeID parsing
                        if "qCodeIDs" in dct:
                            bs._qcode_ids = list(
                                QcodeID(e["id"]) for e in dct["qCodeIDs"]
                            )

                        # Tag handling
                        tags = [parse_tag(tag) for tag in dct.get("tags", [])]
                        bs._tags = dict()
                        for tag in tags:
                            tagtype = type(tag)
                            if tagtype == SynsetType:
                                bs._tags[tagtype] = tag
                            else:
                                bs._tags.setdefault(tagtype, []).append(tag)
                        return bs

                    else:
                        return dct

                babel_synset: _OnlineBabelSynset = json.loads(
                    outserver, object_hook=synset_decoder
                )
            else:
                raise RuntimeError(_restful.print_error_message(outserver))
        except json.JSONDecodeError:
            raise RuntimeError("Cannot decode JSON from RESTFul response")
        # In Java te lo scordi questo B-)
        self.__dict__ = babel_synset.__dict__
        self._is_loaded = True

    @property
    def synset_degree(self) -> int:
        if not self._is_loaded:
            self._load()
        if self._synset_degree == -1:
            raise UnsupportedOnlineError("synset_degree")
        return self._synset_degree


class _OfflineBabelSynset(BabelSynset):
    """
    Offline implementation of a BabelSynset.

    @param synset_id : The BabelSynsetID of the synset to build.
    @param wn_offsets : The WordNet synset IDs.
    @param senses : The synset's senses.
    @param translation_mappings : The mappings for translations.
    @param images : A list of images for the synset.
    @param categories : A list of categories for the synset.
    @param synset_type : The type of synset.
    @param domains : The domain information for the synset.
    @param ids_by_license : The list of InternalBabelSynsetIDs that make up the synset.
    @param target_langs : The languages to be retrieved.
    @param key_concept : True if the synset is a key concept.
    @param translations_index : The translations index.
    """

    def __init__(
        self,
        synset_id: BabelSynsetID,
        wn_offsets: List[WordNetSynsetID],
        senses: List[BabelSense],
        translation_mappings: List[str],
        images: List[BabelImage],
        categories: List[BabelCategory],
        synset_type: SynsetType,
        domains: Dict[BabelDomain, float],
        ids_by_license: List,
        target_langs: Set[Language],
        key_concept: bool,
        translations_index: Dict[int, BabelSense],
        string_tags: Optional[Sequence[StringTag]] = None,
        sense_tags: Optional[Sequence[Tag]] = None
    ):
        """init method
         @param synset_id : The BabelSynsetID of the synset to build.
         @type synset_id: BabelSynsetID
         @param wn_offsets : The WordNet synset IDs.
         @type wn_offsets: List[WordNetSynsetID]
         @param senses : The synset's senses.
         @type senses: List[BabelSense]
         @param translation_mappings : The mappings for translations.
         @type translation_mappings: List[str]
         @param images : A list of images for the synset.
         @type images: List[BabelImage]
         @param categories : A list of categories for the synset.
         @type categories: List[BabelCategory]
         @param synset_type : The type of synset.
         @type synset_type: SynsetType
         @param domains : The domain information for the synset.
         @type domains: Dict[BabelDomain, float]
         @param ids_by_license : The list of InternalBabelSynsetIDs that make up the synset.
         @type ids_by_license: List
         @param target_langs : The languages to be retrieved.
         @type target_langs: Set[Language]
         @param key_concept : True if the synset is a key concept.
         @type key_concept: bool
         @param translations_index : The translations index.
         @type translations_index: Dict[int, BabelSense]

         @param string_tags: A list of StringTag
         @type string_tags: Optional[Sequence[StringTag]]
         @param sense_tags: A list of tags
         @type sense_tags: Optional[Sequence[Tag]]
        """
        super().__init__(synset_id, target_langs)
        self._wn_offsets = wn_offsets
        self._senses = senses
        if images is not None:
            images.sort(key=BabelImageComparator())
            self._images = images
        else:
            self._images = None
        self._categories = categories
        self._translation_mappings = translation_mappings
        self._type = synset_type
        self._domains = domains
        self._ids_by_license = ids_by_license
        self._loaded = True
        self._key_concept = key_concept
        self._translations_index = translations_index

        # Tag runtime population
        self._tags = {}
        if categories:
            self._tags.setdefault(BabelCategory, []).extend(categories)
        self._tags.setdefault(SynsetType, synset_type)
        self._tags.setdefault(BabelDomain, []).extend(domains.keys())
        if string_tags:
            self._tags.setdefault(StringTag, []).extend(string_tags)
        if key_concept:
            self._tags[Usage] = Usage.KEY_CONCEPT
        if sense_tags:
            for sense_tag in sense_tags:
                self._tags.setdefault(type(sense_tag), []).append(sense_tag)

    @property
    def images(self):
        if self._images is None:
            self._images = api.images(self.id)
        return self._images.copy()

    @property
    def translations(self):
        if self._translations is None:
            # Building relations
            self._translations = defaultdict(OrderedSet)
            for translation_mapping in self._translation_mappings:
                split = translation_mapping.split("_")
                if len(split) != 2:
                    raise RuntimeError(
                        "Invalid translation mapping: " + translation_mapping
                    )
                source = int(split[0])
                target = int(split[1])
                # if we have target languages
                if (
                    source not in self._translations_index
                    or target not in self._translations_index
                ):
                    continue
                self._translations[self._translations_index[source]].add(
                    self._translations_index[target]
                )
            # keeps only translations with a certain score
            return self._translations.copy()
        return {}

    @property
    def synset_degree(self) -> int:
        return self._valid_degree()

    def _get_examples(self):
        if self._examples is None:
            # init the example
            self._examples = api.examples(
                self.id, self._target_langs, *self._ids_by_license
            )
        self._examples.sort(key=BabelExampleComparator())
        return self._examples

    def _get_glosses(self):
        if self._glosses is None:
            # init the example
            self._glosses = api.glosses(
                self.id, self._target_langs, *self._ids_by_license
            )
        self._glosses.sort(key=BabelGlossComparator())
        return self._glosses

    def _load(self):
        pass


@comparator
class _InternalBabelSynsetComparator:
    """
    Comparator for BabelSynsets that
        - puts WordNet synsets first;
        - sorts WordNet synsets based on the sense number of a specific input word (see the constructor);
        - sorts Wikipedia synsets based on their degree and lexicographically based on their main sense
    """

    def __init__(self, word: Optional[str] = None, language: Language = Language.EN):
        """init method
        @param word: the word to set for this instance of the comparator. It will be used to compare synsets based on the correlation with this word (default None).
        @type word: Optional[str]
        @param language: the language to use for the comparation.
        @type language: Language
        """
        self._word = word  # The lemma used to sort synsets
        self._language = language  # Language used to sort synsets

    @classmethod
    def _valid_degree(self, bs: BabelSynset) -> int:
        if bs.synset_degree != -1: return bs.synset_degree

        return len(
            [
                g
                for g in bs.outgoing_edges()
                if g.language not in [Language.CEB, Language.SH, Language.SR]
            ]
        )


    @staticmethod
    def _compare_by_edge_then_main_sense(b1: BabelSynset, b2: BabelSynset) -> int:
        """
        @param b1: First BabelSynset.
        @param b2: Second BabelSynset.

        @return: Compare result.
        """
        bsc = BabelSenseComparator()
        result = b2._valid_degree() - b1._valid_degree()
        if result == 0:
            mainsense_b1 = b1.main_sense(Language.EN)
            mainsense_b2 = b2.main_sense(Language.EN)

            if not mainsense_b1 and mainsense_b2:
                return -1
            if not mainsense_b2 and mainsense_b1:
                return 1
            if not mainsense_b1 and not mainsense_b2:
                return 0
            return bsc.compare(mainsense_b1, mainsense_b2)
        return result

    def compare(self, b1: BabelSynset, b2: BabelSynset) -> int:
        """
        Compare two BabelSynset(s)

        @param b1: First BabelSynset.
        @param b2: Second BabelSynset.

        @return: Compare result.
        """
        if not isinstance(b1, BabelSynset) or not isinstance(b2, BabelSynset):
            return NotImplemented
        if b1.pos is not b2.pos:
            return POS.compare_by_pos(b1.pos, b2.pos)
        if not self._word:
            return self._compare_by_edge_then_main_sense(b1, b2)

        b_wordnet1 = BabelSenseSource.WN in b1.sense_sources
        b_wordnet1 &= (
            True
            if self._language is Language.EN
            and b1.senses_by_word(self._word, Language.EN, BabelSenseSource.WN)
            else False
        )

        b_wordnet2 = BabelSenseSource.WN in b2.sense_sources
        b_wordnet2 &= (
            True
            if self._language is Language.EN
            and b2.senses_by_word(self._word, Language.EN, BabelSenseSource.WN)
            else False
        )

        # if the two synsets come from WordNet and contain the lemma in English
        if b_wordnet1 and b_wordnet2:
            # both synsets are in the WordNet: sort based on the sense number
            # of the senses of interest
            s_number1 = 1000
            s_number2 = 1000
            for s1 in b1.senses():
                if (
                    s1.full_lemma.lower() == self._word.lower()
                    and s1.source is BabelSenseSource.WN
                ):
                    # Casting in Python... hahha
                    wn1: WordNetSense = s1
                    if s_number1 > wn1.sense_number:
                        s_number1 = wn1.sense_number
            for s2 in b2.senses():
                if (
                    s2.full_lemma.lower() == self._word.lower()
                    and s2.source is BabelSenseSource.WN
                ):
                    # Casting in Python... hahha
                    wn2: WordNetSense = s2
                    if s_number2 > wn2.sense_number:
                        s_number2 = wn2.sense_number
            # do the magic ;)
            return s_number1 - s_number2
        # if is WordNet and the senseKey is like "word"
        elif b_wordnet1:
            return -1
        elif b_wordnet2:
            return 1

        result = b2._valid_degree() - b1._valid_degree()
        if result != 0:
            return result

        # synsets without WordNet-lemma matching
        bsc = BabelWordSenseComparator(self._word)

        # compare the remaining types of senses
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
        b1senses.sort(key=bsc)
        if not b1senses and not b2senses:
            # sort by edge and EN mainSense
            return self._compare_by_edge_then_main_sense(b1, b2)

        if not b1senses:
            return 1
        if not b2senses:
            return -1

        result = bsc.compare(b1senses[0], b2senses[0])
        if result == 0:
            # sort by number of relations
            return self._compare_by_edge_then_main_sense(b1, b2)
        return result


class BabelSynsetComparator(_InternalBabelSynsetComparator):
    """Comparator for BabelSynsets that:
        - puts WordNet synsets first
        - sorts WordNet synsets based on the sense number of a specific input word
        - sorting Wikipedia synsets lexicographically based on their main sense
    """

    def __init__(self, word: Optional[str] = None, language: Language = Language.EN):
        """init method
        @param word: the word to set for this instance of the comparator. It will be used to compare synsets based on the correlation with this word (default None).
        @type word: Optional[str]
        @param language: the language to use for the comparation (default Langauge.EN).
        @type language: Language
        """
        super(BabelSynsetComparator, self).__init__(word=word, language=language)

    def compare(self, b1: BabelSynset, b2: BabelSynset) -> int:

        if self._word is None:
            return self._compare_by_edge_then_main_sense(b1, b2)

        scoreB1 = self.__synset_score(b1)
        scoreB2 = self.__synset_score(b2)

        compare = cmp(scoreB1, scoreB2)
        return (
            compare
            if compare != 0
            else super(BabelSynsetComparator, self).compare(b1, b2)
        )

    def __synset_score(self, synset: BabelSynset) -> int:

        normalized = True
        automaticTranslation = True

        for sense in synset.senses(self._language):
            simpleWord = self._word.replace(" ", "_").lower()
            simpleLemma = sense.normalized_lemma.replace(" ", "_").lower()
            fullLemma = sense.full_lemma.replace(" ", "_").lower()

            # If the simple lemma or the full lemma are equals to the input word the synset is not from normalization
            if simpleLemma == simpleWord or fullLemma == simpleWord:
                normalized = False
                # If the source of the sense is not from automatic translation the synset is not from Automatic Translation
                if not sense.is_automatic_translation:
                    automaticTranslation = False
                    break

        if not normalized and not automaticTranslation:
            return -3
        else:
            # A very not confusing Python feature: bool are 0 and 1 ints, so we can subtract 1 to them to return -1 or -2
            return automaticTranslation - 2


__all__ = ["BabelSynsetComparator", "SynsetType", "BabelSynset"]
