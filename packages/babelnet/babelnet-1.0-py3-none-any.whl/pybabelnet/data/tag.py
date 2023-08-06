"""This module contains the Tag interface and the related StringTag extension."""

from abc import abstractmethod

from dataclasses import dataclass


class Tag:
    """ A general interface for a tag."""

    @property
    @abstractmethod
    def value(self) -> object:
        """Returns the tag value."""
        pass


@dataclass(frozen=True, unsafe_hash=True)
class StringTag(Tag):
    """
    A string tag associated to a BabelSynset.
    """

    tag: str
    """The string tag"""

    @property
    def value(self) -> str:
        return self.tag
