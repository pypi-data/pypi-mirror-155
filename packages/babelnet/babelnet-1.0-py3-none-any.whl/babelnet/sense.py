"""This module defines BabelSenses and related data."""

from typing import Optional, Dict

from babelnet._utils import comparator, cmp, normalized_lemma_to_string, lemma_to_string
from babelnet.data.lemma import BabelLemma, BabelLemmaType
from babelnet.data.license import BabelLicense
from babelnet.data.phonetics import BabelSensePhonetics
from babelnet.data.source import BabelSenseSource
from babelnet.language import Language
from babelnet.pos import POS
from babelnet.resources import BabelExternalResource


class BabelSense:
    """A sense in BabelNet, contained in a BabelSynset.

    @ivar id: The id of the sense in the SQL database.
    @ivar full_lemma: The full lemma for this sense.
    @ivar normalized_lemma: The normalized lemma for this sense (lowercase, without parentheses, etc.).
    @ivar language: The language of this sense.
    @ivar pos: The part-of-speech of this sense.
    @ivar source: The source of this lemma: WordNet, Wikipedia, translation, etc.
    @ivar _key_sense: The sensekey of the OmegaWiki, Wikidata, Wiktionary, GeoName, MSTERM or VerbNet sense to which this sense corresponds, if any.
    @ivar _synset: The synset this sense belongs to.
    @ivar synset_id: The synset id this sense belongs to.
    @ivar pronunciations: The set of the audio pronunciations.
    @ivar _lemma: the lemma
    @type _lemma: str
    @ivar _yago_url: the yago url

    """

    _DBPEDIA_PREFIX = "http://dbpedia.org/resource/"
    """The prefix of DBPedia URIs."""

    _YAGO_PREFIX = "http://yago-knowledge.org/resource/"
    """The prefix of YAGO3 URIs."""

    def __init__(
        self,
        lemma: str,
        language: Language,
        pos: POS,
        source: BabelSenseSource,
        sensekey: str,
        synset: "BabelSynset",
        *,
        key_sense: bool = False,
        yago_url: str = None,
        phonetics: BabelSensePhonetics = None
    ):
        """init method
        @param lemma: The full lemma for this sense.
        @param language: The language of this sense.
        @param pos: The part-of-speech of this sense.
        @param source: The source of this lemma: WordNet, Wikipedia, translation, etc.
        @param sensekey: The sensekey of the OmegaWiki, Wikidata, Wiktionary, GeoName, MSTERM or VerbNet sense to which this sense corresponds, if any.
        @param synset: The synset this sense belongs to.
        @type synset: L{BabelSynset <babelnet.synset.BabelSynset>}

        @param key_sense: True if it is a key sense (default False).
        @param yago_url: A link to the corresponding YAGO URI (default None).
        @param phonetics: The set of the audio pronunciations (default None.
        """
        self.full_lemma: str = lemma
        self.language: Language = language
        self.pos: POS = pos
        self.source: BabelSenseSource = source
        self.sensekey: str = sensekey
        self._synset = synset
        self.synset_id = synset.id
        self.normalized_lemma = normalized_lemma_to_string(lemma)
        self._lemma: BabelLemma = BabelLemma(
            lemma=lemma_to_string(lemma),
            lemma_type=BabelLemmaType.from_babel_sense_source(
                source=source, language=language
            ),
        )
        self.id: int = 0
        self._key_sense = key_sense
        self._yago_url = yago_url
        self.pronunciations: Optional[BabelSensePhonetics] = phonetics

    def __str__(self):
        seq = (str(self.source), str(self.language), self.full_lemma)
        return ":".join(seq)

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __hash__(self):
        return hash((self.synset_id, hash(self.full_lemma), hash(self.source)))

    def __eq__(self, other):
        if isinstance(other, BabelSense):
            return (
                self.synset_id == other.synset_id
                and self.full_lemma == other.full_lemma
                and self.source == other.source
                and self.language == other.language
                and (self.sensekey is None or self.sensekey == other.sensekey)
            )
        return False

    # TODO: NO TYPING
    @property
    def synset(self) -> "BabelSynset":
        """The synset the sense belongs to.

        @return: the synset
        @rtype: L{BabelSynset <babelnet.synset.BabelSynset>}
        """
        if not self._synset:
            self._synset = self.synset_id.to_synset()
        return self._synset

    @synset.setter
    def synset(self, value: "BabelSynset"):
        """Set the synset the sense belongs to.

        @param value: The synset the sense belongs to.
        @type value: L{BabelSynset <babelnet.synset.BabelSynset>}
        """
        self._synset = value

    @property
    def license(self) -> BabelLicense:
        """The license for this Babel sense.
        @return: the license
        @rtype: BabelLicense
        """
        return self.source.get_license(self.language)

    @property
    def is_key_sense(self) -> bool:
        """True if it is a key sense.

        @return: True or False
        @rtype: bool
        """
        return self._key_sense

    @property
    def is_automatic_translation(self) -> bool:
        """True if the sense is the result of an automatic translation.
        @return: True or False
        @rtype: bool
        """
        return self.source.is_automatic_translation(self.language)

    @property
    def is_not_automatic_translation(self) -> bool:
        """Returns True if the sense is NOT the result of an automatic translation.
        @return: True or False
        @rtype: bool
        """
        return not self.is_automatic_translation

    @property
    def sense_str(self) -> str:
        """A String-based representation of this BabelSense alternative to the
        "canonical" one obtained using C{__str__}.
        This corresponds to a diesis-like representation if the sense belongs
        to WordNet, e.g. C{'car#n#1'} or C{'funk#n#3'}, or the page otherwise the lemma.

        @return: A string that represents this BabelSense
        @rtype: bool
        """
        return self.full_lemma

    def to_uri(self, resource: BabelExternalResource) -> Optional[str]:
        """Return the URI of the sense for a given ExternalResource.

        @param resource: The external resource.
        @type resource: BabelExternalResource

        @return: The URI to the external resource.
        @rtype: Optional[str]
        """
        return {
            BabelExternalResource.DBPEDIA: self._get_dbpedia_uri(),
            BabelExternalResource.YAGO: self._get_yago_uri(),
            BabelExternalResource.GEONAMES: self._get_geonames_uri(),
            # resource.FRAMENET: self._get_framenet_uri(),
            # resource.VERBNET: self._get_verbnet_uri()
        }[resource]

    def _get_dbpedia_uri(self) -> Optional[str]:
        """Get a link to the corresponding DBPedia URI (None if no
        interlinking is available or possible).

        See also: U{DBPedia interlinking <http://wiki.dbpedia.org/Interlinking>}

        @return: A link to the corresponding DBPedia URI.

        """
        if self.language is Language.EN:
            if self.source in [BabelSenseSource.WIKI, BabelSenseSource.WIKIRED]:
                return (
                    self._DBPEDIA_PREFIX
                    + self.full_lemma[0].upper()
                    + self.full_lemma[1:]
                )
            return None
        return None

    def _get_yago_uri(self) -> Optional[str]:
        """Get a link to the corresponding YAGO URI (None if no
        interlinking is available or possible).

        See also: U{YAGO <http://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/yago/>}

        @return: A link to the corresponding YAGO URI.

        """
        return self._YAGO_PREFIX + self._yago_url if self._yago_url else None

    def _get_geonames_uri(self) -> Optional[str]:
        """Get a link to the corresponding GeoNames URI (None if no
        interlinking is available or possible).

        See also: `GeoNames <http://www.geonames.org/>`_

        @return: A link to the corresponding GeoNames URI.

        """
        if self.source is BabelSenseSource.GEONM:
            return self.source.uri + self.sensekey
        return None

    @property
    def lemma(self) -> BabelLemma:
        """
        Get the lemma of this BabelSense

        @return: the lemma
        @rtype: BabelLemma
        """
        return self._lemma


