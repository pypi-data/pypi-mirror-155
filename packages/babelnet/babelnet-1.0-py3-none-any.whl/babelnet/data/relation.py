"""This module contains BabelSynsetRelation and data related to the edges in the BabelNet graph."""
import traceback
from collections import OrderedDict
from aenum import Enum, extend_enum
from typing import List

from babelnet.resources import BabelSynsetID
from babelnet.language import Language
from babelnet.conf import _config


class RelationGroup(Enum):
    """Group of relations (used to bring together relations
    belonging to the same group).
    @ivar ordinal: the ordinal of the enum
    @type ordinal: int
    """

    HYPERNYM: "RelationGroup" = 0
    HYPONYM: "RelationGroup" = 1
    MERONYM: "RelationGroup" = 2
    HOLONYM: "RelationGroup" = 3
    OTHER: "RelationGroup" = 4

    def __init__(self, ordinal: int):
        """init method
        @param ordinal: the ordinal
        """
        self.ordinal: int = ordinal

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class BabelSynsetRelation:
    """
    Class that models a relation to a synset ID in the BabelNet network.

    @ivar language: The language of the relation.
    @type language: Language
    @ivar pointer: The relation type.
    @type pointer: BabelPointer
    @ivar target: The target offset.
    @type target: str
    """

    def __init__(self, language: Language, pointer: "BabelPointer", target: str):
        """init method
        @param language: The language of the relation.
        @type language: Language
        @param pointer: The relation type.
        @type pointer: BabelPointer
        @param target: The target offset.
        @type target: str
        """
        self.language = language
        self.pointer = pointer
        self.target = target

    def __hash__(self):
        return hash((self.language, self.pointer, self.target))

    def __str__(self):
        seq = (str(self.language), self.pointer.symbol, self.target)
        return "_".join(seq)

    def __repr__(self):
        # return '{0} ({1})'.format(object.__repr__(self), str(self))
        return str(self)

    def __eq__(self, other):
        if isinstance(other, BabelSynsetRelation):
            return (
                    self.language is other.language
                    and self.pointer.symbol == other.pointer.symbol
                    and self.target == other.target
            )
        return False

    @staticmethod
    def from_string(edge: str) -> "BabelSynsetRelation":
        """Create a new instance of BabelSynsetRelation from an input record
        in the same format as found in BabelNetIndexField.

        @param edge: The String representation of the edge.
        @type edge: str

        @return: Relation instance.
        @rtype: BabelSynsetRelation

        @raise RuntimeError: if the relation is invalid
        """
        # EN_r_bn:00026887n       --> 3 split
        # DS_NL_r_bn:20268406n   --> 4 split
        # BE_X_OLD_r_bn:20135356n --> 5 split
        relation_split = edge.split("_")
        if len(relation_split) not in [3, 4, 5]:
            raise RuntimeError("Invalid relation: " + edge)

        elif len(relation_split) == 3:
            return BabelSynsetRelation(
                Language[relation_split[0]],
                BabelPointer.from_symbol(relation_split[1]),
                relation_split[2],
            )

        elif len(relation_split) == 4:
            return BabelSynsetRelation(
                Language["_".join(relation_split[0:2])],
                BabelPointer.from_symbol(relation_split[2]),
                relation_split[3],
            )

        else:
            return BabelSynsetRelation(
                Language["_".join(relation_split[:3])],
                BabelPointer.from_symbol(relation_split[3]),
                relation_split[4],
            )

    @property
    def id_target(self):
        """
        Get the target as a BabelSynsetID.

        @return: the target as a BabelSynsetID.
        @rtype: BabelSynsetID
        """
        return BabelSynsetID(self.target)


class BabelPointerNotPresentError(RuntimeError):
    """Runtime error launched if a BabelPointer is not present"""
    pass


