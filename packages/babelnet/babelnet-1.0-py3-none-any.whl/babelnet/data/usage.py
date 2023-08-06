"""This module contains the Usage enum."""

from aenum import Enum, auto


class Usage(Enum):
    """Enumeration describing usage information."""

    KEY_CONCEPT = auto()
    COLOR = auto()
    RARE = auto()
    ARCHAIC = auto()
    OFFENSIVE = auto()
    CULTURAL = auto()
    DEROGATORY = auto()
    SEXUAL = auto()
    VIOLENCE = auto()
    VULGAR = auto()
    NETSPEAK = auto()
    PREFIX = auto()

    # Duck-typing from Tag
    @property
    def value(self) -> "Usage":
        """
        Get the Usage value
        @return: self
        @rtype: Usage
        """
        return self
