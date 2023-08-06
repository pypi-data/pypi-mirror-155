"""
This module sets the api type (RPC/ONLINE/OFFLINE). It also contains the list of functions implemented by the BabelNet API.

@var get_synsets: Get synsets by words or by ResourceIDs, satisfying the optional constraints.
@type get_synsets: L{AbstractAPI.get_synsets}

@var get_synset: Return the synset identified by the ResourceID in input.

        Some examples that can be used follow::
            import babelnet as bn

            # Retrieving BabelSynset from a Wikipedia page title:
            synset = bn.get_synset(WikipediaID('BabelNet', Language.EN, POS.NOUN))

            # Retrieving BabelSynset from a WordNet id:
            synset = bn.get_synset(WordNetSynsetID('wn:03544360n'))

            # Retrieving BabelSynset from a Wikidata page id:
            synset = bn.get_synset(WikidataID('Q4837690'))

            # Retrieving BabelSynset from a OmegaWiki page id:
            synset = bn.get_synset(OmegaWikiID('1499705'))
@type get_synset: L{AbstractAPI.get_synset}

@var get_senses: Get the senses of synsets searched by words or by ResourceIDs,
        satisfying the optional constraints.
@type get_senses: L{AbstractAPI.get_senses}

@var get_senses_containing: Get the senses of synsets containing the word with the given constraints.
@type get_senses_containing: L{AbstractAPI.get_senses_containing}

@var get_senses_from: Get the senses of synsets from the word with the given constraints.
@type get_senses_from: L{AbstractAPI.get_senses_from}

@var to_synsets: Convert from ResourceID to the corresponding BabelSynset.
@type to_synsets: L{AbstractAPI.to_synsets}

@var wordnet_iterator: Create a new instance of a WordNet iterator.
@type wordnet_iterator: L{AbstractAPI.wordnet_iterator}

@var lexicon_iterator: Create a new instance of a lexicon iterator.
@type lexicon_iterator: L{AbstractAPI.lexicon_iterator}

@var offset_iterator: Create a new instance of an offset iterator.
@type offset_iterator: L{AbstractAPI.offset_iterator}

@var iterator: Create a new instance of BabelSynset iterator.
@type iterator: L{AbstractAPI.iterator}

@var version: Get the version of loaded BabelNet indices.
@type version: L{AbstractAPI.version}
"""

import logging
import os
import time

from babelnet.about import header, BabelAPIType
from babelnet.conf import _config

_log = logging.getLogger(__name__)
"""logger"""
_api_type: BabelAPIType = (
    BabelAPIType.RPC
    if _config.RPC_URL
    else (
        BabelAPIType.OFFLINE
        if os.path.exists(_config.BASE_DIR)
        else BabelAPIType.ONLINE
    )
)
"""the type of the api."""
_log.info(header(_api_type))

_api = None
"""the api instance"""

def identity(func):
    """The identity function"""
    return func


wrapper = identity

if _api_type == BabelAPIType.OFFLINE:
    import zerorpc
    from babelnet.apis.local_api import LocalAPI

    _api = LocalAPI()

    def wrapper(func):
        """
        Wrapper for the api. Used when the api is offline.
        """
        def wrap(*args, **kwargs):
            # print(func, args, kwargs)
            if len(args) == 1 and isinstance(args[0], dict):
                arguments = args[0]
                args = arguments.pop("args")
                kwargs = arguments.pop("kwargs")
            ts = time.time()
            result = func(*args, **kwargs)
            # print(
            #     f"func: {func.__name__} | args: {args} | took: {time.time() - ts} sec"
            # )
            return result


        decorator = zerorpc.stream if func.__name__.endswith("iterator") else identity

        return decorator(wrap)


if _api_type == BabelAPIType.RPC:
    from babelnet.apis.rpc_api import RPCApi

    _api = RPCApi()

if _api_type == BabelAPIType.ONLINE:
    from babelnet.apis.online_api import OnlineAPI

    _api = OnlineAPI()

_version = _api.version()
"""The version of the api"""
_config.set_actual_version(_version)


def version():
    return _version


__all__ = [
    "get_synsets",
    "get_synset",
    "get_senses",
    "get_senses_containing",
    "get_senses_from",
    "get_outgoing_edges",
    "to_synsets",
    "images",
    "glosses",
    "examples",
    "version",
    "iterator",
    "offset_iterator",
    "lexicon_iterator",
    "wordnet_iterator",
]

_all_functions = __all__

get_synsets = _api.get_synsets
get_synset = _api.get_synset
get_senses = _api.get_senses
get_senses_containing = _api.get_senses_containing
get_senses_from = _api.get_senses_from
get_outgoing_edges = _api.get_outgoing_edges
to_synsets = _api.to_synsets
images = _api.images
glosses = _api.glosses
examples = _api.examples
wordnet_iterator = _api.wordnet_iterator
lexicon_iterator = _api.lexicon_iterator
offset_iterator = _api.offset_iterator
iterator = _api.iterator

for func_name in _all_functions:
    globals()[func_name] = wrapper(globals()[func_name])

