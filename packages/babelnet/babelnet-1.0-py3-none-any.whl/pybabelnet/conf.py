"""The configuration hub for the BabelNet API."""
import logging.config
import os
import pprint
import traceback
from collections import defaultdict
from copy import copy
from typing import Any, Optional, Callable

import yaml
from yaml import SafeLoader

from pybabelnet.language import Language
from pybabelnet.versions import BabelVersion

_CONFIG_FILENAMES = (
    "pybabelnet_conf.yml",
    "pybabelnet_conf",
    "pybabelnet_conf.yaml",
    "pybabelnet_conf.txt",
)

# CONFIG_TEMPLATE = """# PyBabelNet configuration
# # The directory where the BabelNet files are (TO BE SET IF USING OFFLINE APIs).
# #
# # Example
# # BASE_DIR: '/home/your_user/BabelNet-4.0.1'
# BASE_DIR: ''
#
# # The BabelNet key (TO BE SET IF USING ONLINE APIs).
# #
# # Example
# # RESTFUL_KEY: 'ABF-6Y6NRDquIsfmcJcdOEaQ6cYghxjt'
# RESTFUL_KEY: ''
# """
_RES_PATH = os.path.join(os.path.dirname(__file__), "res")


class Option:
    """
    A descriptor implementing PyBabelNet configuration options.

    @ivar default: The default value of this Option.
    @type default: Any
    @ivar interpolate: If interpolate is set to an Option having a str value and the current Option has a str value then the result is the concatenated strings. This is useful for joining a base path with a file name.
    @type interpolate: Optional["Option"]
    @ivar on_change: Optional callback function that is triggered when the Option is modified. The parameter of the function is the Config instance where the descriptor is used.
    @type on_change: Optional[Callable[["Config"], None]]
    @ivar doc: Docstring used to document the Option.
    @type doc: Optional[str]
    @ivar name: Name of the option.
    """

    # TODO: NO TYPING
    def __init__(
        self,
        default: Any,
        interpolate: Optional["Option"] = None,
        on_change: Optional[Callable[["Config"], None]] = None,
        doc: Optional[str] = None,
    ):
        """init method
        @param default: The default value of this Option.
        @type default: Any
        @param interpolate: If interpolate is set to an Option having a str value and the current Option has a str value then the result is the concatenated strings. This is useful for joining a base path with a file name.
        @type interpolate: Optional["Option"]
        @param on_change: Optional callback function that is triggered when the Option is modified. The parameter of the function is the Config instance where the descriptor is used.
        @type on_change: Optional[Callable[["Config"], None]]
        @param doc: Docstring used to document the Option.
        @type doc: Optional[str]
        """
        self.default = default
        self.interpolate = interpolate
        self.on_change = on_change
        self.doc = doc
        self.name = None
        self.__doc__ = self._docstring()

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        if (
            self.interpolate is not None
            and isinstance(obj._values[self.interpolate.name], str)
            and isinstance(obj._values[self.name], str)
        ):
            return obj._values[self.interpolate.name] + obj._values[self.name]
        else:
            return obj._values[self.name]

    def __set__(self, obj, value):
        obj._values[self.name] = value
        self._callback(obj)

    def __set_name__(self, owner, name):
        self.name = name

    def _docstring(self) -> str:
        default = "``default={}``".format(repr(self.default))

        on_change = (
            ", ``on_change={}``".format(self.on_change.__name__)
            if self.on_change is not None
            else ""
        )

        return "{}{}\n{}".format(default, on_change, self.doc or "")

    def _callback(self, obj):
        """Trigger any callbacks."""
        if self.on_change is not None:
            self.on_change(obj)


