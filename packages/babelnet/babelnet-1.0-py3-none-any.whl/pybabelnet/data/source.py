"""Sources of BabelSenses in BabelNet."""

from typing import Optional

from aenum import Enum, AutoNumberEnum

from pybabelnet.data.license import BabelLicense
from pybabelnet.language import Language


class BabelSenseSource(Enum):
    """
    Enumeration of the different sources for the BabelNet senses.

    @ivar ordinal_for_sorting: Ordinal for sense sorting.
    @type ordinal_for_sorting: int
    @ivar source_name: Name of the source.
    @type source_name: str
    @ivar _uri: Source URI
    @type _uri: str
    @ivar ordinal: the ordinal
    @type ordinal: int
    """

    BABELNET: "BabelSenseSource" = 4, "BabelNet", "http://babelnet.org", 0
    """Lexicalization from BabelNet itself"""

    WN: "BabelSenseSource" = 1, "WordNet 3.0", "http://wordnet.princeton.edu", 1
    """Lexicalization from WordNet 3.0"""

    OMWN: "BabelSenseSource" = (
        2,
        "Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        2,
    )
    """
    Lexicalization from Open Multilingual WordNet
    deprecated: Use the specific type with the language (OMWN_IT, OWMN_FR, ...) instead.
    """

    IWN: "BabelSenseSource" = 2, "Italian WordNet", "https://datahub.io/dataset/iwn", 3
    """Lexicalization from Italian WordNet"""

    WONEF: "BabelSenseSource" = 20, "WordNet du Français", "http://wonef.fr/", 4
    """Lexicalization from WordNet du Francais"""

    WIKI: "BabelSenseSource" = 3, "Wikipedia", "http://www.wikipedia.org", 5
    """Lexicalization from Wikipedia"""

    WIKIDIS: "BabelSenseSource" = 4, "Wikipedia", "http://www.wikipedia.org", 6
    """Lexicalization found in a disambiguation page"""

    WIKIDATA: "BabelSenseSource" = 5, "Wikidata", "http://www.wikidata.org", 7
    """Lexicalization from Wikidata"""

    OMWIKI: "BabelSenseSource" = 6, "OmegaWiki", "http://www.omegawiki.org", 8
    """Lexicalization from OmegaWiki"""

    WIKT: "BabelSenseSource" = 7, "Wiktionary", "http://en.wiktionary.org", 9
    """Lexicalization from Wiktionary"""

    WIKICAT: "BabelSenseSource" = 8, "Wikipedia", "http://www.wikipedia.org", 10
    """Wikipedia category, not available as of version 3.0"""

    WIKIRED: "BabelSenseSource" = 9, "Wikipedia", "http://www.wikipedia.org", 11
    """Lexicalization from a Wikipedia redirection"""

    WIKIQU: "BabelSenseSource" = 10, "Wikiquote", "http://en.wikiquote.org/wiki/", 12
    """
    Lexicalization found in Wikiquote
    deprecated: removed with BabelNet 5.0
    """

    WIKIQUREDI: "BabelSenseSource" = 11, "Wikiquote", "http://en.wikiquote.org/wiki/", 13
    """
    Lexicalization found in Wikiquote redirection
    deprecated: removed with BabelNet 5.0
    """

    WIKTLB: "BabelSenseSource" = 7, "Wiktionary", "http://en.wiktionary.org", 14
    """Wiktionary translation label"""

    VERBNET: "BabelSenseSource" = 13, "VerbNet", "http://verbs.colorado.edu/", 15
    """
    Lexicalization found in VerbNet
    deprecated: removed with BabelNet 5.0
    """

    FRAMENET: "BabelSenseSource" = 13, "FrameNet", "https://framenet2.icsi.berkeley.edu", 16
    """
    Lexicalization found in FrameNet
    deprecated: removed with BabelNet 5.0
    """

    MSTERM: "BabelSenseSource" = (
        12,
        "Microsoft Terminology",
        "https://www.microsoft.com/Language/en-US/Terminology.aspx",
        17,
    )
    """
    Lexicalization found in Microsoft Terminology
    deprecated: removed with BabelNet 5.0
    """

    GEONM: "BabelSenseSource" = 10, "GeoNames", "http://www.geonames.org/", 18
    """Lexicalization found in GeoNames"""

    WNTR: "BabelSenseSource" = (
        20,
        "Translations",
        "http://wordnet.princeton.edu",
        19
    )
    """Lexicalization from an automatic translation of a WordNet concept"""

    WIKITR: "BabelSenseSource" = (
        20,
        "Translations",
        "http://www.wikipedia.org",
        20
    )
    """Lexicalization from an automatic translation of a Wikipedia concept"""

    MCR_EU: "BabelSenseSource" = (
        2,
        "Basque Open Multilingual WordNet",
        "https://adimen.si.ehu.es/web/MCR",
        21,
    )
    """Lexicalization from Basque Open Multilingual WordNet"""

    OMWN_HR: "BabelSenseSource" = (
        2,
        "Croatian Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        22,
    )
    """Lexicalization from Croatian Open Multilingual WordNet"""

    SLOWNET: "BabelSenseSource" = (
        2,
        "Slovenian Open Multilingual WordNet",
        "http://lojze.lugos.si/darja/research/slownet/",
        23,
    )
    """Lexicalization from Slovenian Open Multilingual WordNet"""

    OMWN_ID: "BabelSenseSource" = (
        2,
        "Bahasa Open Multilingual WordNet",
        "http://wn-msa.sourceforge.net/",
        24,
    )
    """Lexicalization from Bahasa Open Multilingual WordNet"""

    OMWN_IT: "BabelSenseSource" = (
        2,
        "Italian Open Multilingual WordNet",
        "https://multiwordnet.fbk.eu/english/home.php",
        25,
    )
    """Lexicalization from Italian Open Multilingual WordNet"""

    MCR_GL: "BabelSenseSource" = (
        2,
        "Galician Open Multilingual WordNet",
        "https://adimen.si.ehu.es/web/MCR",
        26,
    )
    """Lexicalization from Galician Open Multilingual WordNet"""

    ICEWN: "BabelSenseSource" = (
        2,
        "Icelandic (IceWordNet) Open Multilingual WordNet",
        "http://www.malfong.is/index.php?lang=en&pg=icewordnet",
        27,
    )
    """Lexicalization from Galician (IceWordNet) Open Multilingual WordNet"""

    OMWN_ZH: "BabelSenseSource" = (
        2,
        "Chinese Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/cow/",
        28,
    )
    """Lexicalization from Chinese Open Multilingual WordNet"""

    OMWN_NO: "BabelSenseSource" = (
        2,
        "Norwegian Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        29,
    )
    """Lexicalization from Norwegian Open Multilingual WordNet NOB"""

    OMWN_NN: "BabelSenseSource" = (
        2,
        "Norwegian Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        30,
    )
    """Lexicalization from Norwegian Open Multilingual WordNet NN"""

    SALDO: "BabelSenseSource" = (
        2,
        "Swedish Open Multilingual WordNet",
        "http://spraakbanken.gu.se/eng/resource/wordnet-saldo",
        31,
    )
    """Lexicalization from Swedish Open Multilingual WordNet"""

    OMWN_JA: "BabelSenseSource" = (
        2,
        "Japanese Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/wnja/",
        32,
    )
    """Lexicalization from Japanese Open Multilingual WordNet"""

    MCR_CA: "BabelSenseSource" = (
        2,
        "Catalan Open Multilingual WordNet",
        "https://adimen.si.ehu.es/web/MCR",
        33,
    )
    """Lexicalization from Catalan Open Multilingual WordNet"""
    OMWN_PT: "BabelSenseSource" = (
        2,
        "Portuguese Open Multilingual WordNet",
        "https://github.com/arademaker/openWordnet-PT",
        34,
    )
    """Lexicalization from Portuguese Open Multilingual WordNet"""

    OMWN_FI: "BabelSenseSource" = (
        2,
        "Finnish Open Multilingual WordNet",
        "https://www.kielipankki.fi/corpora/finnwordnet/",
        35,
    )
    """Lexicalization from Finnish Open Multilingual WordNet"""

    OMWN_PL: "BabelSenseSource" = (
        2,
        "Poland Open Multilingual WordNet",
        "http://plwordnet.pwr.wroc.pl/wordnet/",
        36,
    )
    """Lexicalization from Poland Open Multilingual WordNet"""

    OMWN_TH: "BabelSenseSource" = (
        2,
        "Thai Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        37,
    )
    """Lexicalization from Thai Open Multilingual WordNet"""

    OMWN_SK: "BabelSenseSource" = (
        2,
        "Slovak Open Multilingual WordNet",
        "http://korpus.juls.savba.sk/WordNet_en.html",
        38,
    )
    """Lexicalization from Slovak Open Multilingual WordNet"""

    OMWN_LT: "BabelSenseSource" = (
        2,
        "Lithuanian Open Multilingual WordNet",
        "http://korpus.juls.savba.sk/ltskwn_en.html",
        39,
    )
    """Lexicalization from Lithuanian Open Multilingual WordNet"""

    OMWN_NL: "BabelSenseSource" = (
        2,
        "Dutch Open Multilingual WordNet",
        "http://wordpress.let.vupr.nl/odwn/",
        40,
    )
    """Lexicalization from Dutch Open Multilingual WordNet"""

    OMWN_AR: "BabelSenseSource" = (
        2,
        "Arabic Open Multilingual WordNet",
        "http://www.globalwordnet.org/AWN/",
        41,
    )
    """Lexicalization from Arabic Open Multilingual WordNet"""

    OMWN_FA: "BabelSenseSource" = (
        2,
        "Persian Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        42,
    )
    """Lexicalization from Persian Open Multilingual WordNet"""

    OMWN_EL: "BabelSenseSource" = (
        2,
        "Greek Open Multilingual WordNet",
        "https://github.com/okfngr/wordnet",
        43,
    )
    """Lexicalization from Greek Open Multilingual WordNet"""

    MCR_ES: "BabelSenseSource" = (
        2,
        "Spanish Open Multilingual WordNet",
        "https://adimen.si.ehu.es/web/MCR",
        44,
    )
    """Lexicalization from Spanish Open Multilingual WordNet"""

    OMWN_RO: "BabelSenseSource" = (
        2,
        "Romanian Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        45,
    )
    """Lexicalization from Romanian Open Multilingual WordNet"""

    OMWN_SQ: "BabelSenseSource" = (
        2,
        "Albanian (AlbaNet) Open Multilingual WordNet",
        "http://compling.hss.ntu.edu.sg/omw/#cite:",
        46,
    )
    """Lexicalization from Albanian (AlbaNet) Open Multilingual WordNet"""

    OMWN_DA: "BabelSenseSource" = (
        2,
        "Danish (DanNet) Open Multilingual WordNet",
        "https://cst.ku.dk/projekter/dannet/",
        47,
    )
    """Lexicalization from Danish (DanNet) Open Multilingual WordNet"""

    OMWN_FR: "BabelSenseSource" = (
        2,
        "French (WOLF) Open Multilingual WordNet",
        "http://alpage.inria.fr/~sagot/wolf-en.html",
        48,
    )
    """Lexicalization from French (WOLF) Open Multilingual WordNet"""

    OMWN_MS: "BabelSenseSource" = (
        2,
        "Bahasa Open Multilingual WordNet",
        "http://wn-msa.sourceforge.net/",
        49,
    )
    """Lexicalization from Bahasa Open Multilingual WordNet"""

    OMWN_BG: "BabelSenseSource" = (
        2,
        "Bulgarian (BulTreeBank) Open Multilingual WordNet",
        "http://www.bultreebank.org/",
        50,
    )
    """Lexicalization from Bulgarian (BulTreeBank) Open Multilingual WordNet"""

    OMWN_HE: "BabelSenseSource" = (
        2,
        "Hebrew Open Multilingual WordNet",
        "http://cl.haifa.ac.il/projects/mwn/index.shtml",
        51,
    )
    """Lexicalization from Hebrew Open Multilingual WordNet"""

    OMWN_KO: "BabelSenseSource" = 2, "Korean WordNet", "http://wordnet.kaist.ac.kr/", 52
    """Lexicalization from Korean WordNet"""

    MCR_PT: "BabelSenseSource" = (
        2,
        "Portuguese from Multilingual Central Repository",
        "https://adimen.si.ehu.es/web/MCR",
        53,
    )
    """Lexicalization from Portuguese Open Multilingual WordNet"""

    OMWN_GAE: "BabelSenseSource" = (
        2,
        "Irish (GAWN) WordNet",
        "https://github.com/jimregan/lemonGAWN",
        54,
    )
    """Lexicalization from Irish (GAWN) WordNet"""

    OMWN_CWN: "BabelSenseSource" = 2, "Chinese WordNet", "http://lope.linguistics.ntu.edu.tw/cwn2/", 55
    """Lexicalization from Chinese WordNet deprecated"""

    # -------------------------------------------------------------------
    WORD_ATLAS: "BabelSenseSource" = 0, "WordAtlas", "http://wordatlas.org", 56
    """Lexicalization from WordAtlas"""

    WIKIDATA_ALIAS: "BabelSenseSource" = 9, "Wikidata", "http://www.wikidata.org", 57
    """Alias from Wikidata"""

    WN2020 = 2, "WordNet 2020", "https://en-word.net", 58
    """Lexicalization from WordNet 2020"""

    OEWN: "BabelSenseSource" = 2, "Open English WordNet", "https://en-word.net", 59
    """Lexicalization from Open English WordNet"""

    def __init__(self, ordinal_for_sorting, source_name, uri, ordinal: int):
        """init method
        @param ordinal_for_sorting: Ordinal for sense sorting.
        @type ordinal_for_sorting: int
        @param source_name: Name of the source.
        @type source_name: str
        @param uri: Source URI.
        @type uri: str
        @param ordinal: the ordinal
        @type ordinal: int
        """
        assert ordinal is not None
        self.ordinal_for_sorting = ordinal_for_sorting
        self.source_name = source_name
        self._uri = uri
        self.ordinal: int = ordinal

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @property
    def is_from_any_wordnet(self) -> bool:
        """True if the source is any wordnet (Princeton WordNet or any other language).

        @return: True if the source is any wordnet (Princeton WordNet or any other language), false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.WN or self.is_from_multi_wordnet

    @property
    def is_from_multi_wordnet(self) -> bool:
        """
        True if the source is any wordnet (Princeton WordNet is not included)

        @return: True if the source is any wordnet (Princeton WordNet is not included), false otherwise.
        @rtype: bool
        """
        return self in [
            BabelSenseSource.OMWN,
            BabelSenseSource.OMWN_SQ,
            BabelSenseSource.OMWN_FI,
            BabelSenseSource.OMWN_IT,
            BabelSenseSource.MCR_CA,
            BabelSenseSource.MCR_GL,
            BabelSenseSource.MCR_ES,
            BabelSenseSource.SALDO,
            BabelSenseSource.OMWN_ZH,
            BabelSenseSource.OMWN_FA,
            BabelSenseSource.OMWN_HE,
            BabelSenseSource.OMWN_JA,
            BabelSenseSource.OMWN_ID,
            BabelSenseSource.OMWN_NO,
            BabelSenseSource.OMWN_NN,
            BabelSenseSource.OMWN_PL,
            BabelSenseSource.OMWN_TH,
            BabelSenseSource.OMWN_MS,
            BabelSenseSource.MCR_EU,
            BabelSenseSource.OMWN_AR,
            BabelSenseSource.OMWN_PT,
            BabelSenseSource.SLOWNET,
            BabelSenseSource.OMWN_FR,
            BabelSenseSource.OMWN_EL,
            BabelSenseSource.OMWN_DA,
            BabelSenseSource.OMWN_BG,
            BabelSenseSource.OMWN_NL,
            BabelSenseSource.OMWN_LT,
            BabelSenseSource.OMWN_RO,
            BabelSenseSource.IWN,
            BabelSenseSource.WONEF,
            BabelSenseSource.OMWN_GAE,
            BabelSenseSource.OMWN_HR,
            BabelSenseSource.ICEWN,
            BabelSenseSource.OMWN_SK,
            BabelSenseSource.OMWN_KO,
            BabelSenseSource.OMWN_CWN,
            BabelSenseSource.MCR_PT,
            BabelSenseSource.WN2020,
            BabelSenseSource.OEWN
        ]

    @property
    def is_from_wordnet(self) -> bool:
        """
        True if the source is Princeton WordNet.

        @return: True if the source is Princeton WordNet, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.WN

    @property
    def is_from_babelnet(self) -> bool:
        """
        True if the source is BabelNet.

        @return: True if the source is BabelNet, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.BABELNET

    @property
    def is_from_wordatlas(self) -> bool:
        """True if the source is WordAtlas.

        @return: True if the source is WordAtlas, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.WORD_ATLAS

    @property
    def is_from_wikipedia(self) -> bool:
        """True if the source is Wikipedia.

        @return: True if the source is Wikipedia, false otherwise.
        @rtype: bool
        """
        return (
                self is BabelSenseSource.WIKI
                or self is BabelSenseSource.WIKIRED
                or self is BabelSenseSource.WIKIDIS
                or self is BabelSenseSource.WIKICAT
        )

    @property
    def is_from_wiktionary(self) -> bool:
        """True if the source is Wiktionary.

        @return: True if the source is Wiktionary, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.WIKT or self is BabelSenseSource.WIKTLB

    @property
    def is_from_wikiquote(self) -> bool:
        """True if the source is WikiQuote.

        @return: True if the source is WikiQuote, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.WIKIQU or self is BabelSenseSource.WIKIQUREDI

    @property
    def is_from_omegawiki(self) -> bool:
        """True if the source is OmegaWiki.

        @return: True if the source is OmegaWiki, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.OMWIKI

    @property
    def is_redirection(self) -> bool:
        """True if the source is Wikipedia or Wikiquote redirection.

        @return: True if the source is Wikipedia or Wikiquote redirection, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.WIKIRED or self is BabelSenseSource.WIKIQUREDI

    @property
    def is_automatic_translation_from_babelnet(self) -> bool:
        """True if the source is the result of automatic machine
        translation from BabelNet. To cover all kinds of machine translation,
        please use the more general L{is_automatic_translation}.

        @return: True if the source is the result of automatic machine translation from BabelNet, false otherwise.
        @rtype: bool
        """
        return self is BabelSenseSource.WIKITR or self is BabelSenseSource.WNTR

    # In Java richiede in input il linguaggio anche se non viene usato. Io l'ho eliminato.
    @property
    def uri(self) -> str:
        """An URI associated with a given language.

        @return: An URI associated with a given language.
        @rtype: str
        """

        return {
            BabelSenseSource.OMWN_SQ: self._uri + "als",
            BabelSenseSource.OMWN_FA: self._uri + "fas",
            BabelSenseSource.OMWN_NO: self._uri + "nob",
            BabelSenseSource.OMWN_NN: self._uri + "nno",
            BabelSenseSource.OMWN_TH: self._uri + "tha",
            BabelSenseSource.OMWN_RO: self._uri + "ron",
            BabelSenseSource.OMWN_HR: self._uri + "hrv",
        }.get(self, self._uri)

    def is_automatic_translation(self, language: Optional[Language] = None) -> bool:
        """
        Return True if the source is the result of automatic machine translation.

        @param language: The language of the source (important to determine if the Open Multilingual WordNet is from
        manual annotation or not).
        @type language: Optional[Language]

        @return: True if the source is the result of automatic machine translation.
        @rtype: bool
        """

        def main_sources_check():
            return self in {
                BabelSenseSource.FRAMENET,
                BabelSenseSource.BABELNET,
                BabelSenseSource.WORD_ATLAS,
                BabelSenseSource.OMWIKI,
                BabelSenseSource.WN,
                BabelSenseSource.WIKI,
                BabelSenseSource.WIKIRED,
                BabelSenseSource.WIKIDIS,
                BabelSenseSource.WIKIQU,
                BabelSenseSource.WIKIQUREDI,
                BabelSenseSource.WIKT,
                BabelSenseSource.WIKTLB,
                BabelSenseSource.WIKICAT,
                BabelSenseSource.WIKIDATA,
                BabelSenseSource.WIKIDATA_ALIAS,
                BabelSenseSource.MSTERM,
                BabelSenseSource.GEONM,
                BabelSenseSource.VERBNET,
                BabelSenseSource.IWN,
                BabelSenseSource.WN2020,
                BabelSenseSource.OEWN,
            }

        if main_sources_check():
            return False

        if self in {
            BabelSenseSource.WONEF,
            BabelSenseSource.WIKITR,
            BabelSenseSource.WNTR,
        }:
            return True

        if language is None:
            if self in {
                BabelSenseSource.OMWN_FR,
                BabelSenseSource.OMWN_PT,
                BabelSenseSource.OMWN_JA,
                BabelSenseSource.OMWN_ID,
                BabelSenseSource.OMWN_MS,
                BabelSenseSource.OMWN_GAE,
            }:
                return True

            if self in {
                # First case block
                BabelSenseSource.OMWN_AR,
                BabelSenseSource.OMWN_IT,
                BabelSenseSource.OMWN_SQ,
                BabelSenseSource.OMWN_FI,
                BabelSenseSource.MCR_CA,
                BabelSenseSource.MCR_GL,
                BabelSenseSource.MCR_ES,
                BabelSenseSource.SALDO,
                BabelSenseSource.OMWN_ZH,
                BabelSenseSource.OMWN_DA,
                BabelSenseSource.OMWN_FA,
                BabelSenseSource.OMWN_HE,
                # Second case block
                BabelSenseSource.OMWN_RO,
                BabelSenseSource.OMWN_SK,
                BabelSenseSource.OMWN_LT,
                BabelSenseSource.OMWN_NL,
                BabelSenseSource.ICEWN,
                BabelSenseSource.OMWN_NO,
                BabelSenseSource.OMWN_PL,
                BabelSenseSource.OMWN_TH,
                BabelSenseSource.MCR_EU,
                BabelSenseSource.OMWN_EL,
                BabelSenseSource.MCR_PT,
            }:
                return False

            return True

        if self == BabelSenseSource.OMWN:
            if language in {
                Language.FR,
                Language.PT,
                Language.JA,
                Language.ID,
                Language.MS,
            }:
                return True
            if language in {
                # First case block
                Language.AR,
                Language.IT,
                Language.SQ,
                Language.FI,
                Language.CA,
                Language.GL,
                Language.ES,
                Language.SV,
                Language.ZH,
                Language.DA,
                Language.FA,
                Language.HE,
                # Second case block
                Language.RO,
                Language.SK,
                Language.LT,
                Language.NL,
                Language.IS,
                Language.NO,
                Language.PL,
                Language.TH,
                Language.EU,
                Language.EL,
            }:
                return False

            return True

        if self in {
            BabelSenseSource.OMWN_FR,
            BabelSenseSource.OMWN_PT,
            BabelSenseSource.OMWN_JA,
            BabelSenseSource.OMWN_ID,
            BabelSenseSource.OMWN_MS,
            BabelSenseSource.OMWN_GAE,
        }:
            return True

        if self in {
            # First case block
            BabelSenseSource.OMWN_AR,
            BabelSenseSource.OMWN_IT,
            BabelSenseSource.OMWN_SQ,
            BabelSenseSource.OMWN_FI,
            BabelSenseSource.MCR_CA,
            BabelSenseSource.MCR_GL,
            BabelSenseSource.MCR_ES,
            BabelSenseSource.SALDO,
            BabelSenseSource.OMWN_ZH,
            BabelSenseSource.OMWN_DA,
            BabelSenseSource.OMWN_FA,
            BabelSenseSource.OMWN_HE,
            # Second case block
            BabelSenseSource.OMWN_RO,
            BabelSenseSource.OMWN_SK,
            BabelSenseSource.OMWN_LT,
            BabelSenseSource.OMWN_NL,
            BabelSenseSource.ICEWN,
            BabelSenseSource.OMWN_NO,
            BabelSenseSource.OMWN_PL,
            BabelSenseSource.OMWN_TH,
            BabelSenseSource.MCR_EU,
            BabelSenseSource.OMWN_EL,
            BabelSenseSource.MCR_PT,
        }:
            return False

        return True

    def get_license(self, language=None) -> BabelLicense:
        """Return the license associated with the source for
        a given language.

        @param language: The source language (default None).
        @type language: Optional[Language]

        @return: Source license.
        @rtype: BabelLicense
        """
        if self is BabelSenseSource.BABELNET:
            return BabelLicense.BABELNET_NC

        if self is BabelSenseSource.WORD_ATLAS:
            return BabelLicense.COMMERCIAL

        if self in {
            BabelSenseSource.WONEF,
            BabelSenseSource.WIKIQUREDI,
            BabelSenseSource.WIKIQU,
            BabelSenseSource.WIKI,
            BabelSenseSource.WIKIRED,
            BabelSenseSource.WIKIDIS,
            BabelSenseSource.WIKT,
            BabelSenseSource.WIKICAT,
            BabelSenseSource.WIKTLB,
            BabelSenseSource.WIKITR,
            BabelSenseSource.WIKIDATA,
            BabelSenseSource.WIKIDATA_ALIAS,
        }:
            return BabelLicense.CC_BY_SA_30

        if self is BabelSenseSource.VERBNET:
            return BabelLicense.UNRESTRICTED

        if self is BabelSenseSource.OMWIKI:
            return BabelLicense.CC0_10

        if self is BabelSenseSource.FRAMENET:
            return BabelLicense.CC_BY_30

        if self is BabelSenseSource.MSTERM:
            return BabelLicense.MLP

        if self is BabelSenseSource.OMWN:
            if language in {
                Language.IS,
                Language.BG,
                Language.SQ,
                Language.FI,
                Language.IT,
                Language.CA,
                Language.GL,
                Language.ES,
                Language.SV,
            }:
                return BabelLicense.CC_BY_30

            if language in {
                Language.ZH,
                Language.DA,
                Language.FA,
                Language.HE,
                Language.JA,
                Language.ID,
                Language.NN,
                Language.NO,
                Language.PL,
                Language.TH,
                Language.MS,
            }:
                return BabelLicense.UNRESTRICTED

            if language in {Language.HR, Language.EU}:
                return BabelLicense.CC_BY_NC_SA_30

            if language == Language.FR:
                return BabelLicense.CECILL_C

            if language == Language.EL:
                return BabelLicense.APACHE_20

            if language == Language.NL:
                return BabelLicense.CC_BY_SA_40

            return None

        if self in {
            BabelSenseSource.ICEWN,
            BabelSenseSource.OMWN_HR,
            BabelSenseSource.MCR_EU,
            BabelSenseSource.OMWN_BG,
            BabelSenseSource.OMWN_SQ,
            BabelSenseSource.OMWN_FI,
            BabelSenseSource.OMWN_IT,
            BabelSenseSource.MCR_CA,
            BabelSenseSource.MCR_GL,
            BabelSenseSource.MCR_ES,
            BabelSenseSource.SALDO,
            BabelSenseSource.MCR_PT,
        }:
            return BabelLicense.CC_BY_30

        if self is BabelSenseSource.OMWN_FA:
            return BabelLicense.UNRESTRICTED

        if self in {
            BabelSenseSource.OMWN_RO,
            BabelSenseSource.OMWN_LT,
            BabelSenseSource.OMWN_SK,
            BabelSenseSource.OMWN_AR,
            BabelSenseSource.OMWN_PT,
        }:
            return BabelLicense.CC_BY_SA_30

        if self is BabelSenseSource.OMWN_FR:
            return BabelLicense.CECILL_C

        if self is BabelSenseSource.OMWN_EL:
            return BabelLicense.APACHE_20

        if self in {BabelSenseSource.OMWN_NL, BabelSenseSource.SLOWNET, BabelSenseSource.GEONM}:
            return BabelLicense.CC_BY_SA_40

        if self in {
            BabelSenseSource.OMWN_ZH,
            BabelSenseSource.OMWN_DA,
            BabelSenseSource.OMWN_HE,
            BabelSenseSource.OMWN_NN,
            BabelSenseSource.OMWN_NO,
            BabelSenseSource.OMWN_PL,
            BabelSenseSource.OMWN_JA,
            BabelSenseSource.OMWN_TH,
            BabelSenseSource.WN,
            BabelSenseSource.WNTR,
        }:
            return BabelLicense.WORDNET

        if self in {BabelSenseSource.OMWN_MS, BabelSenseSource.OMWN_ID, BabelSenseSource.OMWN_KO}:
            return BabelLicense.MIT

        if self is BabelSenseSource.OMWN_GAE:
            return BabelLicense.GFDL_12

        if self is BabelSenseSource.IWN:
            return BabelLicense.ODC_BY_10

        if self in {
            BabelSenseSource.WN2020,
            BabelSenseSource.OEWN
        }:
            return BabelLicense.CC_BY_40

        return None


