"""This module contains the BabelAudio, BabelSensePhonetic classes and related data."""
import re
import traceback
from typing import Set, Tuple
import hashlib
import urllib.parse
import requests

from babelnet.language import Language


class BabelAudio:
    """An audio item in BabelNet.

    @ivar lemma: Lemma pronounced.
    @type lemma: str
    @ivar language: Lemma language.
    @type language: Language
    @ivar filename : Audio filename associated.
    @type filename: str
    @ivar _url: the url
    @type _url: str
    @ivar _url_validated: the validated url
    @type _url_validated: str
    """

    _URL_PREFIX = "//upload.wikimedia.org/wikipedia/commons/"
    """The default audio URL (str)."""

    _REG = "//upload.wikimedia.org/wikipedia/commons/.*?"
    """Regular expression (str)."""

    _URL_COMMOS = "http://commons.wikimedia.org/wiki/"
    """Wikimedia Commons URL (str)."""

    _HTTP_PREFIX = "http:"
    """HTTP prefix (str)."""

    def __init__(self, lemma: str, language: Language, filename: str):
        """init method
        @param lemma: Lemma pronounced.
        @param language: Lemma language.
        @param filename : Audio filename associated.
        """
        self.lemma = lemma
        self.language = language

        # NOTE: BabelNet live: getting only the name of the file
        self.filename = filename.split("/")[-1]
        self._url = None
        self._url_validated = None

    def __eq__(self, other):
        if isinstance(other, BabelAudio):
            return (
                self.lemma == other.lemma
                and self.language is other.language
                and self.filename == other.filename
            )
        return False

    def __hash__(self):
        return hash((self.lemma, self.language, self.filename))

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __str__(self):
        seq = (str(self.language), self.lemma, self.filename)
        return ":".join(seq)

    @property
    def url(self) -> str:
        """The full URL of this BabelAudio.

        @return: the url
        """
        if self._url is None:
            self._url = self._create_url()
        return self._url

    @property
    def validated_url(self) -> str:
        """A valid URL for the audio file.

        @return: A valid URL for the audio file.
        """
        if not self._url_validated:
            if not self._test_url_exists(self.url):
                self._url_validated = self._retrieve_url()
                self._url = self._url_validated
            else:
                self._url_validated = self._url
        return self._url_validated

    def _retrieve_url(self) -> str:
        """Retrieve an url

        @return: the url
        """
        url = self.url
        try:
            response = requests.get(
                self._URL_COMMOS + "File:" + self.filename.replace(" ", "_")
            )
            src = re.compile(self._REG + self.filename.replace(" ", "_"), re.I)

            for chunk in response.iter_content(1024, decode_unicode=True):
                match = src.search(chunk)
                if match:
                    url = match.group(0)
                    break
        except requests.RequestException:
            traceback.print_exc()
        return url

    def _create_url(self) -> str:
        """Create a full-fledged URL.

        @return: the url
        """
        name = self.filename.replace(" ", "_")
        m = hashlib.md5()
        m.update(bytes(name, encoding="UTF-8"))
        md5_hex = m.hexdigest()
        hash1 = md5_hex[:1]
        hash2 = md5_hex[:2]
        return (
            self._URL_PREFIX
            + hash1
            + "/"
            + hash2
            + "/"
            + urllib.parse.quote_plus(name, encoding="UTF-8")
        )

    @staticmethod
    def get_response_code(url_string: str) -> int:
        """Get the response code for an input URL string.

        @param url_string: The URL string.
        @type url_string: str

        @return: The response code for an input URL.
        @rtype: int
        """
        response = requests.head(url_string, timeout=(0.5, 0.5))
        return response.status_code

    @classmethod
    def _test_url_exists(cls, url_string: str) -> bool:
        """Check whether a given URL exists, namely whether it does return
        a 404 error code.

        @param url_string: the url to check

        @return: true if it exists, false otherwise.
        """
        try:
            response_code = cls.get_response_code(cls._HTTP_PREFIX + url_string)
            return response_code == requests.codes.ok
        except requests.exceptions.URLRequired:
            return False
        except requests.RequestException:
            return False


class BabelSensePhonetics:
    """A class modeling audio and transcription of a BabelSense.

    @ivar audios: Set of audio items.
    @type audios: Set[BabelAudio]
    @ivar transcriptions: Set of pronunciation transcriptions.
    @type transcriptions: Set[str]
    """

    def __init__(self, audios: Set[BabelAudio], transcriptions: Set[str]):
        """init method
        @param audios: Set of audio items.
        @type audios: Set[BabelAudio]
        @param transcriptions: Set of pronunciation transcriptions.
        @type transcriptions: Set[str]
        """
        if audios is None:
            self.audios = set()
        else:
            self.audios = audios
        if transcriptions is None:
            self.transcriptions = set()
        else:
            self.transcriptions = transcriptions

    def __str__(self):
        return "audio: %d" % len(self.audios) + "\ttranscriptions: %d" % len(
            self.transcriptions
        )

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)


def transcription_from_string(value: str) -> Tuple[str, str]:
    """Transform a transcription string into a pair of (language_lemma, transcription)s.

    @param value: Transcription string.

    @return: A pair of (language_lemma, transcription)s.

    @raises RuntimeError: if the transcription is invalid
    """
    elems = value.split(":")
    if len(elems) < 4:
        raise RuntimeError("Invalid transcription: " + value)
    resource = elems[0]
    language = elems[1]
    lemma = elems[2].lower()
    transc_title = value.replace(resource + ":" + language + ":" + lemma + ":", "")
    return language + ":" + lemma, transc_title


def audio_from_string(value: str) -> Tuple[str, BabelAudio]:
    """Transform an audio string into a pair of (language_lemma, audio_item)s.

    @param value: Audio string.

    @return: a pair of (language_lemma, audio_item).

    @raises RuntimeError:
    """
    elems = value.split(":")
    if len(elems) < 3:
        raise RuntimeError("Invalid audio: " + value)
    resource = elems[0]
    language = Language[elems[1]]
    lemma = elems[2]
    title = value.replace(resource + ":" + str(language) + ":" + lemma + ":", "")
    lemma = elems[2].lower()
    return str(language) + ":" + lemma, BabelAudio(lemma, language, title)


__all__ = [
    "BabelAudio",
    "BabelSensePhonetics",
    "transcription_from_string",
    "audio_from_string",
]
