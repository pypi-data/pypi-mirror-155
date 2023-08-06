"""This module contains enumerations used in the _index module."""

from aenum import AutoNumberEnum


class BabelNetIndexField(AutoNumberEnum):
    """Fields used to index BabelSynset's and BabelSense's in
    the Lucene index."""

    ID = ()
    """Id reference attribute type."""

    SENSE_ID = ()
    """Sense id."""

    SOURCE = ()
    """Synset source: WordNet, Wikipedia, WordNet + Wikipedia."""

    WORDNET_OFFSET = ()
    """Connectionto one or more WordNet offsets."""

    OLD_WORDNET_OFFSET = ()
    """Connection to one or more old WordNet offsets."""

    MAIN_SENSE = ()
    """Main sense of a BabelSynset."""

    POS = ()
    """Part of speech."""

    LEMMA = ()
    """All lemmas of the BabelSynset(cased)."""

    LEMMA_TOLOWERCASE = ()
    """All lemmas of the BabelSynset(normalized to lowercase)."""

    LANGUAGE_LEMMA_NORMALIZER = ()
    """Concatenation of language + lemma normalized for exact 
    search(Unicode text)."""

    LEMMA_SOURCE = ()
    """Sense source: WordNet, Wikipedia, WordNet translation, 
    Wikipedia translation."""

    LEMMA_LANGUAGE = ()
    """Language of lemmas."""

    LEMMA_SENSEKEY = ()
    """Sensekeys for lemmas mapping to WordNet."""

    OLD_LEMMA_SENSEKEY = ()
    """Old sensekeys for lemmas mapping to WordNet."""

    LANGUAGE_LEMMA = ()
    """Concatenation of language + lemma for exact search."""

    LEMMA_WEIGHT = ()
    """Weights of translations."""

    LEMMA_FREQUENCE = ()
    """Sense frequency in Wikipedia."""

    LEMMA_NUMBER = ()
    """Sense number in WordNet."""

    OLD_LEMMA_NUMBER = ()
    """Sense number in previous WordNet."""

    TRANSLATION_MAPPING = ()
    """A one - to - many relation between a term and its translations."""

    RELATION = ()
    """Relation with other synsets."""

    TYPE = ()
    """Entities / concepts."""

    IMAGE = ()
    """Images."""

    CATEGORY = ()
    """Categories."""

    GLOSS = ()
    """Glosses."""

    EXAMPLE = ()
    """Examples."""

    DOMAIN = ()
    """Domains."""

    DOMAIN_WEIGHT = ()
    """Domain weight."""

    SCORE = ()
    """Confidence of mapping between different versions of 
    WordNet.Range 0 - 100.."""

    PRONU_AUDIO = ()
    """Audio."""

    PRONU_TRANSC = ()
    """Pronunciation transcription."""

    FREEBASE_ID = ()
    """Freebase ID."""

    YAGO_URL = ()
    """YAGO URL."""

    SURFACE = ()
    """All surface lemma of the BabelSynset(cased)."""

    SURFACE_LANGUAGE = ()
    """Language of surfaces."""

    LICENSE_ID = ()
    """License ID."""

    KEY_CONCEPT = ()
    """Key concept of the BabelSynset."""

    VERSION = ()
    """BabelNet version."""

    ID_SENSE = ()
    """The sense identifier."""

    LOCALE_TAG = ()
    """The locale tag identifier"""

    VERBATLAS_FRAME_ID = ()
    """The VerbAtlas frame id"""

    QCODE_ID = ()
    """The Qcode id"""

    SYNSET_DEGREE = ()
    """The synset degree"""

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class BabelNetIndexImageField(AutoNumberEnum):
    """Fields used to index BabelImage's Lucene index."""

    ID = ()
    """Id reference attribute type."""

    SOURCE = ()
    """WordNet, Wikipedia, OmegaWiki etc.."""

    LANGUAGE = ()
    """The language of WikiCommons page."""

    TITLE = ()
    """Title image."""

    URL = ()
    """URL Image."""

    URL_THUMBNAIL = ()
    """Thumbnail Url."""

    LICENSE = ()
    """License image."""

    DATE = ()
    """Date."""

    BADIMAGE = ()
    """is bad Image."""

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
