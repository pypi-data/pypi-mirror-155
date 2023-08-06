"""This module contains the BabelDomain enum."""

from aenum import Enum


class BabelDomain(Enum):
    """Domain of a BabelSynset."""

    # Original 34 domains
    ART_ARCHITECTURE_AND_ARCHAEOLOGY: "BabelDomain" = (
        "Art, architecture, and archaeology",
        "Art (painting, visual arts, sculpture, etc. except for music, dance, poetry, photography and theatre), architecture (construction, buildings, etc.), archaeology (sites, finds etc.), prehistory.",
    )
    """Art (painting, visual arts, sculpture, etc.; except for music, dance, poetry, photography and theatre), architecture (construction, buildings, etc.), archaeology (sites, finds etc.), prehistory."""

    BIOLOGY: "BabelDomain" = (
        "Biology",
        "Biology; animals, plants and their classifications, microorganisms.",
    )
    """Biology; animals, plants and their classifications, microorganisms."""

    ANIMALS: "BabelDomain" = "Animals", ""
    """deprecated domain merged with BIOLOGY"""

    BUSINESS_ECONOMICS_AND_FINANCE: "BabelDomain" = "Business, economics, and finance", ""
    """deprecated domain merged with BUSINESS_INDUSTRY_AND_FINANCE"""

    NUMISMATICS_AND_CURRENCIES: "BabelDomain" = (
        "Numismatics and currencies",
        "Currencies and their study.",
    )
    """Currencies and their study."""

    CHEMISTRY_AND_MINERALOGY: "BabelDomain" = (
        "Chemistry and mineralogy",
        "Chemistry, compounds, chemicals, minerals, mineralogy.",
    )
    """Chemistry, compounds, chemicals, minerals, mineralogy."""

    COMPUTING: "BabelDomain" = "Computing", "Computer science, computing, hardware and software."
    """Computer science, computing, hardware and software."""

    CULTURE_AND_SOCIETY: "BabelDomain" = "Culture and society", ""
    """deprecated domain merged with CULTURE_ANTHROPOLOGY_AND_SOCIETY"""

    EDUCATION: "BabelDomain" = "Education", ""
    """deprecated domain merged with EDUCATION_AND_SCIENCE"""

    ENGINEERING_AND_TECHNOLOGY: "BabelDomain" = "Engineering and technology", ""
    """deprecated domain merged with CRAFT_ENGINEERING_AND_TECHNOLOGY"""

    FOOD_AND_DRINK: "BabelDomain" = "Food and drink", ""
    """deprecated domain merged with FOOD_DRINK_AND_TASTE"""

    GEOGRAPHY_AND_PLACES: "BabelDomain" = "Geography and places", ""
    """deprecated domain merged with GEOGRAPHY_GEOLOGY_AND_PLACES"""

    GEOLOGY_AND_GEOPHYSICS: "BabelDomain" = "Geology and geophysics", ""
    """deprecated domain merged with GEOGRAPHY_GEOLOGY_AND_PLACES"""

    HEALTH_AND_MEDICINE: "BabelDomain" = (
        "Health and medicine",
        "Human health and medicine; diseases, drugs and prescriptions; physical, mental and social well-being.",
    )
    """Human health and medicine; diseases, drugs and prescriptions; physical, mental and social well-being."""

    HERALDRY_HONORS_AND_VEXILLOLOGY: "BabelDomain" = (
        "Heraldry, honors, and vexillology",
        "Armory, vexillology, honors, ranks.",
    )
    """Armory, vexillology, honors, ranks."""

    HISTORY: "BabelDomain" = (
        "History",
        "Events of the past occurred after the invention of writing systems (for prehistory, see archaeology).",
    )
    """Events of the past occurred after the invention of writing systems (for prehistory, see archaeology)."""

    LANGUAGE_AND_LINGUISTICS: "BabelDomain" = (
        "Language and linguistics",
        "Languages, linguistics, idiomatic expressions, phrases.",
    )
    """Languages, linguistics, idiomatic expressions, phrases."""

    LAW_AND_CRIME: "BabelDomain" = (
        "Law and crime",
        "Laws, justice, judges, police, crimes, criminal minds and behaviors.",
    )
    """Laws, justice, judges, police, crimes, criminal minds and behaviors."""

    LITERATURE_AND_THEATRE: "BabelDomain" = (
        "Literature and theatre",
        "Literature, authors, books, novels, poetry, plays, theatre.",
    )
    """Literature, authors, books, novels, poetry, plays, theatre."""

    MATHEMATICS: "BabelDomain" = "Mathematics", ""
    """deprecated domain merged with MATHEMATICS_AND_STATISTICS"""

    MEDIA: "BabelDomain" = "Media", ""
    """deprecated domain merged with MEDIA_AND_PRESS"""

    METEOROLOGY: "BabelDomain" = "Meteorology", ""
    """deprecated domain merged with ENVIRONMENT_AND_METEOROLOGY"""

    MUSIC: "BabelDomain" = "Music", ""
    """deprecated domain merged with MUSIC_SOUND_AND_DANCING"""

    PHILOSOPHY_AND_PSYCHOLOGY: "BabelDomain" = "Philosophy and psychology", ""
    """deprecated domain merged with PHILOSOPHY_PSYCHOLOGY_AND_BEHAVIOR"""

    PHYSICS_AND_ASTRONOMY: "BabelDomain" = (
        "Physics and astronomy",
        "Physics, physical measures and phenomena, matter, its motion and energy; astronomical concepts, celestial objects, space, physical universe.",
    )
    """Physics and astronomy."""

    POLITICS_AND_GOVERNMENT: "BabelDomain" = "Politics and government", ""
    """deprecated domain merged with POLITICS_GOVERNMENT_AND_NOBILITY"""

    RELIGION_MYSTICISM_AND_MYTHOLOGY: "BabelDomain" = (
        "Religion, mysticism and mythology",
        "Religions, faiths, beliefs, mysticism, mythological creatures, myths.",
    )
    """Religions, faiths, beliefs, mysticism, mythological creatures, myths."""

    ROYALTY_AND_NOBILITY: "BabelDomain" = "Royalty and nobility", ""
    """deprecated domain merged with POLITICS_GOVERNMENT_AND_NOBILITY"""

    SPORT_AND_RECREATION: "BabelDomain" = "Sport and recreation", ""
    """deprecated domain merged with SPORT_GAMES_AND_RECREATION"""

    TRANSPORT_AND_TRAVEL: "BabelDomain" = (
        "Transport and travel",
        "Transport, modes of transportation, transportation activities; travels, trips, traveling, travelers, tourism.",
    )
    """Transport, modes of transportation, transportation activities; travels, trips, traveling, travelers, tourism."""

    GAMES_AND_VIDEO_GAMES: "BabelDomain" = "Games and video games", ""
    """deprecated domain merged with SPORT_GAMES_AND_RECREATION"""

    WARFARE_AND_DEFENSE: "BabelDomain" = "Warfare and defense", ""
    """deprecated domain merged with WARFARE_VIOLENCE_AND_DEFENSE"""

    FARMING: "BabelDomain" = "Farming", ""
    """deprecated domain merged with FARMING_FISHING_AND_HUNTING"""

    TEXTILE_AND_CLOTHING: "BabelDomain" = "Textile and clothing", ""
    """deprecated domain merged with TEXTILE_FASHION_AND_CLOTHING"""

    # 8 new domains starting from BabelNet 4 (42 overall)
    VISUAL: "BabelDomain" = (
        "Visual",
        "Visual concepts (visual perception, sight, colors, visibility, except spatial concepts).",
    )
    """deprecated domain merged with VISION_AND_VISUAL"""

    COMMUNICATION_AND_TELECOMMUNICATION: "BabelDomain" = (
        "Communication and telecommunication",
        "Communication (oral, written, etc.) and telecommunication (telegraph, telephone, TV, radio, fax, Internet, etc.) means.",
    )
    """Communication (oral, written, etc.) and telecommunication (telegraph, telephone, TV, radio, fax, Internet, etc.) means."""

    EMOTIONS_AND_FEELINGS: "BabelDomain" = (
        "Emotions and feelings",
        "Feelings, emotions, emotional states and reactions.",
    )
    """Feelings and emotions."""

    ENVIRONMENT: "BabelDomain" = "Environment", ""
    """deprecated domain merged with ENVIRONMENT_AND_METEOROLOGY"""

    FISHING_AND_HUNTING: "BabelDomain" = "Fishing and hunting", ""
    """deprecated domain merged with FARMING_FISHING_AND_HUNTING"""

    NAVIGATION_AND_AVIATION: "BabelDomain" = (
        "Navigation and aviation",
        "Nautical and aviation concepts: vessels and aircrafts; pilots; sea and air traveling.",
    )
    """Nautical and aviation concepts: vessels and aircrafts; pilots; sea and air traveling."""

    SEX: "BabelDomain" = "Sex", "Sexual connotation; sexual activities; sexual reproduction; sexology."
    """Sexual connotation; sexual activities; sexual reproduction; sexology."""

    TIME: "BabelDomain" = "Time", "Temporal concepts; time; events."
    """Temporal concepts; time; events."""

    # new domains starting from BabelNet 5
    SPORT_GAMES_AND_RECREATION: "BabelDomain" = (
        "Sport, games and recreation",
        "Sports, games and video games, recreation (pastimes, hobbies, etc.)",
    )
    """Sports, games and video games, recreation (pastimes, hobbies, etc.)"""

    CRAFT_ENGINEERING_AND_TECHNOLOGY: "BabelDomain" = (
        "Craft, engineering and technology",
        "Crafts (handicraft, skilled work, etc.), engineering, technology.",
    )
    """Crafts (handicraft, skilled work, etc.), engineering, technology."""
    MATHEMATICS_AND_STATISTICS: "BabelDomain" = (
        "Mathematics and statistics",
        "Mathematics, statistics, numbers, mathematical operations and functions, mathematical and statistical concepts.",
    )
    """Mathematics, statistics, numbers, mathematical operations and functions, mathematical and statistical concepts."""
    FOOD_DRINK_AND_TASTE: "BabelDomain" = (
        "Food, drink and taste",
        "Food, drinks, flavors, sense of taste; eating places (bars, pubs, restaurants), food events.",
    )
    """Food, drinks, flavors, sense of taste; eating places (bars, pubs, restaurants), food events."""
    POLITICS_GOVERNMENT_AND_NOBILITY: "BabelDomain" = (
        "Politics, government and nobility",
        "Politics, political leaders and representatives; government; nobility.",
    )
    """Politics, political leaders and representatives; government; nobility."""
    SPACE_AND_TOUCH: "BabelDomain" = (
        "Space and touch",
        "Concepts of space and the sense of touch; dimensionality, proprioception (sense of position and movement) and haptic perception.",
    )
    """Concepts of space and the sense of touch; dimensionality, proprioception (sense of position and movement) and haptic perception."""
    SMELL_AND_PERFUME: "BabelDomain" = (
        "Smell and perfume",
        "Sense of smell; good and bad smells.",
    )
    """Sense of smell; good and bad smells."""
    TASKS_JOBS_ROUTINE_AND_EVALUATION: "BabelDomain" = (
        "Tasks, jobs, routine and evaluation",
        "Tasks, chores, activities, jobs; evaluation, validation, marking, checking, correcting.",
    )
    """Tasks, chores, activities, jobs; evaluation, validation, marking, checking, correcting."""
    GEOGRAPHY_GEOLOGY_AND_PLACES: "BabelDomain" = (
        "Geography, geology and places",
        "Geography and geographical concepts (continents, countries, regions, provinces, cities, towns, villages, rivers, hills, mountains, plains, etc.); geology and geological concepts (solid Earth, rocks, geological processes, earthquakes, volcanos, etc.); geophysics; places.",
    )
    """Geography and geographical concepts (continents, countries, regions, provinces, cities, towns, villages, rivers, hills, mountains, plains, etc.); geology and geological concepts (solid Earth, rocks, geological processes, earthquakes, volcanos, etc.); geophysics; places."""
    SOLID_LIQUID_AND_GAS_MATTER: "BabelDomain" = (
        "Solid, liquid and gas matter",
        "The states of matter (solid, liquid, gas).",
    )
    """The states of matter (solid, liquid, gas)."""
    POSSESSION: "BabelDomain" = (
        "Possession",
        "Concepts of possession; items which tend to belong to people.",
    )
    """Concepts of possession; items which tend to belong to people."""
    FARMING_FISHING_AND_HUNTING: "BabelDomain" = (
        "Farming, fishing and hunting",
        "Farming, agriculture; plant cultivation, livestock raising; fishing; hunting.",
    )
    """Farming, agriculture; plant cultivation, livestock raising; fishing; hunting."""
    TEXTILE_FASHION_AND_CLOTHING: "BabelDomain" = (
        "Textile, fashion and clothing",
        "Fabric, clothes, clothing, footwear, lifestyle, accessories, makeup, hairstyle, fashion, fashion designers.",
    )
    """Fabric, clothes, clothing, footwear, lifestyle, accessories, makeup, hairstyle, fashion, fashion designers."""
    PHILOSOPHY_PSYCHOLOGY_AND_BEHAVIOR: "BabelDomain" = (
        "Philosophy, psychology and behavior",
        "Philosophical concepts, philosophers; psychology, psychological concepts; human behavior.",
    )
    """Philosophical concepts, philosophers; psychology, psychological concepts; human behavior."""
    MUSIC_SOUND_AND_DANCING: "BabelDomain" = (
        "Music, sound and dancing",
        "Sound, sounds, hearing; music, songs, music artists, composers; dances, dancing, dancers.",
    )
    """Sound, sounds, hearing; music, songs, music artists, composers; dances, dancing, dancers."""
    ENVIRONMENT_AND_METEOROLOGY: "BabelDomain" = (
        "Environment and meteorology",
        "Natural environment and its preservation; ecology; natural events (fires, rains, typhoons, etc.); meteorology, weather conditions.",
    )
    """Natural environment and its preservation; ecology; natural events (fires, rains, typhoons, etc.); meteorology, weather conditions."""
    EDUCATION_AND_SCIENCE: "BabelDomain" = (
        "Education and science",
        "Education, teaching, students; science and general scientific concepts (specific concepts go to the various domains: mathematics, physics, astronomy, biology, chemistry, geology, computing, etc.).",
    )
    """Education, teaching, students; science and general scientific concepts (specific concepts go to the various domains: mathematics, physics, astronomy, biology, chemistry, geology, computing, etc.)."""
    CULTURE_ANTHROPOLOGY_AND_SOCIETY: "BabelDomain" = (
        "Culture, anthropology and society",
        "Concepts affecting local and global culture and society; social behavior, trends, norms and expectations in human society; anthropology.",
    )
    """Concepts affecting local and global culture and society; social behavior, trends, norms and expectations in human society; anthropology."""
    BUSINESS_INDUSTRY_AND_FINANCE: "BabelDomain" = (
        "Business, industry and finance",
        "Business, industry, economy, finance, management, money.",
    )
    """Business, industry, economy, finance, management, money."""

    WARFARE_VIOLENCE_AND_DEFENSE: "BabelDomain" = (
        "Warfare, violence and defense",
        "Wars, battles, warfare, physical violence, personal and country defense, secret agencies.",
    )
    """Wars, battles, warfare, physical violence, personal and country defense, secret agencies."""

    MEDIA_AND_PRESS: "BabelDomain" = (
        "Media and press",
        "Mass media such as print media (news media, newspapers, magazines, etc.), publishing, photography, cinema (films, directors, screenwriters, etc.), broadcasting (radio and television), and advertising.",
    )
    """Mass media such as print media (news media, newspapers, magazines, etc.), publishing, photography, cinema (films, directors, screenwriters, etc.), broadcasting (radio and television), and advertising."""

    VISION_AND_VISUAL: "BabelDomain" = (
        "Vision and visual",
        "Visual concepts (visual perception, sight, colors, visibility, except spatial concepts).",
    )
    """Visual concepts (visual perception, sight, colors, visibility, except spatial concepts)."""

    def __init__(self, domain_string: str, description: str):
        """init method
        @param domain_string: the domain as a string
        @param description: a description od the domain
        """
        self._domain_string = domain_string
        self._description = description

    # Duck-typing from Tag
    def value(self) -> "BabelDomain":
        """Return the value of self

        @return: The value of self
        @rtype: "BabelDomain"
        """
        return self

    @property
    def domain_string(self) -> str:
        """The original name of the domain.

        @return: The original name of the domain.
        @rtype: str
        """
        return self._domain_string

    @property
    def description(self) -> str:
        """The description of the domain.

        @return: The original name of the domain.
        @rtype: str
        """
        return self._description

    # non serve perche' posso semplicemente chiamare BabelDomain(str):
    # per esempio:
    #
    # str = 'Business, economics, and finance'
    # bd = BabelDomain(str)
    #
    # @staticmethod
    # def value_of_name(self, value):
    #    """Get the BabelDomain associated to the string given in input.

    # in Java si chiama "value_by"...
    @classmethod
    def from_position(cls, position: int) -> "BabelDomain":
        """Return the BabelDomain of the position given in input.

        @param position: The position of the requested BabelDomain.
        @type position: int

        @return: The corresponding BabelDomain.
        @rtype: BabelDomain

        @raises ValueError: if the position is invalid
        """
        n = len(cls)
        if not 0 <= position < n:
            raise ValueError(
                "the value in input can be > -1 and < "
                + str(n)
                + ", not "
                + str(position)
            )
        return list(cls)[position]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


__all__ = ["BabelDomain"]
