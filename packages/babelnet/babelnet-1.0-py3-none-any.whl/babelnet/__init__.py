"""BabelNet Python API"""
from babelnet import zerorpc_patch

zerorpc_patch.monkey_patch()

from babelnet.conf import _config
from babelnet.api import (
    get_synsets,
    get_synset,
    get_senses,
    get_senses_containing,
    get_senses_from,
    to_synsets,
    iterator,
    lexicon_iterator,
    offset_iterator,
    version,
    wordnet_iterator,
)
from babelnet.synset import BabelSynsetComparator, BabelSynset
from babelnet.resources import BabelSynsetID
from babelnet.language import Language
from babelnet.pos import POS
from babelnet.data.source import BabelSenseSource

__all__ = [
    "about",
    "_config",
    "get_synset",
    "get_synsets",
    "get_synset",
    "get_senses",
    "get_senses_from",
    "get_senses_containing",
    "to_synsets",
    "iterator",
    "lexicon_iterator",
    "offset_iterator",
    "version",
    "BabelSynset",
    "BabelSynsetComparator",
    "BabelSynsetID",
    "Language",
    "POS",
    "wordnet_iterator",
    # Data
    "BabelSenseSource",
]
