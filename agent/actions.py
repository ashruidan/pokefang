from enum import Enum

class Actions(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ACTION1 = "A"  # Replace with actual action name
    ACTION2 = "B"  # Replace with actual action name

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