class Config:
    """
    Base configuration object.
    """

    def __init__(self):
        """init method"""
        self._values = {}
        self._loaded_files = []

        # Set the default value of each ``Option``
        for name, opt in self.options().items():
            # opt._validate(opt.default)
            self._values[name] = opt.default

        # Call hooks for each Option
        # (This must happen *after* all default values are set so that
        # logging can be properly configured.
        for opt in self.options().values():
            opt._callback(self)

    def __str__(self):
        return pprint.pformat(self._values, indent=2)

    def __setattr__(self, name, value):
        if name.startswith("_") or name in self.options().keys():
            super().__setattr__(name, value)
        else:
            raise ValueError("{} is not a valid config option".format(name))

    @classmethod
    def options(cls):
        """Return a dictionary with the Option objects for this config"""
        return {k: v for k, v in cls.__dict__.items() if isinstance(v, Option)}

    def defaults(self):
        """Return the default values of this configuration."""
        return {k: v.default for k, v in self.options().items()}

    def load_dict(self, dct):
        """Load a dictionary of configuration values."""
        if dct:
            for k, v in dct.items():
                setattr(self, k, v)

    def load_file(self, filename):
        """Load config from a YAML file."""
        filename = os.path.abspath(filename)

        with open(filename, encoding="utf8") as f:
            self.load_dict(yaml.load(f, SafeLoader))

        self._loaded_files.append(filename)

    def snapshot(self):
        """Return a snapshot of the current values of this configuration."""
        return copy(self._values)


def _load_languages(conf):
    if isinstance(conf.LANGUAGES, str):
        with open(os.path.join(_RES_PATH, conf.LANGUAGES), encoding="utf8") as stream:
            langs = yaml.load(stream, SafeLoader)["LANGUAGES"]
    else:
        langs = conf.LANGUAGES
    conf._values["LANGUAGES"] = []
    try:
        for lang in langs:
            conf._values["LANGUAGES"].append(Language[lang])
    except Exception:
        conf._values["LANGUAGES"] = [Language.EN]
    if Language.EN not in conf._values["LANGUAGES"]:
        conf._values["LANGUAGES"].append(Language.EN)


def _load_categories(conf):
    if isinstance(conf.CATEGORY_PREFIXES, str):
        with open(
            os.path.join(_RES_PATH, conf.CATEGORY_PREFIXES), encoding="utf8"
        ) as stream:
            param_list = yaml.load(stream, SafeLoader)["CATEGORY_PREFIXES"]
    else:
        param_list = conf.CATEGORY_PREFIXES
    conf._values["CATEGORY_PREFIXES"] = defaultdict(list)
    try:
        # for lang, value in prefixes.items():
        #     conf._values['CATEGORY_PREFIXES'][Language[lang]] = value
        lang = None
        for value in param_list:
            try:
                lang = Language[value.strip()]
            except KeyError:
                conf._values["CATEGORY_PREFIXES"][lang].append(value.strip())
    except Exception:
        traceback.print_exc()


def _config_logger(conf):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
                }
            },
            "handlers": {
                "stdout": {
                    "level": conf.LOG_STDOUT_LEVEL,
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                }
            },
            "root": {
                "level": "DEBUG",
                "handlers": (["stdout"] if conf.LOG_STDOUT_LEVEL else []),
            },
        }
    )


def _set_version(conf: "PyBabelNetConfig"):
    conf._values["VERSION"] = BabelVersion.from_string(conf.VERSION)


def _set_base_version(conf: "PyBabelNetConfig"):
    conf._values["BASE_VERSION"] = BabelVersion.from_string(conf.BASE_VERSION)


