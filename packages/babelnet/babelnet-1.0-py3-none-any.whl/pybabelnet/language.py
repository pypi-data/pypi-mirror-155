"""This module contains the Language enum."""
from typing import Optional

from aenum import Enum

count = 0
"""Count of the elements inside this enum"""

class Language(Enum):
    """A language enumeration."""

    EN = "English"
    """English"""

    AF = "Afrikaans"
    """Afrikaans"""

    SQ = "Albanian"
    """Albanian"""

    AR = "Arabic", True
    """Arabic"""

    HY = "Armenian"
    """Armenian"""

    AZ = "Azerbaijani"
    """Azerbaijani"""

    EU = "Basque"
    """Basque"""

    BN = "Bengali"
    """Bengali"""

    BG = "Bulgarian"
    """Bulgarian"""

    CA = "Catalan"
    """Catalan"""

    ZH = "Chinese"
    """Chinese"""

    HR = "Croatian"
    """Croatian"""

    CS = "Czech"
    """Czech"""

    DA = "Danish"
    """Danish"""

    NL = "Dutch"
    """Dutch"""

    EO = "Esperanto"
    """Esperanto"""

    ET = "Estonian"
    """Estonian"""

    FI = "Finnish"
    """Finnish"""

    FR = "French"
    """French"""

    GL = "Galician"
    """Galician"""

    KA = "Georgian"
    """Georgian"""

    DE = "German"
    """German"""

    EL = "Greek"
    """Greek"""

    HE = "Hebrew", True
    """Hebrew"""

    HI = "Hindi"
    """Hindi"""

    HU = "Hungarian"
    """Hungarian"""

    IS = "Icelandic"
    """Icelandic"""

    ID = "Indonesian"
    """Indonesian"""

    GA = "Irish"
    """Irish"""

    IT = "Italian"
    """Italian"""

    JA = "Japanese"
    """Japanese"""

    KK = "Kazakh"
    """Kazakh"""

    KO = "Korean"
    """Korean"""

    LA = "Latin"
    """Latin"""

    LV = "Latvian"
    """Latvian"""

    LT = "Lithuanian"
    """Lithuanian"""

    MS = "Malay"
    """Malay"""

    MT = "Maltese"
    """Maltese"""

    NO = "Norwegian (Bokmål)"
    """Norwegian (Bokmål)"""

    FA = "Persian", True
    """Persian"""

    PL = "Polish"
    """Polish"""

    PT = "Portuguese"
    """Portuguese"""

    RO = "Romanian"
    """Romanian"""

    RU = "Russian"
    """Russian"""

    SR = "Serbian"
    """Serbian"""

    SIMPLE = "Simple English"
    """Simple English"""

    SK = "Slovak"
    """Slovak"""

    SL = "Slovenian"
    """Slovenian"""

    ES = "Spanish"
    """Spanish"""

    SW = "Swahili"
    """Swahili"""

    SV = "Swedish"
    """Swedish"""

    TL = "Tagalog"
    """Tagalog"""

    TA = "Tamil"
    """Tamil"""

    TH = "Thai"
    """Thai"""

    BO = "Tibetan"
    """Tibetan"""

    TR = "Turkish"
    """Turkish"""

    UK = "Ukrainian"
    """Ukrainian"""

    UR = "Urdu"
    """Urdu"""

    VI = "Vietnamese"
    """Vietnamese"""

    CY = "Welsh"
    """Welsh"""

    WAR = "Waray-Waray"
    """Waray-Waray"""

    CEB = "Cebuano"
    """Cebuano"""

    MIN = "Minangkabau"
    """Minangkabau"""

    UZ = "Uzbek"
    """Uzbek"""

    VO = "Volapük"
    """Volapük"""

    NN = "Norwegian (Nynorsk)"
    """Norwegian (Nynorsk)"""

    OC = "Occitan"
    """Occitan"""

    MK = "Macedonian"
    """Macedonian"""

    BE = "Belarusian"
    """Belarusian"""

    NEW = "Newar / Nepal Bhasa"
    """Newar / Nepal Bhasa"""

    TT = "Tatar"
    """Tatar"""

    PMS = "Piedmontese"
    """Piedmontese"""

    TE = "Telugu"
    """Telugu"""

    BE_X_OLD = "Belarusian (Taraškievica)"
    """Belarusian (Taraškievica)"""

    HT = "Haitian"
    """Haitian"""

    BS = "Bosnian"
    """Bosnian"""

    BR = "Breton"
    """Breton"""

    JV = "Javanese"
    """Javanese"""

    MG = "Malagasy"
    """Malagasy"""

    CE = "Chechen"
    """Chechen"""

    LB = "Luxembourgish"
    """Luxembourgish"""

    MR = "Marathi"
    """Marathi"""

    ML = "Malayalam"
    """Malayalam"""

    PNB = "Western Panjabi", True
    """Western Panjabi"""

    BA = "Bashkir"
    """Bashkir"""

    MY = "Burmese"
    """Burmese"""

    ZH_YUE = "Cantonese"
    """Cantonese"""

    LMO = "Lombard"
    """Lombard"""

    YO = "Yoruba"
    """Yoruba"""

    FY = "West Frisian"
    """West Frisian"""

    AN = "Aragonese"
    """Aragonese"""

    CV = "Chuvash"
    """Chuvash"""

    TG = "Tajik"
    """Tajik"""

    KY = "Kirghiz"
    """Kirghiz"""

    NE = "Nepali"
    """Nepali"""

    IO = "Ido"
    """Ido"""

    GU = "Gujarati"
    """Gujarati"""

    BPY = "Bishnupriya Manipuri"
    """Bishnupriya Manipuri"""

    SCO = "Scots"
    """Scots"""

    SCN = "Sicilian"
    """Sicilian"""

    NDS = "Low Saxon"
    """Low Saxon"""

    KU = "Kurdish"
    """Kurdish"""

    AST = "Asturian"
    """Asturian"""

    QU = "Quechua"
    """Quechua"""

    SU = "Sundanese"
    """Sundanese"""

    ALS = "Alemannic"
    """Alemannic"""

    GD = "Scottish Gaelic"
    """Scottish Gaelic"""

    KN = "Kannada"
    """Kannada"""

    AM = "Amharic"
    """Amharic"""

    IA = "Interlingua"
    """Interlingua"""

    NAP = "Neapolitan"
    """Neapolitan"""

    CKB = "Sorani", True
    """Sorani"""

    BUG = "Buginese"
    """Buginese"""

    BAT_SMG = "Samogitian"
    """Samogitian"""

    WA = "Walloon"
    """Walloon"""

    MAP_BMS = "Banyumasan"
    """Banyumasan"""

    MN = "Mongolian"
    """Mongolian"""

    ARZ = "Egyptian Arabic", True
    """Egyptian Arabic"""

    MZN = "Mazandarani", True
    """Mazandarani"""

    SI = "Sinhalese"
    """Sinhalese"""

    PA = "Punjabi"
    """Punjabi"""

    ZH_MIN_NAN = "Min Nan"
    """Min Nan"""

    YI = "Yiddish", True
    """Yiddish"""

    SAH = "Sakha"
    """Sakha"""

    VEC = "Venetian"
    """Venetian"""

    FO = "Faroese"
    """Faroese"""

    SA = "Sanskrit"
    """Sanskrit"""

    BAR = "Bavarian"
    """Bavarian"""

    NAH = "Nahuatl"
    """Nahuatl"""

    OS = "Ossetian"
    """Ossetian"""

    ROA_TARA = "Tarantino"
    """Tarantino"""

    PAM = "Kapampangan"
    """Kapampangan"""

    OR = "Oriya"
    """Oriya"""

    HSB = "Upper Sorbian"
    """Upper Sorbian"""

    SE = "Northern Sami"
    """Northern Sami"""

    LI = "Limburgish"
    """Limburgish"""

    MRJ = "Hill Mari"
    """Hill Mari"""

    MI = "Maori"
    """Maori"""

    ILO = "Ilokano"
    """Ilokano"""

    CO = "Corsican"
    """Corsican"""

    HIF = "Fiji Hindi"
    """Fiji Hindi"""

    BCL = "Central Bicolano"
    """Central Bicolano"""

    GAN = "Gan"
    """Gan"""

    FRR = "North Frisian"
    """North Frisian"""

    RUE = "Rusyn"
    """Rusyn"""

    GLK = "Gilaki", True
    """Gilaki"""

    MHR = "Meadow Mari"
    """Meadow Mari"""

    NDS_NL = "Dutch Low Saxon"
    """Dutch Low Saxon"""

    FIU_VRO = "Võro"
    """Võro"""

    PS = "Pashto", True
    """Pashto"""

    TK = "Turkmen"
    """Turkmen"""

    PAG = "Pangasinan"
    """Pangasinan"""

    VLS = "West Flemish"
    """West Flemish"""

    GV = "Manx"
    """Manx"""

    XMF = "Mingrelian"
    """Mingrelian"""

    DIQ = "Zazaki"
    """Zazaki"""

    KM = "Khmer"
    """Khmer"""

    KV = "Komi"
    """Komi"""

    ZEA = "Zeelandic"
    """Zeelandic"""

    CSB = "Kashubian"
    """Kashubian"""

    CRH = "Crimean Tatar"
    """Crimean Tatar"""

    HAK = "Hakka"
    """Hakka"""

    VEP = "Vepsian"
    """Vepsian"""

    AY = "Aymara"
    """Aymara"""

    DV = "Divehi", True
    """Divehi"""

    SO = "Somali"
    """Somali"""

    SC = "Sardinian"
    """Sardinian"""

    ZH_CLASSICAL = "Classical Chinese"
    """Classical Chinese"""

    NRM = "Norman"
    """Norman"""

    RM = "Romansh"
    """Romansh"""

    UDM = "Udmurt"
    """Udmurt"""

    KOI = "Komi-Permyak"
    """Komi-Permyak"""

    KW = "Cornish"
    """Cornish"""

    UG = "Uyghur", True
    """Uyghur"""

    STQ = "Saterland Frisian"
    """Saterland Frisian"""

    LAD = "Ladino"
    """Ladino"""

    WUU = "Wu"
    """Wu"""

    LIJ = "Ligurian"
    """Ligurian"""

    FUR = "Friulian"
    """Friulian"""

    EML = "Emilian-Romagnol"
    """Emilian-Romagnol"""

    AS = "Assamese"
    """Assamese"""

    BH = "Bihari"
    """Bihari"""

    CBK_ZAM = "Zamboanga Chavacano"
    """Zamboanga Chavacano"""

    GN = "Guarani"
    """Guarani"""

    PI = "Pali"
    """Pali"""

    GAG = "Gagauz"
    """Gagauz"""

    PCD = "Picard"
    """Picard"""

    KSH = "Ripuarian"
    """Ripuarian"""

    NOV = "Novial"
    """Novial"""

    SZL = "Silesian"
    """Silesian"""

    ANG = "Anglo-Saxon"
    """Anglo-Saxon"""

    NV = "Navajo"
    """Navajo"""

    IE = "Interlingue"
    """Interlingue"""

    ACE = "Acehnese"
    """Acehnese"""

    EXT = "Extremaduran"
    """Extremaduran"""

    FRP = "Franco-Provençal/Arpitan"
    """Franco-Provençal/Arpitan"""

    MWL = "Mirandese"
    """Mirandese"""

    LN = "Lingala"
    """Lingala"""

    SN = "Shona"
    """Shona"""

    DSB = "Lower Sorbian"
    """Lower Sorbian"""

    LEZ = "Lezgian"
    """Lezgian"""

    PFL = "Palatinate German"
    """Palatinate German"""

    KRC = "Karachay-Balkar"
    """Karachay-Balkar"""

    HAW = "Hawaiian"
    """Hawaiian"""

    PDC = "Pennsylvania German"
    """Pennsylvania German"""

    KAB = "Kabyle"
    """Kabyle"""

    XAL = "Kalmyk"
    """Kalmyk"""

    RW = "Kinyarwanda"
    """Kinyarwanda"""

    MYV = "Erzya"
    """Erzya"""

    TO = "Tongan"
    """Tongan"""

    ARC = "Aramaic", True
    """Aramaic"""

    KL = "Greenlandic"
    """Greenlandic"""

    BJN = "Banjar"
    """Banjar"""

    KBD = "Kabardian Circassian"
    """Kabardian Circassian"""

    LO = "Lao"
    """Lao"""

    HA = "Hausa"
    """Hausa"""

    PAP = "Papiamentu"
    """Papiamentu"""

    TPI = "Tok Pisin"
    """Tok Pisin"""

    AV = "Avar"
    """Avar"""

    LBE = "Lak"
    """Lak"""

    MDF = "Moksha"
    """Moksha"""

    JBO = "Lojban"
    """Lojban"""

    WO = "Wolof"
    """Wolof"""

    NA = "Nauruan"
    """Nauruan"""

    BXR = "Buryat (Russia)"
    """Buryat (Russia)"""

    TY = "Tahitian"
    """Tahitian"""

    SRN = "Sranan"
    """Sranan"""

    IG = "Igbo"
    """Igbo"""

    NSO = "Northern Sotho"
    """Northern Sotho"""

    KG = "Kongo"
    """Kongo"""

    TET = "Tetum"
    """Tetum"""

    KAA = "Karakalpak"
    """Karakalpak"""

    AB = "Abkhazian"
    """Abkhazian"""

    LTG = "Latgalian"
    """Latgalian"""

    ZU = "Zulu"
    """Zulu"""

    ZA = "Zhuang"
    """Zhuang"""

    TYV = "Tuvan"
    """Tuvan"""

    CDO = "Min Dong"
    """Min Dong"""

    CHY = "Cheyenne"
    """Cheyenne"""

    RMY = "Romani"
    """Romani"""

    CU = "Old Church Slavonic"
    """Old Church Slavonic"""

    TN = "Tswana"
    """Tswana"""

    CHR = "Cherokee"
    """Cherokee"""

    ROA_RUP = "Aromanian"
    """Aromanian"""

    TW = "Twi"
    """Twi"""

    GOT = "Gothic"
    """Gothic"""

    BI = "Bislama"
    """Bislama"""

    PIH = "Norfolk"
    """Norfolk"""

    SM = "Samoan"
    """Samoan"""

    RN = "Kirundi"
    """Kirundi"""

    BM = "Bambara"
    """Bambara"""

    MO = "Moldovan"
    """Moldovan"""

    SS = "Swati"
    """Swati"""

    IU = "Inuktitut"
    """Inuktitut"""

    SD = "Sindhi", True
    """Sindhi"""

    PNT = "Pontic"
    """Pontic"""

    KI = "Kikuyu"
    """Kikuyu"""

    OM = "Oromo"
    """Oromo"""

    XH = "Xhosa"
    """Xhosa"""

    TS = "Tsonga"
    """Tsonga"""

    EE = "Ewe"
    """Ewe"""

    AK = "Akan"
    """Akan"""

    FJ = "Fijian"
    """Fijian"""

    TI = "Tigrinya"
    """Tigrinya"""

    KS = "Kashmiri", True
    """Kashmiri"""

    LG = "Luganda"
    """Luganda"""

    SG = "Sango"
    """Sango"""

    NY = "Chichewa"
    """Chichewa"""

    FF = "Fula"
    """Fula"""

    VE = "Venda"
    """Venda"""

    CR = "Cree"
    """Cree"""

    ST = "Sesotho"
    """Sesotho"""

    DZ = "Dzongkha"
    """Dzongkha"""

    TUM = "Tumbuka"
    """Tumbuka"""

    IK = "Inupiak"
    """Inupiak"""

    CH = "Chamorro"
    """Chamorro"""

    MUL = "International"
    """International"""

    SH = "Serbo-Croatian"
    """Serbo-Croatian"""

    AZB = "South Azerbaijani", True
    """South Azerbaijani"""

    MAI = "Maithili"
    """Maithili"""

    LRC = "Northern Luri", True
    """Northern Luri"""

    GOM = "Goan Konkani"
    """Goan Konkani"""

    OLO = "Livvinkarjala"
    """Livvinkarjala"""

    JAM = "Patois"
    """Patois"""

    TCY = "Tulu"
    """Tulu"""

    ADY = "Adyghe"
    """Adyghe"""

    ZH_SIMPLIFIED = "Simplified Chinese"
    """Simplified Chinese"""

    """NEW LANGUAGES FROM WIKTIONARY(5 or more occurrences in Wiktionary) * /"""

    ENM = "Middle English"
    """Middle English"""

    GRC = "Ancient Greek"
    """Ancient Greek"""

    XCL = "Old Armenian"
    """Old Armenian"""

    SYC = "Classical Syriac", True
    """Classical Syriac"""

    FRO = "Old French"
    """Old French"""

    GEM_PRO = "Proto-Germanic"
    """Proto-Germanic"""

    NON = "Old Norse"
    """Old Norse"""

    GMQ_BOT = "Westrobothnian"
    """Westrobothnian"""

    FRM = "Middle French"
    """Middle French"""

    SLA_PRO = "Proto-Slavic"
    """Proto-Slavic"""

    SGA = "Old Irish"
    """Old Irish"""

    DUM = "Middle Dutch"
    """Middle Dutch"""

    OTA = "Ottoman Turkish", True
    """Ottoman Turkish"""

    NCI = "Classical Nahuatl"
    """Classical Nahuatl"""

    OSX = "Old Saxon"
    """Old Saxon"""

    GOH = "Old High German"
    """Old High German"""

    CIM = "Cimbrian"
    """Cimbrian"""

    HIL = "Hiligaynon"
    """Hiligaynon"""

    INE_PRO = "Proto-Indo-European"
    """Proto-Indo-European"""

    TXB = "Tocharian B"
    """Tocharian B"""

    MH = "Marshallese"
    """Marshallese"""

    SMI_PRO = "Proto-Samic"
    """Proto-Samic"""

    HRX = "Hunsrik"
    """Hunsrik"""

    COP = "Coptic"
    """Coptic"""

    WYM = "Vilamovian"
    """Vilamovian"""

    MNC = "Manchu"
    """Manchu"""

    BNT_PHU = "Phuthi"
    """Phuthi"""

    DLM = "Dalmatian"
    """Dalmatian"""

    ARN = "Mapudungun"
    """Mapudungun"""

    FIU_FIN_PRO = "Proto-Finnic"
    """Proto-Finnic"""

    GMQ_OSW = "Old Swedish"
    """Old Swedish"""

    MFE = "Mauritian Creole"
    """Mauritian Creole"""

    SMJ = "Lule Sami"
    """Lule Sami"""

    IZH = "Ingrian"
    """Ingrian"""

    ACW = "Hijazi Arabic", True
    """Hijazi Arabic"""

    CHK = "Chuukese"
    """Chuukese"""

    KEA = "Kabuverdianu"
    """Kabuverdianu"""

    KYJ = "Karao"
    """Karao"""

    ODT = "Old Dutch"
    """Old Dutch"""

    CEL_PRO = "Proto-Celtic"
    """Proto-Celtic"""

    CKV = "Kavalan"
    """Kavalan"""

    PDT = "Plautdietsch"
    """Plautdietsch"""

    AMI = "Amis"
    """Amis"""

    UGA = "Ugaritic"
    """Ugaritic"""

    LIV = "Livonian"
    """Livonian"""

    LZZ = "Laz"
    """Laz"""

    EGL = "Emilian"
    """Emilian"""

    DUO = "Dupaningan Agta"
    """Dupaningan Agta"""

    KLD = "Gamilaraay"
    """Gamilaraay"""

    KRL = "Karelian"
    """Karelian"""

    RYU = "Okinawan"
    """Okinawan"""

    ARY = "Moroccan Arabic", True
    """Moroccan Arabic"""

    CHO = "Choctaw"
    """Choctaw"""

    IIR_PRO = "Proto-Indo-Iranian"
    """Proto-Indo-Iranian"""

    NR = "Southern Ndebele"
    """Southern Ndebele"""

    SMN = "Inari Sami"
    """Inari Sami"""

    VOT = "Votic"
    """Votic"""

    SMS = "Skolt Sami"
    """Skolt Sami"""

    OJ = "Ojibwe"
    """Ojibwe"""

    NHE = "Eastern Huasteca Nahuatl"
    """Eastern Huasteca Nahuatl"""

    PRO = "Old Occitan"
    """Old Occitan"""

    GMW_CFR = "Central Franconian"
    """Central Franconian"""

    SHN = "Shan"
    """Shan"""

    ROA_OPT = "Old Portuguese"
    """Old Portuguese"""

    BAL = "Baluchi", True
    """Baluchi"""

    AFB = "Gulf Arabic", True
    """Gulf Arabic"""

    CHL = "Cahuilla"
    """Cahuilla"""

    CIC = "Chickasaw"
    """Chickasaw"""

    MCH = "Maquiritari"
    """Maquiritari"""

    KLS = "Kalasha"
    """Kalasha"""

    KXD = "Brunei Malay"
    """Brunei Malay"""

    KMK = "Limos Kalinga"
    """Limos Kalinga"""

    IST = "Istriot"
    """Istriot"""

    OGE = "Old Georgian"
    """Old Georgian"""

    ORH = "Oroqen"
    """Oroqen"""

    CCC = "Chamicuro"
    """Chamicuro"""

    DAK = "Dakota"
    """Dakota"""

    SJE = "Pite Sami"
    """Pite Sami"""

    LKT = "Lakota"
    """Lakota"""

    PJT = "Pitjantjatjara"
    """Pitjantjatjara"""

    LUD = "Ludian"
    """Ludian"""

    NMN = "ǃXóõ"
    """ǃXóõ"""

    BAN = "Balinese"
    """Balinese"""

    OJP = "Old Japanese"
    """Old Japanese"""

    SAT = "Santali"
    """Santali"""

    ITC_PRO = "Proto-Italic"
    """Proto-Italic"""

    MWW = "White Hmong"
    """White Hmong"""

    POV = "Guinea-Bissau Creole"
    """Guinea-Bissau Creole"""

    KHB = "Lü"
    """Lü"""

    CRS = "Seychellois Creole"
    """Seychellois Creole"""

    OFS = "Old Frisian"
    """Old Frisian"""

    NHG = "Tetelcingo Nahuatl"
    """Tetelcingo Nahuatl"""

    RAP = "Rapa Nui"
    """Rapa Nui"""

    AXM = "Middle Armenian"
    """Middle Armenian"""

    KJH = "Khakas"
    """Khakas"""

    BNT_PRO = "Proto-Bantu"
    """Proto-Bantu"""

    LSI = "Lashi"
    """Lashi"""

    ND = "Northern Ndebele"
    """Northern Ndebele"""

    MGA = "Middle Irish"
    """Middle Irish"""

    ZLW_OPL = "Old Polish"
    """Old Polish"""

    AKK = "Akkadian"
    """Akkadian"""

    ZOM = "Zou"
    """Zou"""

    HTS = "Hadza"
    """Hadza"""

    VAI = "Vai"
    """Vai"""

    URJ_PRO = "Proto-Uralic"
    """Proto-Uralic"""

    APW = "Western Apache"
    """Western Apache"""

    SUX = "Sumerian"
    """Sumerian"""

    OSP = "Old Spanish"
    """Old Spanish"""

    AIN = "Ainu"
    """Ainu"""

    QUC = "K'iche'"
    """K'iche'"""

    STR = "Saanich"
    """Saanich"""

    YUR = "Yurok"
    """Yurok"""

    PEO = "Old Persian"
    """Old Persian"""

    PAL = "Middle Persian"
    """Middle Persian"""

    RAJ = "Rajasthani"
    """Rajasthani"""

    SYL = "Sylheti"
    """Sylheti"""

    TPW = "Old Tupi"
    """Old Tupi"""

    PPL = "Pipil"
    """Pipil"""

    KUM = "Kumyk"
    """Kumyk"""

    OVD = "Elfdalian"
    """Elfdalian"""

    YUA = "Yucatec Maya"
    """Yucatec Maya"""

    ALU = "'Are'are"
    """'Are'are"""

    BHO = "Bhojpuri"
    """Bhojpuri"""

    SJD = "Kildin Sami"
    """Kildin Sami"""

    PRG = "Old Prussian"
    """Old Prussian"""

    GMY = "Mycenaean Greek"
    """Mycenaean Greek"""

    HIT = "Hittite"
    """Hittite"""

    POZ_PRO = "Proto-Malayo-Polynesian"
    """Proto-Malayo-Polynesian"""

    TAO = "Yami"
    """Yami"""

    INE_BSL_PRO = "Proto-Balto-Slavic"
    """Proto-Balto-Slavic"""

    WAU = "Wauja"
    """Wauja"""

    GML = "Middle Low German"
    """Middle Low German"""

    UNM = "Unami"
    """Unami"""

    SIT_PRO = "Proto-Sino-Tibetan"
    """Proto-Sino-Tibetan"""

    SMA = "Southern Sami"
    """Southern Sami"""

    IRA_PRO = "Proto-Iranian"
    """Proto-Iranian"""

    MCQ = "Ese"
    """Ese"""

    MNW = "Mon"
    """Mon"""

    SEM_PRO = "Proto-Semitic"
    """Proto-Semitic"""

    BYK = "Biao"
    """Biao"""

    IUM = "Iu Mien"
    """Iu Mien"""

    YAG = "Yámana"
    """Yámana"""

    XTO = "Tocharian A"
    """Tocharian A"""

    HOP = "Hopi"
    """Hopi"""

    EVN = "Evenki"
    """Evenki"""

    MNS = "Mansi"
    """Mansi"""

    KAW = "Old Javanese"
    """Old Javanese"""

    PMH = "Maharastri Prakrit"
    """Maharastri Prakrit"""

    XNB = "Kanakanabu"
    """Kanakanabu"""

    AER = "Eastern Arrernte"
    """Eastern Arrernte"""

    AYL = "Libyan Arabic", True
    """Libyan Arabic"""

    MSK = "Mansaka"
    """Mansaka"""

    ALE = "Aleut"
    """Aleut"""

    AE = "Avestan", True
    """Avestan"""

    VGR = "Vaghri"
    """Vaghri"""

    RHG = "Rohingya", True
    """Rohingya"""

    GLD = "Nanai"
    """Nanai"""

    NFL = "Aiwoo"
    """Aiwoo"""

    MPM = "Yosondúa Mixtec"
    """Yosondúa Mixtec"""

    ORV = "Old East Slavic"
    """Old East Slavic"""

    XBR = "Kambera"
    """Kambera"""

    POX = "Polabian"
    """Polabian"""

    SJU = "Ume Sami"
    """Ume Sami"""

    KSW = "S'gaw Karen"
    """S'gaw Karen"""

    JPX_PRO = "Proto-Japonic"
    """Proto-Japonic"""

    MAP_PRO = "Proto-Austronesian"
    """Proto-Austronesian"""

    CJS = "Shor"
    """Shor"""

    APC = "North Levantine Arabic", True
    """North Levantine Arabic"""

    PON = "Pohnpeian"
    """Pohnpeian"""

    ARP = "Arapaho"
    """Arapaho"""

    ROA_GAL = "Gallo"
    """Gallo"""

    ITL = "Itelmen"
    """Itelmen"""

    MVI = "Miyako"
    """Miyako"""

    PLW = "Brooke's Point Palawano"
    """Brooke's Point Palawano"""

    SSF = "Thao"
    """Thao"""

    YAI = "Yagnobi"
    """Yagnobi"""

    ALT = "Southern Altai"
    """Southern Altai"""

    MFH = "Matal"
    """Matal"""

    MSB = "Masbatenyo"
    """Masbatenyo"""

    ALG_PRO = "Proto-Algonquian"
    """Proto-Algonquian"""

    SJT = "Ter Sami"
    """Ter Sami"""

    WRH = "Wiradhuri"
    """Wiradhuri"""

    SCE = "Dongxiang"
    """Dongxiang"""

    KFR = "Kachchi"
    """Kachchi"""

    TZO = "Tzotzil"
    """Tzotzil"""

    OTK = "Old Turkic"
    """Old Turkic"""

    POI = "Highland Popoluca"
    """Highland Popoluca"""

    TRK_PRO = "Proto-Turkic"
    """Proto-Turkic"""

    DNG = "Dungan"
    """Dungan"""

    CSM = "Central Sierra Miwok"
    """Central Sierra Miwok"""

    AZG = "San Pedro Amuzgos Amuzgo"
    """San Pedro Amuzgos Amuzgo"""

    NCH = "Central Huasteca Nahuatl"
    """Central Huasteca Nahuatl"""

    STP = "Southeastern Tepehuan"
    """Southeastern Tepehuan"""

    GRK_PRO = "Proto-Hellenic"
    """Proto-Hellenic"""

    PAU = "Palauan"
    """Palauan"""

    GMQ_SCY = "Scanian"
    """Scanian"""

    MIC = "Mi'kmaq"
    """Mi'kmaq"""

    EUQ_PRO = "Proto-Basque"
    """Proto-Basque"""

    YOI = "Yonaguni"
    """Yonaguni"""

    PHN = "Phoenician", True
    """Phoenician"""

    GMH = "Middle High German"
    """Middle High German"""

    NRN = "Norn"
    """Norn"""

    OTE = "Mezquital Otomi"
    """Mezquital Otomi"""

    BLT = "Tai Dam"
    """Tai Dam"""

    TZM = "Central Atlas Tamazight"
    """Central Atlas Tamazight"""

    WLM = "Middle Welsh"
    """Middle Welsh"""

    KKY = "Guugu Yimidhirr"
    """Guugu Yimidhirr"""

    FAY = "Southwestern Fars"
    """Southwestern Fars"""

    TDD = "Tai Nüa"
    """Tai Nüa"""

    WBP = "Warlpiri"
    """Warlpiri"""

    TSU = "Tsou"
    """Tsou"""

    PCC = "Bouyei"
    """Bouyei"""

    AHO = "Ahom"
    """Ahom"""

    XUG = "Kunigami"
    """Kunigami"""

    MFY = "Mayo"
    """Mayo"""

    RYS = "Yaeyama"
    """Yaeyama"""

    SEM_SRB = "Old South Arabian", True
    """Old South Arabian"""

    TCS = "Torres Strait Creole"
    """Torres Strait Creole"""

    ZPQ = "Zoogocho Zapotec"
    """Zoogocho Zapotec"""

    CEL_GAU = "Gaulish"
    """Gaulish"""

    ULC = "Ulch"
    """Ulch"""

    WMW = "Mwani"
    """Mwani"""

    POE = "San Juan Atzingo Popoloca"
    """San Juan Atzingo Popoloca"""

    LIF = "Limbu"
    """Limbu"""

    ABE = "Abenaki"
    """Abenaki"""

    RMF = "Kalo Finnish Romani"
    """Kalo Finnish Romani"""

    ZOR = "Rayón Zoque"
    """Rayón Zoque"""

    KAM = "Kamba"
    """Kamba"""

    KYU = "Western Kayah"
    """Western Kayah"""

    TIY = "Tiruray"
    """Tiruray"""

    POZ_POL_PRO = "Proto-Polynesian"
    """Proto-Polynesian"""

    ALR = "Alutor"
    """Alutor"""

    ZKO = "Kott"
    """Kott"""

    BNO = "Asi"
    """Asi"""

    INH = "Ingush"
    """Ingush"""

    ROO = "Rotokas"
    """Rotokas"""

    OTY = "Old Tamil"
    """Old Tamil"""

    ABG = "Abaga"
    """Abaga"""

    GMQ_ODA = "Old Danish"
    """Old Danish"""

    SEI = "Seri"
    """Seri"""

    FNG = "Fanagalo"
    """Fanagalo"""

    ROP = "Kriol"
    """Kriol"""

    NCJ = "Northern Puebla Nahuatl"
    """Northern Puebla Nahuatl"""

    SKS = "Maia"
    """Maia"""

    NOD = "Northern Thai"
    """Northern Thai"""

    CAK = "Kaqchikel"
    """Kaqchikel"""

    XAG = "Aghwan"
    """Aghwan"""

    KPV = "Komi-Zyrian"
    """Komi-Zyrian"""

    OOD = "O'odham"
    """O'odham"""

    BRA = "Braj"
    """Braj"""

    ONW = "Old Nubian"
    """Old Nubian"""

    YOL = "Yola"
    """Yola"""

    MKH_PRO = "Proto-Mon-Khmer"
    """Proto-Mon-Khmer"""

    CHN = "Chinook Jargon"
    """Chinook Jargon"""

    AKZ = "Alabama"
    """Alabama"""

    PUA = "Purepecha"
    """Purepecha"""

    JAA = "Jamamadí"
    """Jamamadí"""

    UDE = "Udihe"
    """Udihe"""

    CAB = "Garifuna"
    """Garifuna"""

    BDQ = "Bahnar"
    """Bahnar"""

    MHN = "Mòcheno"
    """Mòcheno"""

    CDC_PRO = "Proto-Chadic"
    """Proto-Chadic"""

    HAJ = "Hajong"
    """Hajong"""

    GME_CGO = "Crimean Gothic"
    """Crimean Gothic"""

    UGO = "Gong"
    """Gong"""

    KMR = "Northern Kurdish"
    """Northern Kurdish"""

    XTM = "Magdalena Peñasco Mixtec"
    """Magdalena Peñasco Mixtec"""

    RMW = "Welsh Romani"
    """Welsh Romani"""

    RIF = "Tarifit"
    """Tarifit"""

    CTS = "Northern Catanduanes Bicolano"
    """Northern Catanduanes Bicolano"""

    II = "Sichuan Yi"
    """Sichuan Yi"""

    LSD = "Lishana Deni", True
    """Lishana Deni"""

    BLK = "Pa'o Karen"
    """Pa'o Karen"""

    OKA = "Okanagan"
    """Okanagan"""

    PAO = "Northern Paiute"
    """Northern Paiute"""

    MNK = "Mandinka"
    """Mandinka"""

    COG = "Chong"
    """Chong"""

    TAR = "Central Tarahumara"
    """Central Tarahumara"""

    TUW_PRO = "Proto-Tungusic"
    """Proto-Tungusic"""

    NIU = "Niuean"
    """Niuean"""

    NIO = "Nganasan"
    """Nganasan"""

    AWA = "Awadhi"
    """Awadhi"""

    OAA = "Orok"
    """Orok"""

    SNE = "Bau Bidayuh"
    """Bau Bidayuh"""

    RMQ = "Caló"
    """Caló"""

    SKB = "Saek"
    """Saek"""

    MEL = "Central Melanau"
    """Central Melanau"""

    SVM = "Slavomolisano"
    """Slavomolisano"""

    DHV = "Drehu"
    """Drehu"""

    CRO = "Crow"
    """Crow"""

    COM = "Comanche"
    """Comanche"""

    JIV = "Shuar"
    """Shuar"""

    PSU = "Sauraseni Prakrit"
    """Sauraseni Prakrit"""

    CIA = "Cia-Cia"
    """Cia-Cia"""

    BSK = "Burushaski"
    """Burushaski"""

    TRV = "Taroko"
    """Taroko"""

    XFA = "Faliscan"
    """Faliscan"""

    DTY = "Doteli"
    """Doteli"""

    BRX = "Bodo (India)"
    """Bodo (India)"""

    UDI = "Udi"
    """Udi"""

    SBF = "Shabo"
    """Shabo"""

    SVA = "Svan"
    """Svan"""

    MTR = "Mewari"
    """Mewari"""

    LIL = "Lillooet"
    """Lillooet"""

    GUP = "Gunwinggu"
    """Gunwinggu"""

    TLY = "Talysh"
    """Talysh"""

    SLM = "Pangutaran Sama"
    """Pangutaran Sama"""

    UMB = "Umbundu"
    """Umbundu"""

    MOP = "Mopan Maya"
    """Mopan Maya"""

    DLG = "Dolgan"
    """Dolgan"""

    XPU = "Punic", True
    """Punic"""

    IBL = "Ibaloi"
    """Ibaloi"""

    XLU = "Luwian"
    """Luwian"""

    GNI = "Gooniyandi"
    """Gooniyandi"""

    KPY = "Koryak"
    """Koryak"""

    TLI = "Tlingit"
    """Tlingit"""

    MJC = "San Juan Colorado Mixtec"
    """San Juan Colorado Mixtec"""

    AJI = "Ajië"
    """Ajië"""

    RGN = "Romagnol"
    """Romagnol"""

    LBJ = "Ladakhi"
    """Ladakhi"""

    CHG = "Chagatai", True
    """Chagatai"""

    KLG = "Tagakaulu Kalagan"
    """Tagakaulu Kalagan"""

    KHW = "Khowar", True
    """Khowar"""

    GEZ = "Ge'ez"
    """Ge'ez"""

    JRB = "Judeo-Arabic", True
    """Judeo-Arabic"""

    PIS = "Pijin"
    """Pijin"""

    NLL = "Nihali"
    """Nihali"""

    MTQ = "Muong"
    """Muong"""

    TXG = "Tangut"
    """Tangut"""

    TFT = "Ternate"
    """Ternate"""

    MUP = "Malvi"
    """Malvi"""

    XVN = "Vandalic"
    """Vandalic"""

    FAX = "Fala"
    """Fala"""

    BKM = "Kom (Cameroon)"
    """Kom (Cameroon)"""

    NYS = "Nyunga"
    """Nyunga"""

    YKG = "Northern Yukaghir"
    """Northern Yukaghir"""

    WYI = "Woiwurrung"
    """Woiwurrung"""

    IBA = "Iban"
    """Iban"""

    MRC = "Maricopa"
    """Maricopa"""

    MBT = "Matigsalug Manobo"
    """Matigsalug Manobo"""

    AA = "Afar"
    """Afar"""

    BSQ = "Bassa"
    """Bassa"""

    NTP = "Northern Tepehuan"
    """Northern Tepehuan"""

    TRU = "Turoyo", True
    """Turoyo"""

    MXI = "Mozarabic", True
    """Mozarabic"""

    BEU = "Blagar"
    """Blagar"""

    ROA_CHA = "Champenois"
    """Champenois"""

    CTA = "Tataltepec Chatino"
    """Tataltepec Chatino"""

    LOU = "Louisiana Creole French"
    """Louisiana Creole French"""

    XSY = "Saisiyat"
    """Saisiyat"""

    AMN = "Amanab"
    """Amanab"""

    PKA = "Ardhamagadhi Prakrit"
    """Ardhamagadhi Prakrit"""

    XTA = "Alcozauca Mixtec"
    """Alcozauca Mixtec"""

    SLE = "Sholaga"
    """Sholaga"""

    KET = "Ket"
    """Ket"""

    NEG = "Negidal"
    """Negidal"""

    DRA_PRO = "Proto-Dravidian"
    """Proto-Dravidian"""

    ABQ = "Abaza"
    """Abaza"""

    ZGH = "Moroccan Amazigh"
    """Moroccan Amazigh"""

    GMQ_GUT = "Gutnish"
    """Gutnish"""

    HCH = "Huichol"
    """Huichol"""

    ZAI = "Isthmus Zapotec"
    """Isthmus Zapotec"""

    ULK = "Meriam"
    """Meriam"""

    XAQ = "Aquitanian"
    """Aquitanian"""

    TBL = "Tboli"
    """Tboli"""

    RUQ = "Megleno-Romanian"
    """Megleno-Romanian"""

    SDH = "Southern Kurdish", True
    """Southern Kurdish"""

    LUS = "Mizo"
    """Mizo"""

    BKD = "Binukid"
    """Binukid"""

    XCR = "Carian"
    """Carian"""

    YAP = "Yapese"
    """Yapese"""

    XPO = "Pochutec"
    """Pochutec"""

    ZLW_SLV = "Slovincian"
    """Slovincian"""

    ART_BLK = "Bolak"
    """Bolak"""

    MID = "Mandaic", True
    """Mandaic"""

    OMN = "Minoan"
    """Minoan"""

    NOG = "Nogai"
    """Nogai"""

    CGC = "Kagayanen"
    """Kagayanen"""

    LUO = "Luo"
    """Luo"""

    SMK = "Bolinao"
    """Bolinao"""

    JAC = "Jakaltek"
    """Jakaltek"""

    TUB = "Tübatulabal"
    """Tübatulabal"""

    FLA = "Montana Salish"
    """Montana Salish"""

    DIN = "Dinka"
    """Dinka"""

    NHN = "Central Nahuatl"
    """Central Nahuatl"""

    GMW_ECG = "East Central German"
    """East Central German"""

    XXT = "Tambora"
    """Tambora"""

    POZ_OCE_PRO = "Proto-Oceanic"
    """Proto-Oceanic"""

    CAG = "Nivaclé"
    """Nivaclé"""

    KCA = "Khanty"
    """Khanty"""

    XPM = "Pumpokol"
    """Pumpokol"""

    GMQ_PRO = "Proto-Norse"
    """Proto-Norse"""

    BLC = "Bella Coola"
    """Bella Coola"""

    CKT = "Chukchi"
    """Chukchi"""

    MOH = "Mohawk"
    """Mohawk"""

    RMN = "Balkan Romani"
    """Balkan Romani"""

    NHM = "Morelos Nahuatl"
    """Morelos Nahuatl"""

    XPR = "Parthian"
    """Parthian"""

    XWO = "Written Oirat"
    """Written Oirat"""

    AVD = "Alviri-Vidari", True
    """Alviri-Vidari"""

    HO = "Hiri Motu"
    """Hiri Motu"""

    TSD = "Tsakonian"
    """Tsakonian"""

    SWB = "Maore Comorian"
    """Maore Comorian"""

    XLD = "Lydian", True
    """Lydian"""

    MIR = "Isthmus Mixe"
    """Isthmus Mixe"""

    ZLE_ONO = "Old Novgorodian"
    """Old Novgorodian"""

    APQ = "A-Pucikwar"
    """A-Pucikwar"""

    GBM = "Garhwali"
    """Garhwali"""

    RAD = "Rade"
    """Rade"""

    MAD = "Madurese"
    """Madurese"""

    GWC = "Kalami", True
    """Kalami"""

    XDC = "Dacian"
    """Dacian"""

    CCS_PRO = "Proto-Kartvelian"
    """Proto-Kartvelian"""

    RMC = "Carpathian Romani"
    """Carpathian Romani"""

    NJZ = "Nyishi"
    """Nyishi"""

    WYB = "Ngiyambaa"
    """Ngiyambaa"""

    COL = "Columbia-Wenatchi"
    """Columbia-Wenatchi"""

    NIA = "Nias"
    """Nias"""

    WNY = "Wanyi"
    """Wanyi"""

    AZC_PRO = "Proto-Uto-Aztecan"
    """Proto-Uto-Aztecan"""

    XPQ = "Mohegan-Pequot"
    """Mohegan-Pequot"""

    SAS = "Sasak"
    """Sasak"""

    AZC_NAH_PRO = "Proto-Nahuan"
    """Proto-Nahuan"""

    DJK = "Aukan"
    """Aukan"""

    RME = "Angloromani"
    """Angloromani"""

    ZAB = "San Juan Guelavía Zapotec"
    """San Juan Guelavía Zapotec"""

    DUF = "Dumbea"
    """Dumbea"""

    JDT = "Judeo-Tat"
    """Judeo-Tat"""

    BBC = "Toba Batak"
    """Toba Batak"""

    CAU_CIR_PRO = "Proto-Circassian"
    """Proto-Circassian"""

    XLC = "Lycian"
    """Lycian"""

    XRN = "Arin"
    """Arin"""

    SCL = "Shina", True
    """Shina"""

    BEW = "Betawi"
    """Betawi"""

    MIQ = "Miskito"
    """Miskito"""

    YIJ = "Yindjibarndi"
    """Yindjibarndi"""

    CPG = "Cappadocian Greek"
    """Cappadocian Greek"""

    KSI = "Krisa"
    """Krisa"""

    EVE = "Even"
    """Even"""

    DAR = "Dargwa"
    """Dargwa"""

    ARL = "Arabela"
    """Arabela"""

    GIL = "Gilbertese"
    """Gilbertese"""

    GMQ_JMK = "Jamtish"
    """Jamtish"""

    UMU = "Munsee"
    """Munsee"""

    DOI = "Dogri"
    """Dogri"""

    APE = "Bukiyip"
    """Bukiyip"""

    CRK = "Plains Cree"
    """Plains Cree"""

    MEO = "Kedah Malay"
    """Kedah Malay"""

    NAQ = "Nama"
    """Nama"""

    DGR = "Dogrib"
    """Dogrib"""

    SAM = "Samaritan Aramaic", True
    """Samaritan Aramaic"""

    UVL = "Lote"
    """Lote"""

    TRW = "Torwali", True
    """Torwali"""

    THP = "Thompson"
    """Thompson"""

    TEH = "Tehuelche"
    """Tehuelche"""

    LEP = "Lepcha"
    """Lepcha"""

    CJH = "Upper Chehalis"
    """Upper Chehalis"""

    TFN = "Dena'ina"
    """Dena'ina"""

    DTA = "Daur"
    """Daur"""

    YOX = "Yoron"
    """Yoron"""

    KGP = "Kaingang"
    """Kaingang"""

    FIT = "Meänkieli"
    """Meänkieli"""

    TIG = "Tigre"
    """Tigre"""

    NLC = "Nalca"
    """Nalca"""

    BNN = "Bunun"
    """Bunun"""

    IDB = "Indo-Portuguese"
    """Indo-Portuguese"""

    IBG = "Ibanag"
    """Ibanag"""

    MYN_PRO = "Proto-Mayan"
    """Proto-Mayan"""

    BOR = "Borôro"
    """Borôro"""

    GMW_JDT = "Jersey Dutch"
    """Jersey Dutch"""

    XUM = "Umbrian"
    """Umbrian"""

    OSC = "Oscan"
    """Oscan"""

    HUQ = "Tsat"
    """Tsat"""

    SIP = "Sikkimese"
    """Sikkimese"""

    WLS = "Wallisian"
    """Wallisian"""

    XBC = "Bactrian"
    """Bactrian"""

    INC_OHI = "Old Hindi"
    """Old Hindi"""

    MWR = "Marwari"
    """Marwari"""

    KIJ = "Kilivila"
    """Kilivila"""

    ZDJ = "Ngazidja Comorian"
    """Ngazidja Comorian"""

    CSI = "Coast Miwok"
    """Coast Miwok"""

    AGT = "Central Cagayan Agta"
    """Central Cagayan Agta"""

    TIO = "Teop"
    """Teop"""

    GOR = "Gorontalo"
    """Gorontalo"""

    AEB = "Tunisian Arabic", True
    """Tunisian Arabic"""

    BLA = "Blackfoot"
    """Blackfoot"""

    MYP = "Pirahã"
    """Pirahã"""

    CRG = "Michif"
    """Michif"""

    YAQ = "Yaqui"
    """Yaqui"""

    CTP = "Western Highland Chatino"
    """Western Highland Chatino"""

    WBL = "Wakhi"
    """Wakhi"""

    ZUN = "Zuni"
    """Zuni"""

    IXL = "Ixil"
    """Ixil"""

    ITC_OLA = "Old Latin"
    """Old Latin"""

    WIM = "Wik-Mungkan"
    """Wik-Mungkan"""

    NMC = "Ngam"
    """Ngam"""

    XSS = "Assan"
    """Assan"""

    CHP = "Chipewyan"
    """Chipewyan"""

    OWL = "Old Welsh"
    """Old Welsh"""

    OKN = "Oki-No-Erabu"
    """Oki-No-Erabu"""

    INE_ANA_PRO = "Proto-Anatolian"
    """Proto-Anatolian"""

    SHI = "Tashelhit"
    """Tashelhit"""

    HAI = "Haida"
    """Haida"""

    NMY = "Namuyi"
    """Namuyi"""

    EGX_DEM = "Demotic"
    """Demotic"""

    XMZ = "Mori Bawah"
    """Mori Bawah"""

    THM = "Thavung"
    """Thavung"""

    AII = "Assyrian Neo-Aramaic", True
    """Assyrian Neo-Aramaic"""

    RAR = "Rarotongan"
    """Rarotongan"""

    MEZ = "Menominee"
    """Menominee"""

    AQC = "Archi"
    """Archi"""

    OUI = "Old Uyghur"
    """Old Uyghur"""

    CPE_SPP = "Samoan Plantation Pidgin"
    """Samoan Plantation Pidgin"""

    BDK = "Budukh"
    """Budukh"""

    JUC = "Jurchen"
    """Jurchen"""

    WBA = "Warao"
    """Warao"""

    RTM = "Rotuman"
    """Rotuman"""

    URK = "Urak Lawoi'"
    """Urak Lawoi'"""

    ADA = "Adangme"
    """Adangme"""

    UBU = "Umbu-Ungu"
    """Umbu-Ungu"""

    APY = "Apalaí"
    """Apalaí"""

    ALQ = "Algonquin"
    """Algonquin"""

    KLA = "Klamath-Modoc"
    """Klamath-Modoc"""

    LEW = "Ledo Kaili"
    """Ledo Kaili"""

    NEZ = "Nez Perce"
    """Nez Perce"""

    DRA_OKN = "Halegannada"
    """Halegannada"""

    NHW = "Western Huasteca Nahuatl"
    """Western Huasteca Nahuatl"""

    ZAV = "Yatzachi Zapotec"
    """Yatzachi Zapotec"""

    TAI_PRO = "Proto-Tai"
    """Proto-Tai"""

    TSG = "Tausug"
    """Tausug"""

    PGL = "Primitive Irish"
    """Primitive Irish"""

    AOZ = "Uab Meto"
    """Uab Meto"""

    TKL = "Tokelauan"
    """Tokelauan"""

    CAR = "Galibi Carib"
    """Galibi Carib"""

    BBL = "Bats"
    """Bats"""

    XPG = "Phrygian"
    """Phrygian"""

    OBM = "Moabite", True
    """Moabite"""

    AMM = "Ama"
    """Ama"""

    GMW_RFR = "Rhine Franconian"
    """Rhine Franconian"""

    LND = "Lun Bawang"
    """Lun Bawang"""

    CUP = "Cupeño"
    """Cupeño"""

    STW = "Satawalese"
    """Satawalese"""

    PWN = "Paiwan"
    """Paiwan"""

    NIJ = "Ngaju"
    """Ngaju"""

    GUR = "Farefare"
    """Farefare"""

    BCH = "Bariai"
    """Bariai"""

    AGR = "Aguaruna"
    """Aguaruna"""

    BKU = "Buhid"
    """Buhid"""

    TAB = "Tabasaran"
    """Tabasaran"""

    JRA = "Jarai"
    """Jarai"""

    SHS = "Shuswap"
    """Shuswap"""

    MVV = "Tagal Murut"
    """Tagal Murut"""

    LIC = "Hlai"
    """Hlai"""

    KRK = "Kerek"
    """Kerek"""

    KR = "Kanuri"
    """Kanuri"""

    CHC = "Catawba"
    """Catawba"""

    GMW_GTS = "Gottscheerish"
    """Gottscheerish"""

    NGU = "Guerrero Nahuatl"
    """Guerrero Nahuatl"""

    DTD = "Ditidaht"
    """Ditidaht"""

    MZS = "Macanese"
    """Macanese"""

    AEM = "Arem"
    """Arem"""

    BRG = "Baure"
    """Baure"""

    CTU = "Chol"
    """Chol"""

    GMQ_MNO = "Middle Norwegian"
    """Middle Norwegian"""

    XMK = "Ancient Macedonian"
    """Ancient Macedonian"""

    PLO = "Oluta Popoluca"
    """Oluta Popoluca"""

    OAC = "Oroch"
    """Oroch"""

    MAK = "Makasar"
    """Makasar"""

    SKD = "Southern Sierra Miwok"
    """Southern Sierra Miwok"""

    ARW = "Arawak"
    """Arawak"""

    RML = "Baltic Romani"
    """Baltic Romani"""

    SOU = "Southern Thai"
    """Southern Thai"""

    CEA = "Lower Chehalis"
    """Lower Chehalis"""

    AGN = "Agutaynen"
    """Agutaynen"""

    TMH = "Tuareg"
    """Tuareg"""

    ITV = "Itawit"
    """Itawit"""

    BNY = "Bintulu"
    """Bintulu"""

    SAZ = "Saurashtra"
    """Saurashtra"""

    MFA = "Pattani Malay"
    """Pattani Malay"""

    CAL = "Carolinian"
    """Carolinian"""

    AAU = "Abau"
    """Abau"""

    KJ = "Kwanyama"
    """Kwanyama"""

    MAZ = "Central Mazahua"
    """Central Mazahua"""

    IBD = "Iwaidja"
    """Iwaidja"""

    OLE = "Olekha"
    """Olekha"""

    AIW = "Aari"
    """Aari"""

    QFA_CKA_PRO = "Proto-Chukotko-Kamchatkan"
    """Proto-Chukotko-Kamchatkan"""

    MLM = "Mulam"
    """Mulam"""

    AUD = "Anuta"
    """Anuta"""

    LOC = "Inonhan"
    """Inonhan"""

    BPL = "Broome Pearling Lugger Pidgin"
    """Broome Pearling Lugger Pidgin"""

    MHL = "Mauwake"
    """Mauwake"""

    MIY = "Ayutla Mixtec"
    """Ayutla Mixtec"""

    LAC = "Lacandon"
    """Lacandon"""

    PNW = "Panyjima"
    """Panyjima"""

    MRV = "Mangarevan"
    """Mangarevan"""

    TRK_OAT = "Old Anatolian Turkish", True
    """Old Anatolian Turkish"""

    RMT = "Domari"
    """Domari"""

    ALJ = "Alangan"
    """Alangan"""

    POT = "Potawatomi"
    """Potawatomi"""

    ETO = "Eton (Cameroon)"
    """Eton (Cameroon)"""

    AMW = "Western Neo-Aramaic", True
    """Western Neo-Aramaic"""

    XGF = "Gabrielino-Fernandeño"
    """Gabrielino-Fernandeño"""

    BRC = "Berbice Creole Dutch"
    """Berbice Creole Dutch"""

    MUS = "Creek"
    """Creek"""

    SKR = "Seraiki", True
    """Seraiki"""

    TDV = "Toro"
    """Toro"""

    PAD = "Paumarí"
    """Paumarí"""

    POS = "Sayula Popoluca"
    """Sayula Popoluca"""

    PAW = "Pawnee"
    """Pawnee"""

    BRH = "Brahui", True
    """Brahui"""

    BNP = "Bola"
    """Bola"""

    HNS = "Caribbean Hindustani"
    """Caribbean Hindustani"""

    MFI = "Wandala"
    """Wandala"""

    CWD = "Woods Cree"
    """Woods Cree"""

    XWA = "Kwaza"
    """Kwaza"""

    KOS = "Kosraean"
    """Kosraean"""

    COW = "Cowlitz"
    """Cowlitz"""

    OKM = "Middle Korean"
    """Middle Korean"""

    TEP = "Tepecano"
    """Tepecano"""

    CAA = "Ch'orti'"
    """Ch'orti'"""

    QYP = "Quiripi"
    """Quiripi"""

    TNA = "Tacana"
    """Tacana"""

    SKY = "Sikaiana"
    """Sikaiana"""

    LVK = "Lavukaleve"
    """Lavukaleve"""

    SHY = "Tachawit"
    """Tachawit"""

    TOW = "Jemez"
    """Jemez"""

    QWE_KCH = "Kichwa"
    """Kichwa"""

    KYI = "Kiput"
    """Kiput"""

    TNP = "Whitesands"
    """Whitesands"""

    AQG = "Arigidi"
    """Arigidi"""

    TOS = "Highland Totonac"
    """Highland Totonac"""

    TRP = "Kokborok"
    """Kokborok"""

    CAP = "Chipaya"
    """Chipaya"""

    XMR = "Meroitic"
    """Meroitic"""

    PPK = "Uma"
    """Uma"""

    FKV = "Kven"
    """Kven"""

    TAA = "Lower Tanana"
    """Lower Tanana"""

    MQM = "South Marquesan"
    """South Marquesan"""

    ANE = "Xârâcùù"
    """Xârâcùù"""

    MWF = "Murrinh-Patha"
    """Murrinh-Patha"""

    KPJ = "Karajá"
    """Karajá"""

    ZWA = "Zay"
    """Zay"""

    YUX = "Southern Yukaghir"
    """Southern Yukaghir"""

    MEW = "Maaka"
    """Maaka"""

    WAQ = "Wageman"
    """Wageman"""

    TYA = "Tauya"
    """Tauya"""

    CUI = "Cuiba"
    """Cuiba"""

    CRI = "Sãotomense"
    """Sãotomense"""

    ACM = "Iraqi Arabic", True
    """Iraqi Arabic"""

    CMG = "Classical Mongolian"
    """Classical Mongolian"""

    AAA = "Ghotuo"
    """Ghotuo"""

    TAY = "Atayal"
    """Atayal"""

    AAK = "Ankave"
    """Ankave"""

    KDD = "Yankunytjatjara"
    """Yankunytjatjara"""

    ARS = "Najdi Arabic", True
    """Najdi Arabic"""

    TNC = "Tanimuca-Retuarã"
    """Tanimuca-Retuarã"""

    BCF = "Bamu"
    """Bamu"""

    BEM = "Bemba"
    """Bemba"""

    DDR = "Dhudhuroa"
    """Dhudhuroa"""

    KRI = "Krio"
    """Krio"""

    NYN = "Nyankole"
    """Nyankole"""

    FUN = "Fulniô"
    """Fulniô"""

    MAQ = "Chiquihuitlán Mazatec"
    """Chiquihuitlán Mazatec"""

    YKA = "Yakan"
    """Yakan"""

    SEL = "Selkup"
    """Selkup"""

    PLN = "Palenquero"
    """Palenquero"""

    XAA = "Andalusian Arabic", True
    """Andalusian Arabic"""

    KMV = "Karipúna Creole French"
    """Karipúna Creole French"""

    TOP = "Papantla Totonac"
    """Papantla Totonac"""

    LMW = "Lake Miwok"
    """Lake Miwok"""

    DTR = "Lotud"
    """Lotud"""

    PYU = "Puyuma"
    """Puyuma"""

    AAP = "Pará Arára"
    """Pará Arára"""

    XPI = "Pictish"
    """Pictish"""

    ROA_FCM = "Franc-Comtois"
    """Franc-Comtois"""

    RTH = "Ratahan"
    """Ratahan"""

    BOJ = "Anjam"
    """Anjam"""

    KDR = "Karaim"
    """Karaim"""

    SGP = "Singpho"
    """Singpho"""

    SEM_AMM = "Ammonite", True
    """Ammonite"""

    AIH = "Ai-Cham"
    """Ai-Cham"""

    MSN = "Vurës"
    """Vurës"""

    DIS = "Dimasa"
    """Dimasa"""

    RUT = "Rutul"
    """Rutul"""

    COO = "Comox"
    """Comox"""

    ABJ = "Aka-Bea"
    """Aka-Bea"""

    DRQ = "Dura"
    """Dura"""

    UVE = "West Uvean"
    """West Uvean"""

    KPG = "Kapingamarangi"
    """Kapingamarangi"""

    MEU = "Motu"
    """Motu"""

    YWR = "Yawuru"
    """Yawuru"""

    TNQ = "Taíno"
    """Taíno"""

    YUF = "Havasupai-Walapai-Yavapai"
    """Havasupai-Walapai-Yavapai"""

    YAO = "Yao"
    """Yao"""

    MBL = "Maxakalí"
    """Maxakalí"""

    KKP = "Koko-Bera"
    """Koko-Bera"""

    AGX = "Aghul"
    """Aghul"""

    GEH = "Hutterisch"
    """Hutterisch"""

    XKZ = "Kurtop"
    """Kurtop"""

    MIH = "Chayuco Mixtec"
    """Chayuco Mixtec"""

    USP = "Uspanteco"
    """Uspanteco"""

    ITE = "Itene"
    """Itene"""

    TRR = "Taushiro"
    """Taushiro"""

    SMR = "Simeulue"
    """Simeulue"""

    TIH = "Timugon Murut"
    """Timugon Murut"""

    TVN = "Tavoyan"
    """Tavoyan"""

    ZAU = "Zangskari"
    """Zangskari"""

    MIA = "Miami"
    """Miami"""

    DNY = "Dení"
    """Dení"""

    UUN = "Kulon-Pazeh"
    """Kulon-Pazeh"""

    DGC = "Casiguran Dumagat Agta"
    """Casiguran Dumagat Agta"""

    SYD_PRO = "Proto-Samoyedic"
    """Proto-Samoyedic"""

    PLE = "Palu'e"
    """Palu'e"""

    KIP = "Sheshi Kham"
    """Sheshi Kham"""

    WLO = "Wolio"
    """Wolio"""

    CAX = "Chiquitano"
    """Chiquitano"""

    HNN = "Hanunoo"
    """Hanunoo"""

    WIY = "Wiyot"
    """Wiyot"""

    ARQ = "Algerian Arabic", True
    """Algerian Arabic"""

    BIN = "Edo"
    """Edo"""

    KHA = "Khasi"
    """Khasi"""

    MYU = "Mundurukú"
    """Mundurukú"""

    XEB = "Eblaite"
    """Eblaite"""

    FUD = "East Futuna"
    """East Futuna"""

    WOS = "Hanga Hundi"
    """Hanga Hundi"""

    XLP = "Lepontic"
    """Lepontic"""

    BGT = "Bughotu"
    """Bughotu"""

    AKV = "Akhvakh"
    """Akhvakh"""

    JQR = "Jaqaru"
    """Jaqaru"""

    VNK = "Lovono"
    """Lovono"""

    FOS = "Siraya"
    """Siraya"""

    FUT = "Futuna-Aniwa"
    """Futuna-Aniwa"""

    SRM = "Saramaccan"
    """Saramaccan"""

    KAP = "Bezhta"
    """Bezhta"""

    PQM = "Malecite-Passamaquoddy"
    """Malecite-Passamaquoddy"""

    ABY = "Aneme Wake"
    """Aneme Wake"""

    BNS = "Bundeli"
    """Bundeli"""

    KVH = "Komodo"
    """Komodo"""

    YUY = "East Yugur"
    """East Yugur"""

    RWO = "Rawa"
    """Rawa"""

    NFR = "Nafaanra"
    """Nafaanra"""

    CZK = "Knaanic", True
    """Knaanic"""

    AWK = "Awabakal"
    """Awabakal"""

    MMN = "Mamanwa"
    """Mamanwa"""

    TGT = "Central Tagbanwa"
    """Central Tagbanwa"""

    ACU = "Achuar"
    """Achuar"""

    SHH = "Shoshone"
    """Shoshone"""

    TZH = "Tzeltal"
    """Tzeltal"""

    TOO = "Xicotepec de Juárez Totonac"
    """Xicotepec de Juárez Totonac"""

    KDJ = "Karamojong"
    """Karamojong"""

    HUS = "Wastek"
    """Wastek"""

    SWG = "Swabian"
    """Swabian"""

    PMT = "Tuamotuan"
    """Tuamotuan"""

    SMP = "Samaritan Hebrew", True
    """Samaritan Hebrew"""

    XNG = "Middle Mongolian"
    """Middle Mongolian"""

    AFZ = "Obokuitai"
    """Obokuitai"""

    XTZ = "Tasmanian"
    """Tasmanian"""

    BGZ = "Banggai"
    """Banggai"""

    KJJ = "Khinalug"
    """Khinalug"""

    PRE = "Principense"
    """Principense"""

    SOG = "Sogdian", True
    """Sogdian"""

    WOE = "Woleaian"
    """Woleaian"""

    AAS = "Aasax"
    """Aasax"""

    MDR = "Mandar"
    """Mandar"""

    OSA = "Osage"
    """Osage"""

    PSE = "Central Malay"
    """Central Malay"""

    DIF = "Dieri"
    """Dieri"""

    EMS = "Alutiiq"
    """Alutiiq"""

    BYR = "Baruya"
    """Baruya"""

    ZHX_SHT = "Shaozhou Tuhua"
    """Shaozhou Tuhua"""

    AMC = "Amahuaca"
    """Amahuaca"""

    LOZ = "Lozi"
    """Lozi"""

    NKP = "Niuatoputapu"
    """Niuatoputapu"""

    ATJ = "Atikamekw"
    """Atikamekw"""

    UGE = "Ughele"
    """Ughele"""

    SJO = "Xibe"
    """Xibe"""

    IAN = "Iatmul"
    """Iatmul"""

    SAC = "Fox"
    """Fox"""

    APU = "Apurinã"
    """Apurinã"""

    KYH = "Karok"
    """Karok"""

    BSH = "Kamkata-viri"
    """Kamkata-viri"""

    KZI = "Kelabit"
    """Kelabit"""

    KTN = "Karitiâna"
    """Karitiâna"""

    MBB = "Western Bukidnon Manobo"
    """Western Bukidnon Manobo"""

    ROL = "Romblomanon"
    """Romblomanon"""

    ANM = "Anal"
    """Anal"""

    DHG = "Dhangu"
    """Dhangu"""

    ZOC = "Copainalá Zoque"
    """Copainalá Zoque"""

    KZJ = "Coastal Kadazan"
    """Coastal Kadazan"""

    ANK = "Goemai"
    """Goemai"""

    KAY = "Kamayurá"
    """Kamayurá"""

    GEL = "Fakkanci"
    """Fakkanci"""

    MLU = "To'abaita"
    """To'abaita"""

    DMW = "Mudburra"
    """Mudburra"""

    CKU = "Koasati"
    """Koasati"""

    AGG = "Angor"
    """Angor"""

    WIN = "Winnebago"
    """Winnebago"""

    ZKU = "Kaurna"
    """Kaurna"""

    BCI = "Baoule"
    """Baoule"""

    SGZ = "Sursurunga"
    """Sursurunga"""

    PUW = "Puluwat"
    """Puluwat"""

    FUY = "Fuyug"
    """Fuyug"""

    NNP = "Wancho"
    """Wancho"""

    BWX = "Bu-Nao Bunu"
    """Bu-Nao Bunu"""

    YII = "Yidiny"
    """Yidiny"""

    URB = "Urubú-Kaapor"
    """Urubú-Kaapor"""

    OJV = "Ontong Java"
    """Ontong Java"""

    TQW = "Tonkawa"
    """Tonkawa"""

    SEE = "Seneca"
    """Seneca"""

    TNL = "Lenakel"
    """Lenakel"""

    BKK = "Brokskat"
    """Brokskat"""

    KJN = "Kunjen"
    """Kunjen"""

    QUN = "Quinault"
    """Quinault"""

    BFY = "Bagheli"
    """Bagheli"""

    APN = "Apinayé"
    """Apinayé"""

    AXG = "Mato Grosso Arára"
    """Mato Grosso Arára"""

    GAY = "Gayo"
    """Gayo"""

    ISD = "Isnag"
    """Isnag"""

    CUK = "Kuna"
    """Kuna"""

    JHI = "Jehai"
    """Jehai"""

    COF = "Tsafiki"
    """Tsafiki"""

    TZJ = "Tz'utujil"
    """Tz'utujil"""

    ROB = "Tae'"
    """Tae'"""

    ANQ = "Jarawa"
    """Jarawa"""

    MOG = "Mongondow"
    """Mongondow"""

    TXE = "Totoli"
    """Totoli"""

    PKP = "Pukapukan"
    """Pukapukan"""

    ROA_LOR = "Lorrain"
    """Lorrain"""

    GTU = "Aghu Tharrnggala"
    """Aghu Tharrnggala"""

    MTO = "Totontepec Mixe"
    """Totontepec Mixe"""

    ACY = "Cypriot Arabic"
    """Cypriot Arabic"""

    KLB = "Kiliwa"
    """Kiliwa"""

    NG = "Ndonga"
    """Ndonga"""

    ABX = "Inabaknon"
    """Inabaknon"""

    SAI_OTO = "Otomaco"
    """Otomaco"""

    DJE = "Zarma"
    """Zarma"""

    MWV = "Mentawai"
    """Mentawai"""

    IBB = "Ibibio"
    """Ibibio"""

    ASN = "Xingú Asuriní"
    """Xingú Asuriní"""

    TKP = "Tikopia"
    """Tikopia"""

    MET = "Mato"
    """Mato"""

    KKH = "Khün"
    """Khün"""

    SRU = "Suruí"
    """Suruí"""

    CDM = "Chepang"
    """Chepang"""

    CBI = "Chachi"
    """Chachi"""

    KXO = "Kanoé"
    """Kanoé"""

    CTG = "Chittagonian"
    """Chittagonian"""

    PDO = "Padoe"
    """Padoe"""

    JUP = "Hupdë"
    """Hupdë"""

    CAM = "Cemuhî"
    """Cemuhî"""

    AQP = "Atakapa"
    """Atakapa"""

    KCN = "Nubi"
    """Nubi"""

    STK = "Arammba"
    """Arammba"""

    ELX = "Elamite"
    """Elamite"""

    TRC = "Copala Triqui"
    """Copala Triqui"""

    KRJ = "Kinaray-a"
    """Kinaray-a"""

    KGK = "Kaiwá"
    """Kaiwá"""

    UUR = "Ura (Vanuatu)"
    """Ura (Vanuatu)"""

    MZP = "Movima"
    """Movima"""

    MQY = "Manggarai"
    """Manggarai"""

    HVN = "Sabu"
    """Sabu"""

    MCR = "Menya"
    """Menya"""

    WSK = "Waskia"
    """Waskia"""

    SKI = "Sika"
    """Sika"""

    GUT = "Maléku Jaíka"
    """Maléku Jaíka"""

    KNM = "Kanamari"
    """Kanamari"""

    DBJ = "Ida'an"
    """Ida'an"""

    VAV = "Varli"
    """Varli"""

    GVL = "Gulay"
    """Gulay"""

    STH = "Shelta"
    """Shelta"""

    DBY = "Dibiyaso"
    """Dibiyaso"""

    BBR = "Girawa"
    """Girawa"""

    BXE = "Ongota"
    """Ongota"""

    MVA = "Manam"
    """Manam"""

    NOE = "Nimadi"
    """Nimadi"""

    COC = "Cocopa"
    """Cocopa"""

    CAC = "Chuj"
    """Chuj"""

    MQN = "Moronene"
    """Moronene"""

    WNW = "Wintu"
    """Wintu"""

    FON = "Fon"
    """Fon"""

    XLS = "Lusitanian"
    """Lusitanian"""

    VMF = "East Franconian"
    """East Franconian"""

    BFT = "Balti", True
    """Balti"""

    MEI = "Midob"
    """Midob"""

    NAL = "Nalik"
    """Nalik"""

    YGR = "Yagaria"
    """Yagaria"""

    KWK = "Kwak'wala"
    """Kwak'wala"""

    NCL = "Michoacán Nahuatl"
    """Michoacán Nahuatl"""

    LMC = "Limilngan"
    """Limilngan"""

    BVR = "Burarra"
    """Burarra"""

    AMK = "Ambai"
    """Ambai"""

    HIX = "Hixkaryana"
    """Hixkaryana"""

    PPO = "Folopa"
    """Folopa"""

    KWA = "Dâw"
    """Dâw"""

    IFK = "Tuwali Ifugao"
    """Tuwali Ifugao"""

    KSK = "Kansa"
    """Kansa"""

    BPZ = "Bilba"
    """Bilba"""

    ANI = "Andi"
    """Andi"""

    TTT = "Tat"
    """Tat"""

    AGM = "Angaataha"
    """Angaataha"""

    KKK = "Kokota"
    """Kokota"""

    HID = "Hidatsa"
    """Hidatsa"""

    SQU = "Squamish"
    """Squamish"""

    AND = "Ansus"
    """Ansus"""

    PMF = "Pamona"
    """Pamona"""

    GCR = "Guianese Creole"
    """Guianese Creole"""

    MWM = "Sar"
    """Sar"""

    ROA_OLE = "Old Leonese"
    """Old Leonese"""

    SCB = "Chut"
    """Chut"""

    HUR = "Halkomelem"
    """Halkomelem"""

    SRR = "Serer"
    """Serer"""

    OMA = "Omaha-Ponca"
    """Omaha-Ponca"""

    XCE = "Celtiberian"
    """Celtiberian"""

    WWW = "Wawa"
    """Wawa"""

    HZ = "Herero"
    """Herero"""

    AEY = "Amele"
    """Amele"""

    ULN = "Unserdeutsch"
    """Unserdeutsch"""

    PLU = "Palikur"
    """Palikur"""

    DBL = "Dyirbal"
    """Dyirbal"""

    CAY = "Cayuga"
    """Cayuga"""

    EGA = "Ega"
    """Ega"""

    UBY = "Ubykh"
    """Ubykh"""

    TDI = "Tomadino"
    """Tomadino"""

    BHP = "Bima"
    """Bima"""

    SGH = "Shughni"
    """Shughni"""

    GVF = "Golin"
    """Golin"""

    BDG = "Bonggi"
    """Bonggi"""

    ALO = "Larike-Wakasihu"
    """Larike-Wakasihu"""

    XBI = "Kombio"
    """Kombio"""

    YER = "Tarok"
    """Tarok"""

    NAI_KRY = "Kings River Yokuts"
    """Kings River Yokuts"""

    MLP = "Bargam"
    """Bargam"""

    ZEN = "Zenaga"
    """Zenaga"""

    TUN = "Tunica"
    """Tunica"""

    TKR = "Tsakhur"
    """Tsakhur"""

    JAO = "Yanyuwa"
    """Yanyuwa"""

    AHT = "Ahtna"
    """Ahtna"""

    KGE = "Komering"
    """Komering"""

    TEW = "Tewa"
    """Tewa"""

    ALK = "Alak"
    """Alak"""

    NTJ = "Ngaanyatjarra"
    """Ngaanyatjarra"""

    DUS = "Dumi"
    """Dumi"""

    MOE = "Montagnais"
    """Montagnais"""

    ABZ = "Abui"
    """Abui"""

    SED = "Sedang"
    """Sedang"""

    LBW = "Tolaki"
    """Tolaki"""

    UMC = "Marrucinian"
    """Marrucinian"""

    LTI = "Leti (Indonesia)"
    """Leti (Indonesia)"""

    AKE = "Akawaio" """Akawaio"""

    def __init__(self, language_name: str, right_to_left: Optional[bool] = False):
        """init method
        @param language_name: Name of the language.
        @type language_name: str

        @param right_to_left: Does the language read right to left? (default False).
        @type right_to_left: Optional[bool]
        """
        self._language_name = language_name
        self._right_to_left = right_to_left
        global count
        self.ordinal: int = count
        count += 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @property
    def language_name(self) -> str:
        """Get the name of the language

        @return: the name
        @rtype: str
        """
        return self._language_name

    @property
    def is_right_to_left(self) -> bool:
        """Does the language read right to left?
        @return: true if the language read right to left, false otherwise
        @rtype: bool
        """
        return self._right_to_left

    @staticmethod
    def from_iso(iso: str) -> "Language":
        """Return the Language with the given ISO code.

        @param iso: The iso code.

        @return: The Language object.
        """
        return Language[iso.upper()]


__all__ = ["Language"]
