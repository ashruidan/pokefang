from enum import Enum

class Actions(Enum):
    # Directional Input
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    # Action Input
    A = "a"
    B = "b"
    # Special Input
    START = "start"
    SELECT = "select"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
