from typing import Tuple


class Pixel:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return 'x: ' + str(self.x) + ' y: ' + str(self.y) + ' color: ' + str(self.color)