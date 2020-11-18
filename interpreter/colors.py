from enum import IntEnum
from typing import Tuple


class Hue(IntEnum):
    BLACK = -2
    WHITE = -1
    RED = 0
    YELLOW = 1
    GREEN = 2
    CYAN = 3
    BLUE = 4
    MAGENTA = 5


class Lightness(IntEnum):
    LIGHT = 0
    NORMAL = 1
    DARK = 2


class Color():
    def __init__(self, rgb: Tuple[int, int, int]):
        if len(rgb) == 4:
            self.rgb = rgb[:-1]
        else:
            self.rgb = rgb
        self.lightness = colors[self.rgb][0]
        self.hue = colors[self.rgb][1]

    def __eq__(self, other):
        return self.rgb == other.rgb

    def __repr__(self):
        return f'rgb: {self.rgb}'


colors = {(255, 192, 192): (Lightness.LIGHT, Hue.RED),
          (255, 255, 192): (Lightness.LIGHT, Hue.YELLOW),
          (192, 255, 192): (Lightness.LIGHT, Hue.GREEN),
          (192, 255, 255): (Lightness.LIGHT, Hue.CYAN),
          (192, 192, 255): (Lightness.LIGHT, Hue.BLUE),
          (255, 192, 255): (Lightness.LIGHT, Hue.MAGENTA),
          (255, 0, 0): (Lightness.NORMAL, Hue.RED),
          (255, 255, 0): (Lightness.NORMAL, Hue.YELLOW),
          (0, 255, 0): (Lightness.NORMAL, Hue.GREEN),
          (0, 255, 255): (Lightness.NORMAL, Hue.CYAN),
          (0, 0, 255): (Lightness.NORMAL, Hue.BLUE),
          (255, 0, 255): (Lightness.NORMAL, Hue.MAGENTA),
          (192, 0, 0): (Lightness.DARK, Hue.RED),
          (192, 192, 0): (Lightness.DARK, Hue.YELLOW),
          (0, 192, 0): (Lightness.DARK, Hue.GREEN),
          (0, 192, 192): (Lightness.DARK, Hue.CYAN),
          (0, 0, 192): (Lightness.DARK, Hue.BLUE),
          (192, 0, 192): (Lightness.DARK, Hue.MAGENTA),
          (255, 255, 255): (Lightness.NORMAL, Hue.WHITE),
          (0, 0, 0): (Lightness.NORMAL, Hue.BLACK)}
