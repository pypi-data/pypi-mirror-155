"""This module contains the Alphabet enum."""

from aenum import Enum, auto

from babelnet.data.tag import Tag


class Alphabet(Tag, Enum):
    """Enumeration describing alphabet information"""

    TRADITIONAL_CHINESE = auto()
    """Traditional chinese alphabet"""

    SIMPLIFIED_CHINESE = auto()
    """Simplified chinese alphabet"""

    @property
    def value(self) -> "Alphabet":
        return self