class PyBabelNetConfig(Config):
    """The PyBabelNet config manager"""

    BASE_DIR = Option("", doc="""The BabelNet base directory.""")

    LEXICON_INDEX_DIR = Option(
        "/lexicon",
        interpolate=BASE_DIR,
        doc="""The BabelNet lexicon index directory.""",
    )

    DICT_INDEX_DIR = Option(
        "/dict", interpolate=BASE_DIR, doc="""BabelNet dictionary index directory."""
    )

    INFO_INDEX_DIR = Option(
        "/info_CC_BY_NC_SA_30",
        interpolate=BASE_DIR,
        doc="""The BabelNet info index directory.""",
    )

    WN_INFO_INDEX_DIR = Option(
        "/info_wordnet",
        interpolate=BASE_DIR,
        doc="""The WordNet dictionary index directory.""",
    )

    GLOSS_INDEX_DIR = Option(
        "/gloss", interpolate=BASE_DIR, doc="""The BabelNet gloss index directory."""
    )

    GRAPH_INDEX_DIR = Option(
        "/graph_CC_BY_NC_SA_30",
        interpolate=BASE_DIR,
        doc="""The BabelNet graph index directory.""",
    )

    IMAGE_INDEX_DIR = Option(
        "/image", interpolate=BASE_DIR, doc="""The BabelNet image index directory."""
    )

    MAPPING_INDEX_DIR = Option(
        "/core_CC_BY_NC_SA_30",
        interpolate=BASE_DIR,
        doc="""The BabelNet mapping index directory.""",
    )

    RESTFUL_KEY = Option("", doc="""The BabelNet online key.""")

    RESTFUL_URL = Option(
        "http://babelnet.io/v6/service", doc="""The BabelNet RESTful URL."""
    )

    IMAGE_RESTFUL_URL = Option(
        "babelnet.io/images", doc="""The BabelNet RESTful image URL."""
    )

    LANGUAGES = Option(
        "languages.yml", on_change=_load_languages, doc="""The BabelNet languages."""
    )

    IS_BAD_IMAGE_FILTER_ACTIVE = Option(
        True, doc="""Whether the bad image filter is active"""
    )

    POINTER_LIST_PATH = Option("", doc="""The path of the pointer list.""")

    IS_MUL_CONVERSION_FILTER_ACTIVE = Option(
        True, doc="""Whether the MUL conversion is active."""
    )

    USE_REDIRECTION_SENSES = Option(
        True, doc="""Whether redirections also count as appropriate senses."""
    )

    CATEGORY_PREFIXES = Option(
        "category_prefix.yml",
        on_change=_load_categories,
        doc="""The prefixes for the categories in all languages.""",
    )

    LOG_STDOUT_LEVEL = Option(
        "INFO",
        on_change=_config_logger,
        doc="""The logging level of the application.""",
    )

    DOC_BUILDING = Option(False, doc="""Used for building the documentation.""")

    VERSION = Option("5.1", doc="""The index version.""", on_change=_set_version)
    BASE_VERSION = Option("4.0", doc="""The index version.""", on_change=_set_base_version)

    RPC_URL = Option("", doc="""The PyBabelNet Docker endpoint.""")

    def set_actual_version(self, version: BabelVersion):
        self.POINTER_LIST_PATH = os.path.join(
            _RES_PATH,
            "pointer_v2.txt" if version == BabelVersion.V5_0 or version == BabelVersion.V5_1 else "pointer_v1.txt",
        )

        from pybabelnet.data.relation import _add_extra_relations
        _add_extra_relations()

    def log(self):
        """Log current settings."""
        if self._loaded_files:
            _log.info("Loaded configuration from %s", self._loaded_files)
        else:
            _log.info("Using default configuration (no config file provided)")


# def create_config_file():
#     """Create a new configuration file in the current directory."""
#     if not os.path.exists(CONFIG_FILENAME):
#         with open(CONFIG_FILENAME, 'w', encoding='utf8') as f:
#                 f.write(CONFIG_TEMPLATE)
#

_config = PyBabelNetConfig()
_log = logging.getLogger(__name__)

_env_config = 'PYBABELNET_CONF'
if _env_config in os.environ and os.path.exists(os.environ[_env_config]):
    _config.load_file(os.environ[_env_config])
else:
    for f in _CONFIG_FILENAMES:
        if os.path.exists(f):
            _config.load_file(f)
_config.log()

_config.POINTER_LIST_PATH = os.path.join(
    _RES_PATH,
    "pointer_v2.txt" if _config.VERSION == BabelVersion.V5_0 or _config.VERSION == BabelVersion.V5_1 else "pointer_v1.txt",
)

__all__ = ["_CONFIG_FILENAMES", "_config", "PyBabelNetConfig", "Config", "Option"]
