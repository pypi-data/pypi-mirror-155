"""This module contains the FrameID class and the related VerbAtlas implementation."""

from abc import abstractmethod

from dataclasses import dataclass


class FrameID(object):
    """A general class for a frame identifier."""

    @property
    @abstractmethod
    def id(self):
        """Gets the ID of this FrameID

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError

    def copy(self):
        """Gets a copy of this FrameID

        @raise NotImplementedError: if not implemented
        """
        raise NotImplementedError


@dataclass(frozen=True, unsafe_hash=True)
class VerbAtlasFrameID(FrameID):
    """
    Constructs a frame identifier with the specified ID.
    """

    _id: str
    """the id"""

    @property
    def id(self) -> str:
        """Gets the ID of this FrameID"""
        return self._id

    def copy(self):
        """
        Get a copy of this object

        @return: a copy of this objct
        @rtype: VerbAtlasFrameID
        """
        return VerbAtlasFrameID(**self.__dict__)
