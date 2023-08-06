"""This module contains all the iterators over BabelNet."""

from abc import ABC

import lucene
from org.apache.lucene.index import MultiFields

from pybabelnet._impl import BabelNetIndexField
from pybabelnet.iterators.abstract_iter import (
    BabelIterator,
    BabelSynsetIterator,
    BabelLexiconIterator,
    WordNetSynsetIterator,
    BabelOffsetIterator,
)
from pybabelnet.language import Language
from pybabelnet.pos import POS
from pybabelnet.resources import BabelSynsetID, InvalidSynsetIDError


class BabelIteratorImpl(BabelIterator, ABC):
    """Abstract iterator over BabelNet's content.

    @ivar _reader: the reader
    @ivar _current_index: indicates the current index of the iteration
    @ivar _live_docs: the LiveDocs of lucene
    """

    def __init__(self, searcher):
        """init method
        @param searcher: The searcher to use
        """
        super().__init__()
        self._reader = searcher.getIndexReader()
        self._current_index = 0
        self._live_docs = MultiFields.getLiveDocs(self._reader)
        while (
            self._current_index < self._reader.maxDoc()
            and self._live_docs is not None
            and not self._live_docs.get(self._current_index)
        ):
            self._current_index += 1

    def __iter__(self):
        return self

    def has_next(self):
        return self._current_index < self._reader.maxDoc()


class BabelSynsetIteratorImpl(BabelIteratorImpl, BabelSynsetIterator):
    """Iterator over BabelSynset(s)"""

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        if self._live_docs is not None and not self._live_docs.get(self._current_index):
            raise StopIteration
        try:
            doc = self._reader.document(self._current_index)
            self._current_index += 1
            # if it'is the doc with version, skip this Lucene document
            version = doc.get(BabelNetIndexField.VERSION.name)
            if version is not None:
                return self.__next__()
            id_ = doc.get(BabelNetIndexField.ID.name)
            try:
                return BabelSynsetID(id_).to_synset()
            except InvalidSynsetIDError:
                raise RuntimeError(
                    "InvalidBabelSynsetIDError: " + str(self._current_index)
                )
        except lucene.JavaError:
            raise StopIteration


class BabelLexiconIteratorImpl(BabelIteratorImpl, BabelLexiconIterator):
    """Iterator over BabelNet's lexicon"""

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        if self._live_docs is not None and not self._live_docs.get(self._current_index):
            raise StopIteration
        try:
            if self._current_index == self._reader.maxDoc():
                return StopIteration
            doc = self._reader.document(self._current_index)
            self._current_index += 1
            # if it'is the doc with version, skip this Lucene document
            version = doc.get(BabelNetIndexField.VERSION.name)
            if version is not None:
                return self.__next__()
            pos = POS.from_tag(doc.get(BabelNetIndexField.POS.name))
            lemma = doc.get(BabelNetIndexField.LEMMA.name)
            language = Language[doc.get(BabelNetIndexField.LEMMA_LANGUAGE.name)]
            return lemma, pos, language
        except lucene.JavaError:
            raise StopIteration

    def has_next(self):
        if self._reader.maxDoc() == 1:
            return False
        return super().has_next()


class BabelOffsetIteratorImpl(BabelIteratorImpl, BabelOffsetIterator):
    """Iterator over BabelNet's synset offsets"""

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        if self._live_docs is not None and not self._live_docs.get(self._current_index):
            raise StopIteration
        try:
            doc = self._reader.document(self._current_index)
            self._current_index += 1
            # if it'is the doc with version, skip this Lucene document
            version = doc.get(BabelNetIndexField.VERSION.name)
            if version is not None:
                return self.__next__()
            return doc.get(BabelNetIndexField.ID.name)

        except lucene.JavaError:
            raise StopIteration


class WordNetSynsetIteratorImpl(BabelIteratorImpl, WordNetSynsetIterator):
    """Iterator over WordNet BabelSynset(s)."""

    _MAX_SYNSET_VALUE: int = 117659

    _NOUN_MAX_VALUE: int = 82115
    _VERB_MAX_VALUE: int = 95882
    _ADJ_MAX_VALUE: int = 114038

    _NOUN_CHAR: str = "n"
    _VERB_CHAR: str = "v"
    _ADJ_CHAR: str = "a"
    _ADV_CHAR: str = "r"

    _PREFIX: str = "bn:"

    def __init__(self, searcher):
        """init method
        @param searcher: the searcher
        """
        super().__init__(searcher)
        self._current_index = 1

    def __next__(self):
        # Skip invalid synsets
        if not self.has_next():
            raise StopIteration

        char: str = WordNetSynsetIterator.get_char(self._current_index)
        synset_id: str = (
            f"{WordNetSynsetIterator._PREFIX}{str(self._current_index).zfill(8)}{char}"
        )
        synset = BabelSynsetID(synset_id).to_synset()

        self._current_index += 1

        return next(self) if synset is None else synset

    def has_next(self):
        return self._current_index <= WordNetSynsetIterator._MAX_SYNSET_VALUE

    @staticmethod
    def get_char(index: int) -> str:
        """Get the character at the given index.

        @param index: the index of the char
        @type index: int

        @return: the character.
        @rtype: str
        """
        assert index <= WordNetSynsetIterator._MAX_SYNSET_VALUE
        # NOUN -> VERB -> ADJ -> ADV
        if index <= WordNetSynsetIterator._NOUN_MAX_VALUE:
            return WordNetSynsetIterator._NOUN_CHAR

        if index <= WordNetSynsetIterator._VERB_MAX_VALUE:
            return WordNetSynsetIterator._VERB_CHAR

        if index <= WordNetSynsetIterator._ADJ_MAX_VALUE:
            return WordNetSynsetIterator._ADJ_CHAR

        return WordNetSynsetIterator._ADV_CHAR


__all__ = [
    "BabelIteratorImpl",
    "BabelSynsetIteratorImpl",
    "BabelLexiconIteratorImpl",
    "BabelOffsetIteratorImpl",
    "WordNetSynsetIteratorImpl",
]
