"""Tokens for BabelSense"""

from functools import total_ordering


@total_ordering
class BabelTokenId:
    """Represents the association between the word that appears in a
    Babel gloss and the BabelSynsetID that identifies the
    lemma in BabelNet.
        @ivar start: The start position.
        @type start: int
        @ivar end: The end position.
        @type end: int
        @ivar id: The id of the BabelSynset.
        @type id: BabelSynsetID
        @ivar word: The word being annotated.
        @type word: str

    """

    def __init__(self, start, end, synset_id, word):
        """init method
        @param start: The start position.
        @type start: int
        @param end: The end position.
        @type end: int
        @param synset_id: The id of the BabelSynset.
        @type synset_id: BabelSynsetID
        @param word: The word being annotated.
        @type word: str
        """
        self.start = start
        self.end = end
        self.id = synset_id
        self.word = word

    def __str__(self):
        return "(%d" % self.start + ", %d" % self.end + ")"

    def __repr__(self):
        # return '{0} {1}'.format(object.__repr__(self), str(self))
        return str(self)

    def __eq__(self, other):
        if isinstance(other, BabelTokenId):
            return self.start == other.start and self.end == other.end
        return False

    def __lt__(self, other):
        if isinstance(other, BabelTokenId):
            if other.start - self.start == 0:
                return self.end > other.end
            else:
                return self.start > other.start
        return NotImplemented

    def __hash__(self):
        return hash((self.start, self.end))


@total_ordering
class BabelTokenWord:
    """
    Represents the token unit which can be used to build sentences.

    @ivar start: The start position.
    @type start: int
    @ivar end: The end position.
    @type end: int
    @ivar lemma: The lemma of the inflected form in the string range.
    @type lemma: str
    """

    def __init__(self, start, end, lemma):
        """init method
        @param start: The start position.
        @type start: int
        @param end: The end position.
        @type end: int
        @param lemma: The lemma of the inflected form in the string range.
        @type lemma: str
        """
        self.start = start
        self.end = end
        self.lemma = lemma

    def __str__(self):
        return "(%d" % self.start + ", %d" % self.end + ")"

    def __repr__(self):
        # return '{0} {1}'.format(object.__repr__(self), str(self))
        return str(self)

    def __eq__(self, other):
        if isinstance(other, BabelTokenWord):
            return self.start == other.start and self.end == other.end
        return False

    def __lt__(self, other):
        if isinstance(other, BabelTokenWord):
            if other.start - self.start == 0:
                return self.end > other.end
            else:
                return self.start > other.start
        return NotImplemented

    def __hash__(self):
        return hash((self.start, self.end))


__all__ = ["BabelTokenId", "BabelTokenWord"]
