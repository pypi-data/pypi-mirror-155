"""This module contains the POS enum."""
from typing import Optional

from aenum import Enum


class POS(Enum):
    """Universal POS tag set."""

    ADJ: "POS" = 0, "a"
    """Adjective"""
    ADV: "POS" = 1, "r"
    """Adverb"""
    NOUN: "POS" = 2, "n"
    """Noun"""
    VERB: "POS" = 3, "v"
    """Verb"""

    @property
    def ordinal(self):
        """The ordinal property

        @return: the ordinal
        """
        return self.value[0]

    @property
    def tag(self) -> Optional[str]:
        """Get the POS tag character.

        @return: the POS tag character
        """
        return self.value[1]

    # il nome originale e' value_of...
    # TODO: NO TYPING
    @classmethod
    def from_tag(cls, tag: str) -> Optional["POS"]:
        """Construct a POS from a POS tag character.

        @param tag: The POS tag character.

        @return: The corresponding POS.
        """
        return {
            "n": cls.NOUN,
            "a": cls.ADJ,
            "v": cls.VERB,
            "r": cls.ADV,
        }.get(tag, None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @staticmethod
    def compare_by_pos(pos1: "POS", pos2: "POS") -> int:
        """Compare POSes.

        @param pos1:  First POS.
        @param pos2:  Second POS.

        @return: Compare result.
        @rtype: int
        """

        if not isinstance(pos1, POS) or not isinstance(pos2, POS):
            return NotImplemented
        if pos1 is POS.NOUN:
            return 0 if pos2 is POS.NOUN else -1
        if pos1 is POS.VERB:
            return 1 if pos2 is POS.NOUN else 0 if pos2 is POS.VERB else -1
        if pos1 is POS.ADJ:
            return 1 if pos2 in [POS.NOUN, POS.VERB] else 0 if pos2 is POS.ADJ else -1
        if pos1 is POS.ADV:
            return (
                1
                if pos2 in [POS.NOUN, POS.VERB, POS.ADJ]
                else 0
                if pos2 is POS.ADV
                else -1
            )
        return pos1.ordinal - pos2.ordinal


__all__ = ["POS"]
