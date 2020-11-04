from enum import IntEnum


class Directions(IntEnum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class BlockChooser():
    def __init__(self):
        self.dp = Directions.RIGHT
        self.cc = Directions.LEFT
        self.next_codel = Directions.UP

    def choose_next_codel(self):
        if self.dp == Directions.RIGHT or self.dp == Directions.LEFT:
            self.next_codel = Directions.UP if self.cc != self.dp \
                else Directions.DOWN
        elif self.dp == Directions.UP:
            self.next_codel = Directions.LEFT if self.cc == Directions.LEFT \
                else Directions.RIGHT
        else:
            self.next_codel = Directions.RIGHT if self.cc == Directions.LEFT \
                else Directions.LEFT

    def change_cc(self):
        self.cc = Directions.LEFT if self.cc == Directions.RIGHT else Directions.RIGHT

    def change_dp(self):
        if self.dp == Directions.LEFT:
            self.dp = Directions.UP
        else:
            self.dp += 1