class BabelPointer(Enum):
    """Models a semantic pointer in BabelNet. Includes an associative (i.e.
    semantically unspecified) relation.
    Notes: At runtime this Enum is expanded with additional values.

    @ivar symbol: The symbol in BabelNet data files that is used to indicate this pointer type.
    @type symbol: str
    @ivar relation_name: Relation name.
    @type relation_name: str
    @ivar short_name: Relation short name.
    @type short_name: str
    @ivar relation_group: Relation group the pointer belongs to (e.g. HYPERNYM).
    @type relation_group: RelationGroup
    @ivar is_automatic: Is automatic relation (default False).
    @type is_automatic: bool

    """

    SEMANTICALLY_RELATED: "BabelPointer" = "r", "Semantically related form", "related"
    """Wikipedia relations."""

    GLOSS_MONOSEMOUS: "BabelPointer" = "gmono", "Gloss related form (monosemous)", "gloss-related"
    """Gloss related form (monosemous) from WordNet."""

    GLOSS_DISAMBIGUATED: "BabelPointer" = "gdis", "Gloss related form (disambiguated)", "gloss-related"
    """Gloss related form (disambiguated) from WordNet."""

    ALSO_SEE: "BabelPointer" = "^", "Also See", "also-see"
    """Also See from WordNet."""

    ANTONYM: "BabelPointer" = "!", "Antonym", "antonym"
    """Antonym from WordNet."""

    ATTRIBUTE: "BabelPointer" = "=", "Attribute", "attrib"
    """Attribute from WordNet."""

    CAUSE: "BabelPointer" = ">", "Cause", "cause"
    """Cause from WordNet."""

    DERIVATIONALLY_RELATED: "BabelPointer" = "+", "Derivationally related form", "deriv"
    """Derivationally related form from WordNet."""

    ENTAILMENT: "BabelPointer" = "*", "Entailment", "entails"
    """Entailment from WordNet."""

    HYPERNYM: "BabelPointer" = "@", "Hypernym", "is-a", RelationGroup.HYPERNYM
    """Hypernym from WordNet."""

    HYPERNYM_INSTANCE: "BabelPointer" = "@i", "Instance hypernym", "is-a", RelationGroup.HYPERNYM
    """Instance hypernym from WordNet."""

    HYPONYM: "BabelPointer" = "~", "Hyponym", "has-kind", RelationGroup.HYPONYM
    """Hyponym from WordNet."""

    HYPONYM_INSTANCE: "BabelPointer" = "~i", "Instance hyponym", "has-kind", RelationGroup.HYPONYM
    """Instance hyponym from WordNet."""

    HOLONYM_MEMBER: "BabelPointer" = "#m", "Member holonym", "has-part", RelationGroup.HOLONYM
    """Member holonym from WordNet."""

    HOLONYM_SUBSTANCE: "BabelPointer" = "#s", "Substance holonym", "has-part", RelationGroup.HOLONYM
    """Substance holonym from WordNet."""

    HOLONYM_PART: "BabelPointer" = "#p", "Part holonym", "has-part", RelationGroup.HOLONYM
    """Part holonym from WordNet."""

    MERONYM_MEMBER: "BabelPointer" = "%m", "Member meronym", "part-of", RelationGroup.MERONYM
    """Member meronym from WordNet."""

    MERONYM_SUBSTANCE: "BabelPointer" = "%s", "Substance meronym", "part-of", RelationGroup.MERONYM
    """Substance meronym from WordNet."""

    MERONYM_PART: "BabelPointer" = "%p", "Part meronym", "part-of", RelationGroup.MERONYM
    """Part meronym from WordNet."""

    PARTICIPLE: "BabelPointer" = "<", "Participle", "participle"
    """Participle from WordNet."""

    PERTAINYM: "BabelPointer" = "\\", "Pertainym BabelPointer(pertains to nouns)", "pertains-to"
    """Pertainym from WordNet."""

    REGION: "BabelPointer" = ";r", "Domain of synset - REGION", "domain"
    """Domain of synset - REGION from WordNet."""

    REGION_MEMBER: "BabelPointer" = "-r", "Member of this domain - REGION", "domain"
    """Member of this domain from WordNet."""

    SIMILAR_TO: "BabelPointer" = "&", "Similar To", "sim"
    """Similar To from WordNet."""

    TOPIC: "BabelPointer" = ";c", "Domain of synset - TOPIC", "topic"
    """Domain of synset - TOPIC from WordNet."""

    TOPIC_MEMBER: "BabelPointer" = "-c", "Member of this domain - TOPIC", "topic"
    """Member of this domain - TOPIC from WordNet."""

    USAGE: "BabelPointer" = ";u", "Domain of synset - USAGE", "usage"
    """Domain of synset - USAGE from WordNet."""

    USAGE_MEMBER: "BabelPointer" = "-u", "Member of this domain - USAGE", "usage"
    """Member of this domain - USAGE from WordNet."""

    VERB_GROUP: "BabelPointer" = "$", "Verb Group", "verb_group"
    """Verb Group from WordNet."""

    WIBI_HYPERNYM: "BabelPointer" = "@w", "Hypernym", "is-a", RelationGroup.HYPERNYM, True
    """Hypernym from Wikipedia Bitaxonomy."""

    WIKIDATA_HYPERNYM: "BabelPointer" = "@wd", "Hypernym", "is-a", RelationGroup.HYPERNYM
    """Hypernym from Wikidata."""

    WIKIDATA_MERONYM: "BabelPointer" = "%wdm", "Part meronym", "part-of", RelationGroup.MERONYM
    """Meronym from Wikidata."""

    WIBI_HYPONYM: "BabelPointer" = "~@w", "Hyponym", "has-kind", RelationGroup.HYPONYM, True
    """Hyponym from Wikipedia Bitaxonomy."""

    WIKIDATA_HYPONYM_INSTANCE: "BabelPointer" = "~wd", "Hyponym", "has-kind", RelationGroup.HYPONYM
    """Hyponym instance from Wikidata."""

    WIKIDATA_HYPONYM: "BabelPointer" = "~wds", "Hyponym", "has-kind", RelationGroup.HYPONYM
    """Hyponym from Wikidata."""

    ANY_HYPERNYM: "BabelPointer" = "ahpe", "Any Hypernym", "is-a", RelationGroup.HYPERNYM
    """Hypernyms from all res."""

    ANY_MERONYM: "BabelPointer" = "am", "Any Meronym", "part-of", RelationGroup.MERONYM
    """Meronyms from all res."""

    ANY_HOLONYM: "BabelPointer" = "aho", "Any Holonym", "has-part", RelationGroup.HOLONYM
    """Holonyms from all res."""

    ANY_HYPONYM: "BabelPointer" = "ahpo", "Any Hyponym", "has-kind", RelationGroup.HYPONYM
    """Hyponyms from all res."""

    def __init__(
            self,
            symbol,
            relation_name,
            short_name,
            relation_group=RelationGroup.OTHER,
            is_automatic=False,
    ):
        """init method
        @param symbol: The symbol in BabelNet data files that is used to indicate this pointer type.
        @type symbol: str
        @param relation_name: Relation name.
        @type relation_name: str
        @param short_name: Relation short name.
        @type short_name: str
        @param relation_group: Relation group the pointer belongs to (e.g. HYPERNYM) (default: RelationGroup.OTHER).
        @type relation_group: RelationGroup
        @param is_automatic: Is automatic relation (default False).
        @type is_automatic: bool
        """
        self.symbol = symbol
        self.relation_name = relation_name
        self.short_name = short_name
        self.relation_group = relation_group
        self.is_automatic = is_automatic

    def __str__(self):
        return self.relation_name.lower().replace(" ", "_").replace(",", "")

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, BabelPointer):
            return (
                    self.relation_name == other.relation_name
                    and self.symbol == other.symbol
            )
        return False

    def __hash__(self):
        return hash((self.relation_name, self.symbol))

    @property
    def is_hypernym(self) -> bool:
        """True if the relation is of a hypernymy kind.

        @return: True if the relation is of a hypernymy kind, False otherwise
        @rtype: bool
        """
        return self.relation_group is RelationGroup.HYPERNYM

    @property
    def is_hyponymy(self) -> bool:
        """True if the relation is of a hyponymy kind.

        @return: True if the relation is of a hyponymy kind, False otherwise.
        @rtype: bool
        """
        return self.relation_group is RelationGroup.HYPONYM

    @property
    def is_meronym(self) -> bool:
        """True if the relation is of a meronym kind.

        @return: True if the relation is of a meronym kind, False otherwise.
        @rtype: bool
        """
        return self.relation_group is RelationGroup.MERONYM

    @property
    def is_holonym(self) -> bool:
        """True if the relation is of a holonym kind.

        @return: True if the relation is of a holonym kind, False otherwise.
        @rtype: bool
        """
        return self.relation_group is RelationGroup.HOLONYM

    # @classmethod
    # def values(cls):
    #     """Return a collection of all the pointers declared in this Enum,
    #     in the order they are declared.
    #
    #     Returns
    #     -------
    #     List[BabelPointer]
    #         The full collection of BabelPointers.
    #     """
    #     return list(cls._symbol_to_pointer.values())

    @classmethod
    def from_name(cls, name: str) -> List["BabelPointer"]:
        """Return the pointer types that match the specified pointer name.

        @param name: The name string of the relations.
        @type name: str

        @return: The BabelPointers corresponding to the given name.
        @rtype: List[BabelPointer]

        @raise BabelPointerNotPresentError: Raised if the name does not correspond to a known pointer.
        """
        try:
            return cls._name_to_pointer[name.lower()]
        except KeyError:
            raise BabelPointerNotPresentError(name)

    @classmethod
    def from_symbol(cls, symbol: str) -> "BabelPointer":
        """Return the pointer type that matches the specified pointer symbol.

        @param symbol: The string representation of the semantic relation.
        @type symbol: str

        @return: The type of semantic relation.
        @rtype: BabelPointer

        @raise BabelPointerNotPresentError: Raised if the name does not correspond to a known pointer.
        """
        try:
            return cls._symbol_to_pointer[symbol]
        except KeyError:
            raise BabelPointerNotPresentError(symbol)


