"""This module contains the implementation of the local api. It uses the local indexes of babelnet in order to perform queries"""
import traceback
from typing import List, Optional, Iterable, Dict, Callable, Set, Union

from ordered_set import OrderedSet

from babelnet.indices import local_index
from babelnet.apis.abstract_api import AbstractAPI
from babelnet.data.relation import BabelSynsetRelation
from babelnet.iterators.abstract_iter import (
    BabelSynsetIterator,
    BabelOffsetIterator,
    BabelLexiconIterator,
    WordNetSynsetIterator,
)
from babelnet.language import Language
from babelnet.pos import POS
from babelnet.resources import (
    ResourceID,
    BabelSynsetID,
    WordNetSynsetID,
    InvalidSynsetIDError,
    _InternalBabelSynsetID,
)
from babelnet.sense import BabelSense, WordNetSense
from babelnet.synset import BabelSynset
from babelnet.versions import BabelVersion, WordNetVersion


class LocalAPI(AbstractAPI):
    """The local api"""
    _index = local_index.instance()
    """An instance of the BabelNet indexes."""

    def get_senses_containing(
        self, 
        word: str, 
        language: Optional[Language] = None, 
        pos: Optional[POS] = None,
        to_langs: Optional[Set[Language]] = None
    ) -> List[BabelSense]:
        return self.get_senses(
            word,
            from_langs=[language] if language else None,
            containing=True,
            poses=[pos] if pos else None,
            to_langs=to_langs if to_langs else None,
        )

    def get_senses_from(
        self, 
        word: str, 
        language: Optional[Language] = None, 
        pos: Optional[POS] = None,
        to_langs: Optional[Set[Language]] = None
    ) -> List[BabelSense]:
        return self.get_senses(
            word,
            from_langs=[language] if language else None,
            poses=[pos] if pos else None,
            to_langs=to_langs if to_langs else None
        )

    def get_senses(self, *args: Union[str, ResourceID], **kwargs) -> List[BabelSense]:
        self._prepare_kwargs(kwargs)

        if all(isinstance(arg, str) for arg in args):
            words = OrderedSet(args)
            return self._get_senses(words=words, **kwargs)
        if all(isinstance(arg, ResourceID) for arg in args):
            resource_ids = OrderedSet(args)
            return self._get_senses(resource_ids=resource_ids, **kwargs)
        else:
            raise ValueError("The arguments have to be homogeneous.")

    def get_synsets(self, *args: Union[str, ResourceID], **kwargs) -> List[BabelSynset]:
        self._prepare_kwargs(kwargs)

        if all(isinstance(arg, str) for arg in args):
            words = OrderedSet(args)
            result = self._get_synsets(words=words, **kwargs)
            return result
        if all(isinstance(arg, ResourceID) for arg in args):
            resource_ids = OrderedSet(args)
            return self._get_synsets(resource_ids=resource_ids, **kwargs)
        else:
            raise ValueError(f"The arguments have to be homogeneous: {args}")

    def get_synset(self, resource_id: ResourceID, to_langs: Optional[Set[Language]] = None ) -> Optional[BabelSynset]:
        syns = self.get_synsets(resource_id, to_langs=to_langs if to_langs else None)
        return syns[0] if syns else None

    def _prepare_kwargs(self, kwargs):
        if "from_langs" in kwargs and kwargs["from_langs"]:
            kwargs["from_langs"] = OrderedSet(kwargs["from_langs"])
        if "to_langs" in kwargs and kwargs["to_langs"]:
            kwargs["to_langs"] = OrderedSet(kwargs["to_langs"])
        if "poses" in kwargs and kwargs["poses"]:
            kwargs["poses"] = OrderedSet(kwargs["poses"])
        if "sources" in kwargs and kwargs["sources"]:
            kwargs["sources"] = OrderedSet(kwargs["sources"])
        if "sense_filters" in kwargs and kwargs["sense_filters"]:
            kwargs["sense_filters"] = OrderedSet(kwargs["sense_filters"])
        if "synset_filters" in kwargs and kwargs["synset_filters"]:
            kwargs["synset_filters"] = OrderedSet(kwargs["synset_filters"])

    def _get_senses(
        self,
        words: Optional[Set[str]] = None,
        resource_ids: Optional[Set[ResourceID]] = None,
        containing: Optional[bool] = False,
        to_langs: Optional[Set[Language]] = None,
        sources: Optional[Set["BabelSenseSource"]] = None,
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

        # TODO: DEBUG ##
        # from babelnet.synset import BabelSynsetComparator
        # synsets.sort(key=BabelSynsetComparator())
        # print(len(synsets))
        # TODO: END DEBUG ##

        for synset in synsets:
            # TODO: DEBUG ##
            # print(synset, 'len: ', len(synset.senses()), 'id: ', synset.id)
            # if str(synset) == 'dog#n#1':
            #     from babelnet.sense import BabelSenseComparator
            #     _senses = synset.senses()
            #     _senses.sort(key=BabelSenseComparator())
            #     for sense in _senses:
            #         print(sense)
            # TODO: END DEBUG ##

            for sense in synset.senses():
                if containing and words and sense.normalized_lemma.lower() not in words:
                    continue
                if to_langs and sense.language not in to_langs:
                    continue
                if sources and sense.source not in sources:
                    continue
                senses.append(sense)
        return senses

    def version(self) -> BabelVersion:
        return self._index.version()

    def _get_synsets(
        self,
        words: Optional[Set[str]] = None,
        resource_ids: Optional[Set[ResourceID]] = None,
        from_langs: Optional[Set[Language]] = None,
        to_langs: Optional[Set[Language]] = None,
        poses: Set[Set[POS]] = None,
        normalized: Optional[bool] = True,
        sources: Optional[Set["BabelSenseSource"]] = None,
        synset_filters: Optional[Set[Callable[[BabelSynset], bool]]] = None,
        sense_filters: Optional[Set[Callable[[BabelSense], bool]]] = None,
    ) -> List[BabelSynset]:
        synsets = OrderedSet()
        synset_filters = OrderedSet() if synset_filters is None else synset_filters
        sense_filters = OrderedSet() if sense_filters is None else sense_filters
        # se e' una ricerca per lemmi
        if words:
            for word in words:

                # ricerca negli indici la parola richiesta usando le info in input
                license_ids = self._index.license_ids_for_word(
                    word, poses, from_langs, normalized
                )

                # recupera i synset
                if not license_ids:
                    continue

                # ricerca mappatura a seconda della API implementata
                id_set = self._mapping_from_ids(*license_ids)

                if not synset_filters and not sense_filters:
                    synsets.update(self._index.synsets(id_set, to_langs))
                else:
                    results = self._index.synsets(id_set, to_langs)
                    synsets.update(
                        list(
                            synset
                            for synset in results
                            if all(p(synset) for p in synset_filters)
                            and synset.retain_senses(*sense_filters)
                        )
                    )
        elif resource_ids:
            # In JAVA controlla solo per i synset_filters...
            if not synset_filters and not sense_filters:
                for id_ in resource_ids:
                    if not id_ or not id_.id:
                        continue
                    if isinstance(id_, WordNetSynsetID) and id_.version not in {
                        WordNetVersion.WN_30,
                        WordNetVersion.WN_2020,
                        WordNetVersion.OEWN
                    }:
                        try:
                            for new_id in self._index.wordnet_offsets(
                                id_.simple_offset, id_.version
                            ):
                                synsets.update(self.to_synsets(new_id, to_langs))
                        except InvalidSynsetIDError:
                            traceback.print_exc()
                        except Exception as e:
                            print(e)
                    else:
                        synsets.update(self.to_synsets(id_, to_langs))
            else:
                for id_ in resource_ids:
                    if not id_ or not id_.id:
                        continue
                    results = set()
                    # Questo pezzo non c'e' in JAVA... l'ho messo per simmetria con la parte sopra
                    if isinstance(id_, WordNetSynsetID) and id_.version not in {
                        WordNetVersion.WN_30,
                        WordNetVersion.WN_2020,
                        WordNetVersion.OEWN
                    }:
                        try:
                            for new_id in self._index.wordnet_offsets(
                                id_.simple_offset, id_.version
                            ):
                                results.update(self.to_synsets(new_id, to_langs))
                        except InvalidSynsetIDError:
                            traceback.print_exc()
                        except Exception as e:
                            print(e)
                    else:
                        results = self.to_synsets(id_, to_langs)

                    # in questo caso la semantica in JAVA prevede che vengono scartati tutti i synset
                    # SE ci sono filtri per synset E esiste almeno un filtro per i senses.
                    # Secondo me la semantica corretta deve verificare se ci sono filtri per synsets
                    # O per senses come il caso sotto, e controllare entrambi, dunque adottero' questo controllo
                    synsets.update(
                        list(
                            synset
                            for synset in results
                            if all(p(synset) for p in synset_filters)
                            and synset.retain_senses(*sense_filters)
                        )
                    )
        if not sources:
            return list(synsets)
        else:
            # seleziona solo i synset che hanno almeno un senso con una lingua e sorgente richieste
            return [
                synset
                for synset in synsets
                if any(
                    (to_langs is None or s.language in to_langs) and s.source in sources
                    for s in synset.senses()
                )
            ]

    def _mapping_from_ids(
        self,
        *ids: BabelSynsetID,
    ) -> Dict[BabelSynsetID, List["_InternalBabelSynsetID"]]:
        return self._index.mapping_from_babelsynsetids(*ids)

    def _get_outgoing_edges(
        self, synset_id: BabelSynsetID
    ) -> List[BabelSynsetRelation]:
        related = []
        related_edge_strings = self._index.successors(synset_id)
        if related_edge_strings is None:
            return related
        for related_edge_string in related_edge_strings:
            if not related_edge_string:
                continue
            edge = BabelSynsetRelation.from_string(related_edge_string)
            related.append(edge)
        return related

    def to_babelnet_synsets(self, id_, languages):
        id_set = self._mapping_from_ids(id_)

        # recupera il synset
        results = self._index.synsets(id_set, languages)

        # restituisce il synset ma senza dati perche' non si trova nulla in langs
        if not results:
            return (
                [self._index.synset_from_empty_document(id_, id_set[id_])]
                if id_set
                else []
            )
        else:
            return [results[0]]

    def _to_wordnet_synsets(self, id_, languages):
        license_ids = None

        try:
            license_ids = self._index.synsets_from_wordnet_offset(id_)
        except InvalidSynsetIDError:
            traceback.print_exc()

        if not license_ids:
            return []

        # ricerca mappatura
        id_set = self._mapping_from_ids(*license_ids)
        # NOTE: controllare che l'offset corrisponda alla risorsa corretta (WN o WN2020)
        # Esempio:
        # Cerco l'offset 02084071n in lucene e voglio che il risultato venga fuori solo se il prefisso
        # inserito in input sia quello corretto della giusta risorsa, ovvero wn:02084071n e non wn2020:02084071n

        synsets = self._index.synsets(id_set, languages)
        if len(synsets) != 0:
            senses: List[WordNetSense] = synsets[0].senses(source=id_.source)
            for sense in senses:
                if sense.wordnet_offset.lower() == id_.simple_offset.lower():
                    return synsets

        return []

    def to_synsets(
        self, resource_id: ResourceID, languages: Optional[Iterable[Language]] = None
    ) -> List[BabelSynset]:
        languages = None if languages is None else OrderedSet(languages)
        if isinstance(resource_id, BabelSynsetID):
            return self.to_babelnet_synsets(resource_id, languages)
        if isinstance(resource_id, WordNetSynsetID):
            return self._to_wordnet_synsets(resource_id, languages)

        license_ids = None
        try:
            license_ids = self._index.licence_ids_from_resource_id(resource_id)
        except InvalidSynsetIDError:
            traceback.print_exc()
        if not license_ids:
            return []

        # ricerca mappatura
        id_set = self._mapping_from_ids(*license_ids)
        return [
            synset
            for synset in self._index.synsets_from_resource_id(
                resource_id, id_set, languages
            )
        ]

    def iterator(self) -> BabelSynsetIterator:
        return self._index.synset_iterator()

    def wordnet_iterator(self) -> WordNetSynsetIterator:
        return self._index.wordnet_iterator()

    def offset_iterator(self) -> BabelOffsetIterator:
        return self._index.offset_iterator()

    def lexicon_iterator(self) -> BabelLexiconIterator:
        return self._index.lexicon_iterator()

    def images(self, id: BabelSynsetID):
        return self._index.images(id)

    def examples(
        self,
        synset_id: BabelSynsetID,
        filter_langs: Set[Language],
        *ids: _InternalBabelSynsetID,
    ):
        return self._index.examples(synset_id, filter_langs, *ids)

    def glosses(
        self,
        synset_id: BabelSynsetID,
        filter_langs: Set[Language],
        *ids: _InternalBabelSynsetID,
    ):
        return self._index.glosses(synset_id, filter_langs, *ids)