class WordNetSense(BabelSense):
    """A WordNet sense. Provides WordNet-specific methods.
    @ivar wordnet_offset: The offset of the WordNet sense to which this sense corresponds, if any.
    @ivar sense_number: The sense number of the WordNet if any.
    @ivar position: The position of the WordNet sense to which this sense corresponds.
    @ivar sensekey: The sensekey of the OmegaWiki, Wikidata, Wiktionary, GeoName, MSTERM or VerbNet sense to which this sense corresponds, if any.
    """

    def __init__(
        self,
        lemma: str,
        language: Language,
        pos: POS,
        source: BabelSenseSource,
        sensekey: str,
        synset: "BabelSynset",
        *,
        wordnet_offset: Optional[str] = None,
        wordnet_synset_position: Optional[int] = None,
        wordnet_sense_number: Optional[int] = None,
        **kwargs
    ):
        """init method
        @param lemma: The full lemma for this sense.
        @type lemma: str
        @param language: The language of this sense.
        @type language: Language
        @param pos: The part-of-speech of this sense.
        @type pos: POS
        @param source: The source of this lemma: WordNet, Wikipedia, translation, etc.
        @type source: BabelSenseSource
        @param sensekey: The sensekey of the OmegaWiki, Wikidata, Wiktionary, GeoName, MSTERM or VerbNet sense to which this sense corresponds, if any.
        @type sensekey: str
        @param synset: The synset this sense belongs to.
        @type synset: L{BabelSynset <babelnet.synset.BabelSynset>}

        @param wordnet_offset: The offset of the WordNet sense to which this sense corresponds, if any (default None).
        @type wordnet_offset: Optional[str]
        @param wordnet_synset_position: The position of the WordNet sense to which this sense corresponds (default None).
        @type wordnet_synset_position: Optional[int]
        @param wordnet_sense_number: The sense number of the WordNet if any (default None).
        @type wordnet_sense_number: Optional[int]
        @param kwargs: Optional parameters of BabelSense.
        """
        super().__init__(lemma, language, pos, source, sensekey, synset, **kwargs)
        self.wordnet_offset: Optional[str] = wordnet_offset
        self.sense_number: Optional[int] = wordnet_sense_number
        self.position: Optional[int] = wordnet_synset_position

    @property
    def sense_str(self):
        seq = (self.full_lemma, self.pos.tag, str(self.sense_number))
        return "#".join(seq)