BabelPointer._symbol_to_pointer = OrderedDict(
    (pointer.symbol, pointer) for pointer in BabelPointer
)
BabelPointer._name_to_pointer = OrderedDict(
    (pointer.relation_name.lower(), pointer) for pointer in BabelPointer
)


def _add_extra_relations():
    if _config.DOC_BUILDING:
        return
    try:
        with open(_config.POINTER_LIST_PATH, encoding="utf8") as file:
            for _line in file:
                if _line.startswith("%") or _line == "":
                    continue
                _line = _line.strip()
                _pointers = _line.split("\t")
                _symbol = _pointers[0]
                _name = _pointers[1]
                _short_name = _pointers[2]

                _enum_name = _name.upper().replace(" ", "_")
                if _enum_name in BabelPointer._member_map_:
                    _enum_name += "_"+_symbol

                if len(_pointers) == 4:
                    extend_enum(
                        BabelPointer,
                        _enum_name,
                        _symbol,
                        _name,
                        _short_name,
                        RelationGroup[_pointers[3]],
                    )
                elif len(_pointers) == 5:
                    extend_enum(
                        BabelPointer,
                        _enum_name,
                        _symbol,
                        _name,
                        _short_name,
                        RelationGroup[_pointers[3]],
                    )
                else:
                    extend_enum(
                        BabelPointer,
                        _enum_name,
                        _symbol,
                        _name,
                        _short_name,
                    )
                BabelPointer._symbol_to_pointer[_symbol.lower()] = BabelPointer[_enum_name]
                BabelPointer._name_to_pointer[_name.lower()] = BabelPointer[_enum_name]
    except FileExistsError:
        traceback.print_exc()
    except IOError:
        traceback.print_exc()
