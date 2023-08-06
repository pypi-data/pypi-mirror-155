"""This module contains the implementation of the online api. It sends queries to the RESTful BabelNet service."""
import json
from typing import Optional, Sequence, Callable, List, Iterable, Set, Dict

from ordered_set import OrderedSet

from babelnet._utils import UnsupportedOnlineError
from babelnet.apis.abstract_api import AbstractAPI
from babelnet.data.relation import BabelSynsetRelation, BabelPointer
from babelnet.iterators.abstract_iter import (
    BabelSynsetIterator,
    BabelOffsetIterator,
    BabelLexiconIterator,
    WordNetSynsetIterator,
)
from babelnet.language import Language
from babelnet.pos import POS
from babelnet import _restful

from babelnet.resources import ResourceID, BabelSynsetID, WikipediaID, WikiquoteID
from babelnet.sense import BabelSense
from babelnet.sense import BabelSenseSource
from babelnet.synset import BabelSynset, _OnlineBabelSynset
from babelnet.versions import BabelVersion

_UNSUPPORTED_ONLINE_MSG = "Unsupported online operation"


class OnlineAPI(AbstractAPI):
    """The online api"""

    def _get_senses(
        self,
        words: Optional[Set[str]] = None,
        resource_ids: Optional[Set[ResourceID]] = None,
        containing: Optional[bool] = False,
        to_langs: Optional[Set[Language]] = None,
        sources: Optional[Set[BabelSenseSource]] = None,
        **kwargs,
    ) -> List[BabelSense]:

        if words:
            synsets = self._get_synsets(
                words=words, to_langs=to_langs, sources=sources, **kwargs
            )
        elif resource_ids:
            synsets = self._get_synsets(
                resource_ids=resource_ids, to_langs=to_langs, sources=sources, **kwargs
            )
        else:
            return []

        senses = []

        for synset in synsets:
            for sense in synset.senses():
                if containing and words and sense.normalized_lemma.lower() not in words:
                    continue
                if to_langs and sense.language not in to_langs:
                    continue
                if sources and sense.source not in sources:
                    continue
                senses.append(sense)

        return senses

    def _get_synsets(
        self,
        words: Optional[Sequence[str]] = None,
        resource_ids: Optional[Sequence[ResourceID]] = None,
        from_langs: Optional[Sequence[Language]] = None,
        to_langs: Optional[Sequence[Language]] = None,
        poses: Sequence[Sequence[POS]] = None,
        normalized: Optional[bool] = True,
        sources: Optional[Sequence[BabelSenseSource]] = None,
        synset_filters: Optional[Sequence[Callable[[BabelSynset], bool]]] = None,
        sense_filters: Optional[Sequence[Callable[[BabelSense], bool]]] = None,
    ) -> List[BabelSynset]:
        max_languages = 3
        synset_filters = OrderedSet() if synset_filters is None else synset_filters
        sense_filters = OrderedSet() if sense_filters is None else sense_filters

        if resource_ids:
            synset_ids = OrderedSet()

            ids = self._get_synset_ids(to_langs, *resource_ids)
            if ids:
                synset_ids.update(ids)
            to_langs = OrderedSet({Language.EN}) if not to_langs else to_langs

            synsets = []

            for synset_id in synset_ids:
                synsets.append(_OnlineBabelSynset(synset_id, to_langs))

            if synset_filters or sense_filters:
                # in questo caso la semantica in JAVA prevede che vengono scartati tutti i synset
                # SE ci sono filtri per synset E esiste almeno un filtro per i senses.
                # Secondo me la semantica corretta deve verificare se ci sono filtri per synsets
                # O per senses come il caso sotto, e controllare entrambi, dunque adottero' questo controllo
                return [
                    synset
                    for synset in synsets
                    if all(p(synset) for p in synset_filters)
                    and synset.retain_senses(*sense_filters)
                ]
            return synsets
        elif words:
            packet = _restful.RESTfulPacket(
                _restful.RESTfulCallType.GET_SYNSETS, _restful.RFKEY
            )
            if from_langs is None:
                raise UnsupportedOnlineError("get_synsets without from_langs attribute")
            packet.search_languages = list(from_langs)
            packet.lemmas = list(words)
            packet.poses = list(poses) if poses else None
            packet.sense_sources = list(sources) if sources else None
            packet.normalizer = normalized
            packet.target_languages = list(to_langs) if to_langs else None

            outserver = _restful.send_request(packet)
            try:
                if not _restful.check_error_code(outserver):

                    def babel_synset_id_decoder(dct):
                        bs = BabelSynsetID(dct["id"])
                        bs.pos = POS[dct["pos"]]
                        return bs

                    synset_ids = json.loads(
                        outserver, object_hook=babel_synset_id_decoder
                    )
                else:
                    raise RuntimeError(_restful.print_error_message(outserver))
            except json.JSONDecodeError:
                raise RuntimeError("Cannot decode JSON from RESTFul response")

            if not to_langs:
                to_langs = from_langs[:max_languages]
            else:
                to_langs = (from_langs | to_langs)[:max_languages]

            synsets = [
                _OnlineBabelSynset(synset_id, to_langs) for synset_id in synset_ids
            ]

            if synset_filters or sense_filters:
                return [
                    synset
                    for synset in synsets
                    if all(p(synset) for p in synset_filters)
                    and synset.retain_senses(*sense_filters)
                ]
            return synsets
        else:
            return []

    def _get_outgoing_edges(
        self, synset_id: BabelSynsetID
    ) -> List[BabelSynsetRelation]:
        """Return the outgoing edges from a given BabelSynsetID

        @param synset_id: The BabelSynsetID whose outgoing edges we want to retrieve.
        @type synset_id: BabelSynsetID

        @return: The list of relation edges.
        @rtype: List[BabelSynsetRelation]
        """
        packet = _restful.RESTfulPacket(
            _restful.RESTfulCallType.GET_SUCCESSORS, _restful.RFKEY
        )
        packet.synset_ids = [synset_id]

        outserver = _restful.send_request(packet)
        if outserver is None:
            return None
        try:
            if not _restful.check_error_code(outserver):

                def babel_synset_relation_decoder(dct: dict):
                    if dct.keys() == {
                        "language",
                        "pointer",
                        "target",
                        "weight",
                        "normalizedWeight",
                    }:
                        return BabelSynsetRelation(
                            Language[dct["language"]], dct["pointer"], dct["target"]
                        )

                    elif dct.keys() == {
                        "fSymbol",
                        "name",
                        "shortName",
                        "relationGroup",
                        "isAutomatic",
                    }:
                        return BabelPointer.from_symbol(dct["fSymbol"])
                    else:
                        return dct

                return json.loads(outserver, object_hook=babel_synset_relation_decoder)
            else:
                raise RuntimeError(_restful.print_error_message(outserver))
        except json.JSONDecodeError:
            raise RuntimeError("Cannot decode JSON from RESTFul response")

    def version(
        self,
    ) -> BabelVersion:
        """Get the version of loaded BabelNet indices.

        @return: The BabelVersion of BabelNet indices.
        @rtype: BabelVersion

        @raises RuntimeError: Raised if cannot decode the response from server or if other error occured.
        """
        packet = _restful.RESTfulPacket(
            _restful.RESTfulCallType.GET_VERSION, _restful.RFKEY
        )
        outserver = _restful.send_request(packet)
        if outserver is None:
            return None
        try:
            if not _restful.check_error_code(outserver):
                return BabelVersion[json.loads(outserver)]
            else:
                raise RuntimeError(_restful.print_error_message(outserver))
        except json.JSONDecodeError:
            raise RuntimeError("Cannot decode JSON from RESTFul response")

    def to_synsets(
        self, resource_id: ResourceID, languages: Optional[Iterable[Language]] = None
    ) -> List[BabelSynset]:
        to_langs = OrderedSet(languages) if languages else OrderedSet({Language.EN})
        return [
            _OnlineBabelSynset(bid, to_langs)
            for bid in self._get_synset_ids(to_langs, resource_id)
        ]

    def _get_synset_ids(
        self, to_langs: Sequence[Language], *resource_ids: ResourceID
    ) -> Optional[List[BabelSynsetID]]:
        """
        Private method that returns a list of synset ids given a list of languages and a ResourceID.

        @param to_langs: the sequence of languages to use
        @param resource_ids: the ResourceID from where the information to construct the BabelSynsetID will be retrieved

        @return: A list of the BabelSynsetIDs that were retreived from the ResourceIDs passed as input.
        """
        packet = _restful.RESTfulPacket(
            _restful.RESTfulCallType.GET_IDSFROMRID, _restful.RFKEY
        )
        packet.resource_ids = list(resource_ids)
        if not to_langs:
            to_langs = [
                resource.language
                for resource in resource_ids
                if isinstance(resource, WikipediaID)
                or isinstance(resource, WikiquoteID)
            ]
            packet.target_languages = to_langs if to_langs else None
        else:
            packet.target_languages = list(to_langs)

        outserver = _restful.send_request(packet)

        if outserver is None:
            return None
        try:
            if not _restful.check_error_code(outserver):

                def babel_synset_id_decoder(dct):
                    bs = BabelSynsetID(dct["id"])
                    bs.pos = POS[dct["pos"]]
                    return bs

                return json.loads(outserver, object_hook=babel_synset_id_decoder)
            else:
                raise RuntimeError(_restful.print_error_message(outserver))
        except json.JSONDecodeError:
            raise RuntimeError("Cannot decode JSON from RESTFul response")

    def iterator(
        self,
    ) -> BabelSynsetIterator:
        raise UnsupportedOnlineError("iterator")

    def offset_iterator(
        self,
    ) -> BabelOffsetIterator:
        raise UnsupportedOnlineError("offset_iterator")

    def lexicon_iterator(
        self,
    ) -> BabelLexiconIterator:
        raise UnsupportedOnlineError("lexicon_iterator")

    def wordnet_iterator(
        self,
    ) -> WordNetSynsetIterator:
        raise UnsupportedOnlineError("wordnet_iterator")

    def images(self, id):
        raise UnsupportedOnlineError("images")

    # def examples(self, id, _target_langs, param):
    #     raise UnsupportedOnlineError("examples")
    #
    # def glosses(self, id, _target_langs, param):
    #     raise UnsupportedOnlineError("glosses")
