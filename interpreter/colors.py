from enum import IntEnum


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
    DARK = 0
    NORMAL = 1
    LIGHT = 2


class Cycle:
    def __init__(self, cycle: []):
        self.cycle = cycle

    def get_next(self, item: IntEnum):
        if item == len(self.cycle) - 1:
            return self.cycle[0]
        return self.cycle[item + 1]


class Colors:
    def __init__(self):
        self.pixel_hue = {(255, 192, 192): (Lightness.LIGHT, Hue.RED),
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
        self.hue_cycle = Cycle([Hue.RED, Hue.YELLOW, Hue.GREEN, Hue.CYAN, Hue.BLUE, Hue.MAGENTA])
        self.lightness_cycle = Cycle([Lightness.DARK, Lightness.NORMAL, Lightness.LIGHT])
