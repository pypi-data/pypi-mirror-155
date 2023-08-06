"""This module contains the abstract BabelIterator"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterator, Tuple

from babelnet.language import Language
from babelnet.pos import POS
from babelnet.synset import BabelSynset
from babelnet.resources import BabelSynsetID


T = TypeVar("T")
"""Generic type"""


class BabelIterator(ABC, Generic[T]):
    """Abstract iterator over BabelNet's content"""
    @abstractmethod
    def __next__(self) -> T:
        raise NotImplemented

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        raise NotImplemented

    @abstractmethod
    def has_next(self) -> bool:
        """function that returns true if the iterator has still another element to continue the iteration with.

        @return: true if there is another element, false otherwise
        @rtype: bool
        """
        raise NotImplemented


BabelSynsetIterator = BabelIterator[BabelSynset]
"""Variable containing a BabelIterator that uses BabelSynset. The implementation is L{BabelSynsetIteratorImpl}"""
BabelLexiconIterator = BabelIterator[Tuple[str, POS, Language]]
"""Variable containing a BabelIterator that uses Tuple[str, POS, Language]. The implementation is L{BabelLexiconIteratorImpl}"""
BabelOffsetIterator = BabelIterator[BabelSynsetID]
"""Variable containing a BabelIterator that uses BabelSynsetID. The implementation is L{BabelOffsetIteratorImpl}"""
WordNetSynsetIterator = BabelIterator[BabelSynset]
"""Variable containing a BabelIterator that uses BabelSynset. The implementation is L{WordNetSynsetIteratorImpl}"""


__all__ = [
    "BabelIterator",
    "BabelSynsetIterator",
    "BabelLexiconIterator",
    "BabelOffsetIterator",
    "WordNetSynsetIterator",
]
