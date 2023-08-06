"""Information about PyBabelNet."""
from typing import Optional

from aenum import Enum

TITLE = "PyBabelNet"  #:

VERSION = "1.0.dev5"  #:

AUTHOR = (
    "Babelscape"  #:
)

AUTHOR_EMAIL = "info@babelscape.com"  #:

DOCUMENTATION_URL = "http://babelnet.org/"  #:

DESCRIPTION = "Python APIs for BabelNet"  #:


class BabelAPIType(Enum):
    """Type of BabelNet API."""

    OFFLINE = "offline"
    """Fully offline, with all indices on the machine."""

    ONLINE = "online RESTful"
    """Fully online, with no indices on the machine."""

    RPC = "Remote Procedure Call"
    """Fully offline, with all indices on the machine and index APIs accessible via RPC"""

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    @property
    def type(self) -> str:
        """
        Return the corresponding type of API.
        """
        return self.value


def header(api_type: Optional[BabelAPIType] = None) -> str:
    """Return an initialization string for the BabelNet API.

    @param api_type: The API type (default None).
    @type api_type: Optional[BabelAPIType]

    @return: The initialization string.
    """
    type_str = "" if api_type is None else str(api_type)
    return TITLE + " " + type_str + " API v" + VERSION


__all__ = [
    "TITLE",
    "VERSION",
    "AUTHOR",
    "AUTHOR_EMAIL",
    "DOCUMENTATION_URL",
    "DESCRIPTION",
    "BabelAPIType",
    "header",
]
