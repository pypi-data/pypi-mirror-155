"""This module contains the Taggable interface."""

from abc import abstractmethod
from typing import Sequence, Type, Optional

from pybabelnet.data.tag import Tag


class Taggable:
    """A general interface for a taggable."""

    @abstractmethod
    def get_tags(self, tag_type: Optional[Type[Tag]] = None) -> Sequence[Tag]:
        """Returns the collection of the given class of this Taggable.

        @param tag_type: the class for the search..
        @type tag_type: Optional[Type[Tag]]

        @return: the collection of the given class
        @rtype: Sequence[Tag]
        """
        raise NotImplementedError

    @abstractmethod
    def is_tagged_as(self, *tags: Tag) -> bool:
        """Checks if all the given tags are contained in this Taggable.

        @param tags: the tags of interest.
        @type tags: Tag

        @return: true if all the given tags are contained in this Taggable, false otherwise
        @rtype: bool
        """
        raise NotImplementedError