@comparator
class BabelSenseComparator:
    """
    Comparator for BabelSenses that:
        - puts WordNet senses first
        - sorts WordNet senses based on their sense number
        - sorts Wikipedia senses lexicographically
    """

    def _sort_by_parentheses(self, b1: BabelSense, b2: BabelSense) -> int:
        """
        Sort two BabelSenses by parenthesis (senses without parenthesis first).

        @param b1: First BabelSense.
        @type b1: BabelSense
        @param b2: Second BabelSense.
        @type b2: BabelSense

        @return: Compare result.
        @rtype: int
        """

        sourceB1 = b1.source
        sourceB2 = b2.source

        if sourceB1 is not sourceB2:
            # precedence to WIKI vs. other sources
            if sourceB1 is BabelSenseSource.WIKI:
                return -1
            else:
                if sourceB2 is BabelSenseSource.WIKI:
                    return 1

            # sort WIKIRED
            if sourceB1 is BabelSenseSource.WIKIRED:
                return -1
            else:
                if sourceB2 is BabelSenseSource.WIKIRED:
                    return 1

            # sort WIKITR
            if sourceB1 is BabelSenseSource.WIKITR:
                return -1
            else:
                if sourceB2 is BabelSenseSource.WIKITR:
                    return 1

        # if sources are the same or different from the ones checked before
        if sourceB1 is BabelSenseSource.WIKIRED or sourceB1 is BabelSenseSource.WIKITR:
            return cmp(b1.sense_str.lower(), b2.sense_str.lower())

        b_par1 = "(" in b1.sense_str
        b_par2 = "(" in b2.sense_str
        if b_par1 and b_par2:
            return cmp(b1.sense_str.lower(), b2.sense_str.lower())
        elif b_par1:
            return 1
        elif b_par2:
            return -1

        # Wikipedia senses are sorted lexicographically otherwise
        return cmp(b1.sense_str.lower(), b2.sense_str.lower())

    def _sort_wordnet(self, b1: BabelSense, b2: BabelSense):
        """Sort wordnet senses

        @param b1: the first sense
        @param b2: the second sense
        @return: the result of the comparation.
        @rtype: int
        """
        wn1: WordNetSense = b1
        wn2: WordNetSense = b2

        # if different WordNet synsets
        if wn1.wordnet_offset != wn2.wordnet_offset:
            result = wn1.sense_number - wn2.sense_number
            if result == 0:
                # if same wordnet_sense_number  - WN:EN: house WN: EN:business_organization
                # lexicographical sort
                return cmp(wn1.sense_str.lower(), wn2.sense_str.lower())
            else:
                return result
        # if same WordNet synset
        else:
            return wn1.position - wn2.position

    def compare(self, b1: BabelSense, b2: BabelSense) -> int:
        """
        Compare two BabelSense(s)

        @param b1: First BabelSense.
        @type b1: BabelSense
        @param b2: Second BabelSense.
        @type b2: BabelSense

        @return: Compare result.
        @rtype: int
        """
        if not isinstance(b1, BabelSense) or not isinstance(b2, BabelSense):
            return NotImplemented
        if b1.pos is not b2.pos:
            return POS.compare_by_pos(b1.pos, b2.pos)

        b_word_atlas1 = b1.source is BabelSenseSource.WORD_ATLAS
        b_word_atlas2 = b2.source is BabelSenseSource.WORD_ATLAS

        if not b_word_atlas1 and b_word_atlas2:
            return 1
        if b_word_atlas1 and not b_word_atlas2:
            return -1

        b_babelnet1 = b1.source is BabelSenseSource.BABELNET
        b_babelnet2 = b2.source is BabelSenseSource.BABELNET
        if not b_babelnet1 and b_babelnet2:
            return -1
        if b_babelnet1 and not b_babelnet2:
            return 1

        # [1 - WordNet senses]

        b_wordnet1 = b1.source.is_from_wordnet
        b_wordnet2 = b2.source.is_from_wordnet
        # both senses are in the WordNet: sort based on the sense number
        # of the senses of interest
        if b_wordnet1 and b_wordnet2:
            return self._sort_wordnet(b1, b2)
        # WordNet's senses come before Wikipedia's
        elif b_wordnet1:
            return -1
        # ditto
        elif b_wordnet2:
            return 1

        b_wordnet20201 = b1.source == BabelSenseSource.WN2020 or b1.source == BabelSenseSource.OEWN
        b_wordnet20202 = b2.source == BabelSenseSource.WN2020 or b2.source == BabelSenseSource.OEWN
        # both senses are in the WordNet 2020: sort based on the sense number
        # of the senses of interest
        if b_wordnet20201 and b_wordnet20202:
            return self._sort_wordnet(b1, b2)
        # WordNet's senses come before Wikipedia's
        elif b_wordnet20201:
            return -1
        # ditto
        elif b_wordnet20202:
            return 1

        # [2 - Open Multilingual Wordnet senses + VerbNet]

        # sort by source and automatic translations

        b_omwordnet1 = b1.source is BabelSenseSource.VERBNET or (
            b1.source.is_from_multi_wordnet  # FIX, OLDVAL: is BabelSenseSource.OMWN
            and not b1.source.is_automatic_translation(b1.language)
        )
        b_omwordnet2 = b2.source is BabelSenseSource.VERBNET or (
            b2.source.is_from_multi_wordnet  # FIX, OLDVAL: is BabelSenseSource.OMWN
            and not b2.source.is_automatic_translation(b2.language)
        )

        # sort open multiwordnet
        if b_omwordnet1 and b_omwordnet2:
            return cmp(b1.sense_str.lower(), b2.sense_str.lower())
        elif b_omwordnet1:
            return -1
        elif b_omwordnet2:
            return 1

        # sort wiki
        if b1.source is b2.source:
            # NON C'E' LA FREQUENZA
            return self._sort_by_parentheses(b1, b2)

        # sort order by sources (see BabelSenseSource)
        if b1.source is not b2.source:
            b_translation1 = b1.source.is_automatic_translation(b1.language)
            b_translation2 = b2.source.is_automatic_translation(b2.language)

            b_wikired1 = b1.source.is_redirection
            b_wikired2 = b2.source.is_redirection

            if b_translation1 and b_wikired2:
                return 1
            if b_translation2 and b_wikired1:
                return -1

            if b_wikired1 and not b_wikired2:
                return 1
            if not b_wikired1 and b_wikired2:
                return -1

            if b_wikired1 and b_wikired2:
                # NON C'E' LA FREQUENZA
                return cmp(b1.sense_str.lower(), b2.sense_str.lower())

            if b_translation1 and not b_translation2:
                return 1
            elif b_translation2 and not b_translation1:
                return -1

            # FIX
            ordinal_diff = b1.source.ordinal_for_sorting - b2.source.ordinal_for_sorting

            if ordinal_diff == 0:
                return cmp(b1.sense_str.lower(), b2.sense_str.lower())
            return ordinal_diff

            # return b1.source.ordinal_for_sorting - b2.source.ordinal_for_sorting
            # END FIX
        else:
            return cmp(b1.sense_str.lower(), b2.sense_str.lower())


