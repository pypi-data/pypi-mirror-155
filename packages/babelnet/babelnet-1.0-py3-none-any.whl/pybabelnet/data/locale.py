"""This module contains the Locale enum."""

from aenum import Enum, auto

from pybabelnet.data.tag import Tag


class Locale(Tag, Enum):
    """Enumeration describing lexical and orthographic variations

    @ivar super_tag: the tag of the super
    @type super_tag: str

    @ivar index: Index
    @type index: int
    """

    AFRICA = "AFRICA", auto()

    ALASKA = "US", auto()

    AMERICA = "AMERICA", auto()

    AUSTRALIA = "AUSTRALIA", auto()

    CANADA = "AMERICA", auto()

    EAST_AFRICA = "AFRICA", auto()

    ENGLAND = "UK", auto()

    HAWAII = "US", auto()

    HONG_KONG = "HONG_KONG", auto()

    INDIA = "INDIA", auto()

    IRELAND = "IRELAND", auto()

    MIDLAND_US = "US", auto()

    MIDWESTERN_US = "US", auto()

    NEW_ZEALAND = "NEW_ZEALAND", auto()

    NORTHERN_ENGLAND = "UK", auto()

    NORTHERN_IRELAND = "UK", auto()

    PHILIPPINES = "PHILIPPINES", auto()

    SCOTLAND = "UK", auto()

    SINGAPORE = "SINGAPORE", auto()

    SOUTH_AFRICA = "AFRICA", auto()

    SOUTHERN_ENGLAND = "UK", auto()

    UK = "UK", auto()

    US = "US", auto()

    WALES = "UK", auto()

    WESTERN_US = "US", auto()

    BRAZIL = "AMERICA", auto()

    PORTUGAL = "PORTUGAL", auto()

    def __init__(self, super_tag: str, index: int):
        """init method
        @param super_tag: the tag of the super
        @param index: the index
        """
        self.super_tag: str = super_tag
        self.index: int = index

    @property
    def coarse_grained(self) -> "Locale":
        """return the locale of the super

        @return: Locale[self.super_tag]
        @rtype: "Locale"
        """
        return Locale[self.super_tag]

    @property
    def value(self) -> "Locale":
        return self
