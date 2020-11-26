from enum import Enum, IntEnum


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)

    def next(self, clockwise=True):
        direction = 1 if clockwise else -1
        if self.value[0] == 0:
            x = self.value[1] * (-direction)
            y = 0
        else:
            x = 0
            y = self.value[0] * direction
        return Direction((x, y))


class CC(IntEnum):
    RIGHT = 1
    LEFT = -1

    def next(self):
        return CC(self.value * -1)