class BabelImageSource(Enum):
    """
    Sources for BabelNet images, sorted by priority.

    @ivar ordinal: the ordinal
    @type ordinal: int
    """

    BABELNET: "BabelImageSource" = 0
    """BabelNet image."""

    OMWIKI: "BabelImageSource" = 1
    """OmegaWiki image."""

    WIKI: "BabelImageSource" = 2
    """Wikipedia image."""

    IMAGENET: "BabelImageSource" = 3
    """ImageNet image."""

    WIKIDATA: "BabelImageSource" = 4
    """Wikidata image."""

    BABELPIC_GOLD: "BabelImageSource" = 5
    """BabelPic gold image."""

    BABELPIC_SILVER: "BabelImageSource" = 6
    """BabelPic silver image"""

    def __init__(self, ordinal: int):
        """init method
        @param ordinal: the ordinal
        """
        self.ordinal: int = ordinal

    @classmethod
    def get_license(cls, source: "BabelImageSource") -> BabelLicense:
        """
        Return the license for a given image source.

        @param source: Image source.

        @return: The BabelLicense for the image source.
        """
        return {
            cls.BABELNET: BabelLicense.CC_BY_NC_SA_30,
            cls.WIKIDATA: BabelLicense.CC_BY_SA_30,
            cls.WIKI: BabelLicense.CC_BY_SA_30,
            cls.OMWIKI: BabelLicense.CC_BY_30,
            cls.BABELPIC_GOLD: BabelLicense.CC_BY_NC_SA_40,
            cls.BABELPIC_SILVER: BabelLicense.CC_BY_NC_SA_40,
        }[source]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


__all__ = ["BabelSenseSource", "BabelImageSource"]
