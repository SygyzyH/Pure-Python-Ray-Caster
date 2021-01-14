from enum import Enum, auto


class PieceType(Enum):
    # object type enumerations
    ENEMY = auto()
    PORTAL = auto()
    SECTOR = auto()
    SPRITE = auto()


class GamePiece:
    def __init__(self, piece_type, location: tuple, vector: tuple = None):
        self._type = piece_type
        self.location = location

        # pointer to map location
        self.vector = vector

    def __str__(self):
        return str(self._type) + " @ " + str(self.location)
