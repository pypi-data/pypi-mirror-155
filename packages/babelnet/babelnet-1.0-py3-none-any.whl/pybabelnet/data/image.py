"""This module contains the BabelImage class and related data."""

from typing import Set

from pybabelnet.data.source import BabelImageSource
from pybabelnet.data.license import BabelLicense
from pybabelnet.language import Language
from pybabelnet._utils import comparator


class BabelImage:
    """An image in BabelNet.

    @ivar name: The short name / MediaWiki page name for the image, e.g. ::
        'Haile-newyork-cropforfocus.jpg'
    @type name: str
    @ivar languages: The languages of the Wikipedia this image comes from.
    @type languages: Set[Language]
    @ivar url_source: Source of the image URL.
    @type url_source: str
    @ivar thumb_url: The URL thumb to the actual image, e.g. ::
        'http://upload.wikimedia.org/wikipedia/commons/9/94/Haile-newyork-cropforfocus.jpg/120px-Haile-newyork-cropforfocus.jpg'
    @type thumb_url: str
    @ivar url: The URL to the actual image, e.g. ::
        'http://upload.wikimedia.org/wikipedia/commons/9/94/Haile-newyork-cropforfocus.jpg'
    @type url: str
    @ivar license_: Image license.
    @type license_: BabelLicense
    @ivar is_bad: True if bad or censored image.
    @type is_bad: bool
    """

    def __init__(self, title: str, language: str, url: str, thumb_url: str, source: str, license_: str, is_bad: bool):
        """init method
        @param title: Image title.
        @param language: Image language
        @param url: Image URL.
        @param thumb_url: Image thumbnail URL.
        @param source: URL source.
        @param license_: Image license.
        @param is_bad: Is it a bad/censored image?
        """
        self.name = title.strip()
        self.languages = set()
        self.languages.add(Language[language])
        self.url_source = BabelImageSource[source]
        self.url = url
        self.thumb_url = thumb_url
        self.license_ = BabelLicense[license_.replace(" ", "_")]
        self.is_bad: bool = is_bad
        # self._comparator = BabelImageComparator()

    def __str__(self):
        return '<a href="' + self.url + '">' + self.name + "</a>"

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __eq__(self, other):
        if isinstance(other, BabelImage):
            return other.url == self.url and other.url_source is self.url_source
        return False

    # def __lt__(self, other):
    # return self._comparator.compare(self, other) < 0

    def add_language(self, language: Language):
        """Add a new Language.

        @param language: The language to add.
        @type language: Language
        """
        self.languages.add(language)


@comparator
class BabelImageComparator:
    """Comparator for BabelImages which sorts by source."""

    @staticmethod
    def compare(b1: BabelImage, b2: BabelImage) -> int:
        """
        Compare two BabelImages

        @param b1: First BabelImage.
        @param b2: Second BabelImage.

        @return: Compare result.

        @raise NotImplemented: If b1 xor b2 are not instance of BabelExample
        """
        if not isinstance(b1, BabelImage) or not isinstance(b2, BabelImage):
            return NotImplemented

        source1 = b1.url_source
        source2 = b2.url_source

        # Force Wikidata as first image. The second one will be OmegaWiki
        if (
            source1 == BabelImageSource.WIKIDATA
            and source2 != BabelImageSource.WIKIDATA
        ):
            return -1
        if (
            source2 == BabelImageSource.WIKIDATA
            and source1 != BabelImageSource.WIKIDATA
        ):
            return 1
        if (
            source1 == BabelImageSource.WIKIDATA
            and source2 == BabelImageSource.WIKIDATA
        ):
            return 0

        result = source1.ordinal - source2.ordinal
        if result == 0:
            result = len(b2.languages) - len(b1.languages)
        if result == 0:
            lang_en_b1 = Language.EN in b1.languages
            lang_en_b2 = Language.EN in b2.languages
            if lang_en_b1 and not lang_en_b2:
                return -1
            if lang_en_b2 and not lang_en_b1:
                return 1
        return result


__all__ = ["BabelImage", "BabelImageComparator"]
