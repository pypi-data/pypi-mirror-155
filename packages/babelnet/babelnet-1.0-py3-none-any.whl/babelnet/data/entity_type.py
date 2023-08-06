"""This module contains the EntityType enum."""

from enum import Enum, auto


class EntityType(Enum):
    """Enumeration describing entity type information"""

    ANIMAL = auto()
    BIOLOGY = auto()
    CELESTIAL_BODY = auto()
    DISEASE = auto()
    EVENT = auto()
    FOOD = auto()
    INSTRUMENT = auto()
    LOCATION = auto()
    MEDIA = auto()
    MONETARY = auto()
    NUMBER = auto()
    ORGANIZATION = auto()
    PERSON = auto()
    PHYSICAL_PHENOMENON = auto()
    PLANT = auto()
    SUPERNATURAL = auto()
    TIME = auto()
    VEHICLE = auto()

    @property
    def value(self) -> "EntityType":
        return self