@comparator
class BabelWordSenseComparator(BabelSenseComparator):
    """BabelSenseComparator for BabelSenses with precedence given
    to a certain word.
    @ivar word: The word whose sense numbers are used to sort the BabelSense.
    @type word: Optional[str]
    """

    def __init__(self, word: Optional[str] = None):
        """init method
        @param word: The word whose sense numbers are used to sort the BabelSense (default None).
        @type word: Optional[str]
        """
        self.word: Optional[str] = word

    def _sort_by_parentheses(self, b1: BabelSense, b2: BabelSense) -> int:
        from .synset import SynsetType

        if b1.pos is not b2.pos:
            return POS.compare_by_pos(b1.pos, b2.pos)

        # precedence to the specified word
        if self.word:
            lemmab1 = b1.normalized_lemma
            lemmab2 = b2.normalized_lemma

            if (
                lemmab1.lower() == self.word.lower()
                and not lemmab2.lower() == self.word.lower()
            ):
                return -1
            if (
                not lemmab1.lower() == self.word.lower()
                and lemmab2.lower() == self.word.lower()
            ):
                return 1

            if (
                b1.synset.type is SynsetType.CONCEPT
                and b2.synset.type is SynsetType.NAMED_ENTITY
            ):
                return -1
            if (
                b2.synset.type is SynsetType.CONCEPT
                and b1.synset.type is SynsetType.NAMED_ENTITY
            ):
                return 1
        return super()._sort_by_parentheses(b1, b2)


__all__ = [
    "BabelSense",
    "WordNetSense",
    "BabelSenseComparator",
    "BabelWordSenseComparator",
]
