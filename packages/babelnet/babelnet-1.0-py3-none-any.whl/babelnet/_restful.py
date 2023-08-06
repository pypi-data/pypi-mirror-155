"""This module handles the RESTful communication of the online BabelNet API."""

import json
import traceback
import requests
from typing import Optional
from aenum import Enum, AutoNumberEnum

from babelnet.resources import WordNetSynsetID, BabelSynsetID
from babelnet.conf import _config

RFKEY = _config.RESTFUL_KEY
RFURL = _config.RESTFUL_URL
session = requests.session()


class RESTfulCallType(AutoNumberEnum):
    """Enum that contains all the available restful call type that can be used
    in order to interrogate the BabelNet RESTful online indexes service."""

    GET_SENSES = ()
    """get_senses call."""

    GET_SYNSETS = ()
    """get_synsets call."""

    GET_PRIVATESYNSET = ()
    """Gets internal synset data."""

    GET_SUCCESSORS = ()
    """get_successor_edges call."""

    GET_IDSFROMRID = ()
    """Get a list of synset ids from a ResourceID."""

    GET_VERSION = ()
    """Get the BabelNet version."""

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class RFParameter(Enum):
    """A RESTful parameter."""

    SETIMAGES = "setnameimages"
    PROTOCOL = "p"

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class RESTfulPacket:
    """BabelNet RESTful request object.

    @ivar wordnet_id: the id of wordnet
    @ivar poses: the POSes to ask for
    @ivar lemmas: the lemmas to ask for
    @ivar sense_sources: the sources to filter for the senses
    @ivar synest_ids: the synset ids to ask for
    @ivar search_languages: the language to filter for the search
    @ivar resource_ids: the resource ids to filter
    @ivar target_languages: the language to use for the response
    @ivar call_type: the type of the request
    @ivar rf_key: teh restful key
    @ivar normalizer: the normalizer to use
    """

    def __init__(self, call_type, rf_key):
        """init method
        @param call_type: The type of the RESTful calls.
        @type call_type: RESTfulCallType
        @param rf_key: The restful key
        """
        if not rf_key:
            raise ValueError(
                "Please define the parameter RESTFUL_KEY in " + "babelnet_conf.yml"
            )
        self.call_type = call_type
        self.rf_key = rf_key
        self.wordnet_id = None
        self.poses = None
        self.lemmas = None
        self.sense_sources = None
        self.synset_ids = None
        self.search_languages = None
        self.resource_ids = None
        self.target_languages = None
        self.normalizer = None

    def to_json(self) -> str:
        """Get the json serialization for this object

        @return: the json serialization
        @rtype: str
        """
        dct = {}
        if self.call_type:
            dct["callType"] = self.call_type.name
        if self.rf_key:
            dct["RFKey"] = self.rf_key
        # controllare bene questo nome... sembra che non serve a nnt ??
        if self.wordnet_id:
            dct["WordNetId"] = self.res_properties(self.wordnet_id)
        if self.poses:
            dct["poses"] = [pos.name for pos in self.poses]
        if self.lemmas:
            dct["lemmas"] = self.lemmas
        if self.sense_sources:
            dct["senseSources"] = [source.name for source in self.sense_sources]
        if self.synset_ids:
            dct["synsetIDs"] = [self.res_properties(sid) for sid in self.synset_ids]
        if self.search_languages:
            dct["searchLanguages"] = [lang.name for lang in self.search_languages]
        if self.resource_ids:
            dct["resourceIDs"] = []
            for res in self.resource_ids:
                package = (
                    "it.uniroma1.lcl.babelnet"
                    if type(res) in [BabelSynsetID, WordNetSynsetID]
                    else "it.uniroma1.lcl.babelnet.resources"
                )
                dct["resourceIDs"].append(
                    {
                        "type": type(res).__name__,
                        "properties": self.res_properties(res),
                        "package": package,
                    }
                )
        if self.target_languages:
            dct["targetLanguages"] = [lang.name for lang in self.target_languages]
        if self.normalizer is not None:
            dct["normalizer"] = self.normalizer
        return json.dumps(dct)

    @staticmethod
    def res_properties(res):
        """
        Get the response properties

        @param res: the response
        @returns: a dict with all the properties of the response inside.
        """
        prop_dct = {}
        if res.id:
            prop_dct["id"] = res.id
        if res.pos:
            prop_dct["pos"] = res.pos.name
        if res.source:
            prop_dct["source"] = res.source.name
        if res.language:
            prop_dct["language"] = res.language.name
        if isinstance(res, WordNetSynsetID):
            if res.version:
                prop_dct["version"] = res.version.name
            if res.version_mapping:
                prop_dct["version_mapping"] = {
                    k.name: v for k, v in res.version_mapping
                }
        return prop_dct


def send_request(packet: RESTfulPacket) -> Optional[bytes]:
    """ Send a request to the BabelNet RESTful service.

    @param packet: the RESTfulPacket to send

    @return: the response as an Optional[bytes]

    @raise ValueError: if the restful key is not set
    @raise RuntimeError: if there is a problem while trying to contact the BabelNet RESTful service
    """
    if not RFURL:
        raise ValueError(
            "Please define the parameter RESTFUL_KEY"
            " in babelnet.ini in the config folder."
        )
    param = {RFParameter.PROTOCOL.value: packet.to_json()}
    try:
        response = session.post(RFURL, data=param)
        if response.status_code != requests.codes.ok:
            if response.status_code == requests.codes.not_found:
                raise RuntimeError(
                    "Sorry, it is not possible to contact the BabelNet RESTful service. "
                    "Please check your connection or the parameter RESTFUL_KEY in babelnet_conf.yml."
                )
            else:
                response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError:
        traceback.print_exc()
    except requests.exceptions.RequestException:
        raise RuntimeError(
            "Sorry, it is not possible to contact the BabelNet RESTful service. "
            "Please check your connection or the parameter RESTFUL_KEY in babelnet_conf.yml."
        )
    return None


def check_error_code(response: bytes) -> bool:
    """ Check the error code of the response received from BabelNet RESTful service.

    @param response: the response
    @rtype: bytes

    @returns: True if the message field is in the response and is not empty.
    @rtype: bool
    """
    try:
        dct = json.loads(response)
    except json.JSONDecodeError:
        return False
    # Il JSON deve essere un dict... se e' una lista non funziona
    if "message" in dct and dct["message"]:
        return True
    return False


def print_error_message(response: bytes) -> bool:
    """
    Warnings: It has to be called after check_error_code has returned True with the same response string.

    @param response: the response
    @type response: bytes

    @return: The error message
    @rtype: bool
    """
    message = json.loads(response)["message"]
    return message
