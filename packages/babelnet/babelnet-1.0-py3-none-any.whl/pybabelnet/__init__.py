"""PyBabelnet API"""
from pybabelnet import zerorpc_patch

zerorpc_patch.monkey_patch()

from pybabelnet.conf import _config
from pybabelnet.api import (
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
from pybabelnet.synset import BabelSynsetComparator, BabelSynset
from pybabelnet.resources import BabelSynsetID
from pybabelnet.language import Language
from pybabelnet.pos import POS
from pybabelnet.data.source import BabelSenseSource

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
