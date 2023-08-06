"""This module contains version data."""
import datetime
from datetime import date
from aenum import MultiValueEnum, Enum


class BabelVersion(MultiValueEnum):
    """BabelNet version enumeration."""

    UNKNOWN = "unknown", None
    PRE_2_0 = "< 2.0", date(2013, 1, 15),1
    V2_0 = "2.0", date(2014, 3, 2),2
    V2_0_1 = "2.0.1", date(2014, 3, 10),3
    V2_5 = "2.5", date(2014, 11, 5),4
    V2_5_1 = "2.5.1", date(2014, 11, 15),5
    V3_0 = "3.0", date(2014, 12, 20),6
    V3_1 = "3.1", date(2015, 2, 15),7
    V3_5 = "3.5", date(2015, 9, 10),8
    V3_6 = "3.6", date(2016, 1, 15),9
    V3_7 = "3.7", date(2016, 8, 5),10
    V4_0 = "4.0", date(2018, 1, 10),11
    V5_0 = "5.0", date(2021, 2, 1),12
    V5_1 = "5.1", date(2022, 4, 10),13
    LIVE = "LIVE", date.today(),14

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    @property
    def release_date(self) -> datetime.date:
        """The release date of the version."""
        return self.values[1]

    @property
    def ordinal(self) -> int:
        """The ordinal of the version."""
        return self.values[2]

    @classmethod
    def latest_version(cls) -> "BabelVersion":
        """Return the latest version of BabelNet."""
        return list(cls)[-1]

    @classmethod
    def from_string(cls, version_str: str) -> "BabelVersion":
        """Gets a version of BabelNet from a string

        @param version_str: the string to use
        @type version_str: str

        @return: The version of BabelNet associated to the string passed as input.
        """
        for version in BabelVersion:
            if version.value == version_str:
                return version

        return BabelVersion.UNKNOWN


class WordNetVersion(Enum):
    """A version of WordNet."""

    WN_15: "WordNetVersion" = "1.5"
    WN_16: "WordNetVersion" = "1.6"
    WN_171: "WordNetVersion" = "1.7"
    WN_20: "WordNetVersion" = "2.0"
    WN_21: "WordNetVersion" = "2.1"
    WN_30: "WordNetVersion" = "3.0"
    WN_2020: "WordNetVersion" = "2020"
    OEWN: "WordNetVersion" = "oewn"

    @staticmethod
    def from_string(s: str) -> "WordNetVersion":
        """Gets a version of WordNet from a string

        @param s: the string to use

        @return: The version of WordNet associated to the string passed as input.
        """
        if s.startswith("1.5"):
            return WordNetVersion.WN_15
        if s.startswith("1.6"):
            return WordNetVersion.WN_16
        if s.startswith("1.7"):
            return WordNetVersion.WN_171
        if s == "2.0":
            return WordNetVersion.WN_20
        if s == "2.1":
            return WordNetVersion.WN_21
        if s == "3.0":
            return WordNetVersion.WN_30
        if s == "2020":
            return WordNetVersion.WN_2020
        if s == "oewn":
            return WordNetVersion.OEWN
        raise ValueError("Invalid version: " + s)

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


__all__ = ["BabelVersion", "WordNetVersion"]
