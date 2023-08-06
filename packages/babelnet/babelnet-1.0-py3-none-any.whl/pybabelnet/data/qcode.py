"""This module contains the QcodeID class."""

from dataclasses import dataclass

@dataclass(frozen=True, unsafe_hash=True)
class QcodeID(object):
    """
    Constructs a qcode identifier with the specified ID.
    """

    _id: str

    @property
    def id(self) -> str:
        """
        Get the ID.
        @return: the ID.
        @rtype: str
        """
        return self._id

    def copy(self):
        """
        Get a copy of this object
        @return: the copy.
        @rtype: QcodeID
        """
        return QcodeID(**self.__dict__)
