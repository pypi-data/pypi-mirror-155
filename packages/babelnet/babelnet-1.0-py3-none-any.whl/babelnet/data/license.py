"""This module contains the BabelLicense enum."""
from typing import Optional

from aenum import Enum


# TODO: update documentation
class BabelLicense(Enum):
    """License information for a BabelNet item."""

    UNRESTRICTED: "BabelLicense" = "UNR", ""
    """All the permissive licenses without specific restrictions"""

    CC_BY_SA_30: "BabelLicense" = "CBS30", "https://creativecommons.org/licenses/by-sa/3.0/"
    """Creative Commons Attribution-ShareAlike 3.0 License https://creativecommons.org/licenses/by-sa/3.0/"""

    CC_BY_SA_40: "BabelLicense" = "CBS40", "https://creativecommons.org/licenses/by-sa/4.0/"
    """Creative Commons Attribution-ShareAlike 4.0 International https://creativecommons.org/licenses/by-sa/4.0/"""

    CC_BY_30: "BabelLicense" = "CB30", "https://creativecommons.org/licenses/by/3.0/"
    """Creative Commons Attribution 3.0 License https://creativecommons.org/licenses/by/3.0/"""

    CECILL_C: "BabelLicense" = "CEC", "http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.txt"
    """CeCILL-C free software license agreement http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.txt"""

    APACHE_20: "BabelLicense" = "APCH20", "http://www.apache.org/licenses/LICENSE-2.0"
    """Apache 2.0 License http://www.apache.org/licenses/LICENSE-2.0"""

    CC_BY_NC_SA_30: "BabelLicense" = "CBNS30", "http://creativecommons.org/licenses/by-nc-sa/3.0/"
    """Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License http://creativecommons.org/licenses/by-nc-sa/3.0/"""

    MLP: "BabelLicense" = "MLP", "http://www.microsoft.com/Language/en-US/LicenseAgreement.aspx"
    """Microsoft language portal materials license http://www.microsoft.com/Language/en-US/LicenseAgreement.aspx"""

    OTHER: "BabelLicense" = "OTHER", ""
    """Items without specific licenses."""

    WORDNET: "BabelLicense" = "WORDNET", "https://wordnet.princeton.edu/license-and-commercial-use"
    """WordNet license https://wordnet.princeton.edu/license-and-commercial-use"""

    MIT: "BabelLicense" = "MIT", "https://opensource.org/licenses/MIT"
    """MIT license https://opensource.org/licenses/MIT"""

    ODC_BY_10: "BabelLicense" = "ODCBY10", "https://opendatacommons.org/licenses/by/1-0/"
    """ODC-BY 1.0 license https://opendatacommons.org/licenses/by/1-0/"""

    GFDL_12: "BabelLicense" = "GFDL12", "https://www.gnu.org/licenses/old-licenses/fdl-1.2.html"
    """GFDL 1.2 license https://www.gnu.org/licenses/old-licenses/fdl-1.2.html"""

    BABELNET_NC: "BabelLicense" = "BNNC", "https://babelnet.org/license"
    """BabelNet NonCommercial license https://babelnet.org/license"""

    CC_BY_NC_SA_40: "BabelLicense" = "CBNS40", "http://creativecommons.org/licenses/by-nc-sa/4.0/"
    """Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Unported License http://creativecommons.org/licenses/by-nc-sa/4.0/"""

    CC_BY_40: "BabelLicense" = "CB40", "http://creativecommons.org/licenses/by/4.0/"
    """Creative Commons Attribution 4.0 License http://creativecommons.org/licenses/by/4.0/"""

    COMMERCIAL: "BabelLicense" = "CM", ""
    """Babelscape commercial license"""

    CC0_10: "BabelLicense" = "CC010", "https://creativecommons.org/publicdomain/zero/1.0/deed.en"
    """CC0 1.0 Universal"""

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @property
    def short_name(self) -> str:
        """
        Get the short name
        @return: the short name
        """
        return self.value[0]

    @property
    def uri(self) -> Optional[str]:
        """ Returns a URI associated with B{this} license
        @return: a URI associated with B{this} license
        """
        return self.value[1]

    # TODO: no typing
    @classmethod
    def long_name(cls, string_name: str) -> Optional["BabelLicense"]:
        """Return the BabelLicence for a given string.

        @param string_name: The license string.

        @return: The corresponding license.
        """
        if string_name.startswith("bn"):
            return cls.UNRESTRICTED
        if string_name.startswith("AAA"):
            return None
        if string_name.startswith("AAB"):
            return None

        for bl in cls:
            if bl.short_name == string_name:
                return bl

        # short_name is not a short name of BabelLicense
        return None


__all__ = ["BabelLicense"]
