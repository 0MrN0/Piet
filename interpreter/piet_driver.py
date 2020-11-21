from typing import Set, List, Tuple
from enum import Enum, IntEnum

from interpreter.colors import Hue
from interpreter.picture import Picture, Pixel


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


class PietDriver:
    def __init__(self, picture: Picture):
        # (сдвиг оттенка, сдвиг яркости) : команда
        self.commands = {(0, 0): self.no_action, (0, 1): self.push,
                         (0, 2): self.pop, (1, 0): self.add,
                         (1, 1): self.subtract, (1, 2): self.multiply,
                         (2, 0): self.divide, (2, 1): self.mod,
                         (2, 2): self.not_operation, (3, 0): self.greater,
                         (3, 1): self.pointer, (3, 2): self.switch,
                         (4, 0): self.duplicate, (4, 1): self.roll,
                         (4, 2): self.in_int, (5, 0): self.in_char,
                         (5, 1): self.out_int, (5, 2): self.out_char}
        self.picture: Picture = picture
        self.dp: Direction = Direction.RIGHT
        self.cc: CC = CC.LEFT
        self.stack: List[int] = []
        self.current_pixel: Pixel = self.picture[0, 0]
        self.current_block: Set[Tuple[int, int]] = set()

    def change_picture(self, picture: Picture):
        self.picture = picture

    def no_action(self):
        return

    def push(self):
        self.stack.append(len(self.current_block))

    def pop(self):
        if len(self.stack) == 0:
            return
        self.stack.pop()

    def add(self):
        self._calculate(int.__add__, -1)

    def subtract(self):
        self._calculate(int.__sub__, -1)

    def multiply(self):
        self._calculate(int.__mul__, -1)

    def divide(self):
        self._calculate(int.__divmod__, 0)

    def mod(self):
        self._calculate(int.__divmod__, 1)

    def _calculate(self, operation: callable, index: int):
        if len(self.stack) < 2:
            return
        a = self.stack.pop()
        b = self.stack.pop()
        if index != -1:
            a = abs(a) if index == 1 else a
            self.stack.append(operation(b, a)[index])
            return
        self.stack.append(operation(b, a))

    def not_operation(self):
        if len(self.stack) == 0:
            return
        old_value = self.stack.pop()
        self.stack.append(1 if old_value == 0 else 0)

    def greater(self):
        if len(self.stack) < 2:
            return
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(1 if b > a else 0)

    def pointer(self):
        if len(self.stack) == 0:
            return
        turn_count = self.stack.pop()
        for i in range(abs(turn_count)):
            self.dp = self.dp.next(turn_count > 0)

    def switch(self):
        if len(self.stack) == 0:
            return
        turn_count = self.stack.pop()
        for i in range(abs(turn_count)):
            self.cc = self.cc.next()

    def duplicate(self):
        if len(self.stack) == 0:
            return
        self.stack.append(self.stack[len(self.stack) - 1])

    # берем depth последних элементов листа и прокручиваем их
    # с шагом count, -count - влево, +count - вправо
    def roll(self):
        if len(self.stack) < 2 or self.stack[-2] < 0:
            return
        count = self.stack.pop()
        depth = self.stack.pop()
        if depth == 1:
            return
        count %= depth
        _ = -abs(count) + depth * (count < 0)
        self.stack[-depth:] = self.stack[_:] + self.stack[-depth:_]

    def in_int(self):
        input_value = input()
        try:
            self.stack.append(int(input_value))
        except ValueError:
            return

    def in_char(self):
        input_value = input()
        try:
            if len(input_value) > 1:
                return
            self.stack.append(ord(input_value))
        except TypeError:
            return
        except ValueError:
            return

    def out_int(self):
        if len(self.stack) == 0:
            return
        print(self.stack.pop(), end='')

    def out_char(self):
        if len(self.stack) == 0:
            return
        try:
            print(chr(self.stack.pop()), end='')
        except ValueError:
            return

    def set_current_block(self):
        self.current_block.clear()
        visited: Set[(int, int)] = set()
        stack: List[Pixel] = [self.current_pixel]
        while len(stack) != 0:
            current_pixel = stack.pop()
            visited.add((current_pixel.x, current_pixel.y))
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 and dy != 0:
                        continue
                    x = current_pixel.x + dx
                    y = current_pixel.y + dy
                    if (x >= self.picture.width or x < 0
                            or y >= self.picture.height or y < 0):
                        continue
                    pixel = self.picture[x, y]
                    if ((x, y) in visited
                            or pixel.color != self.current_pixel.color):
                        continue
                    stack.append(pixel)
        self.current_block = visited

    def find_uttermost_pixel_by_dp(self):
        if self.dp.value[0] + self.dp.value[1] == 1:
            changing_cord = 'x' if self.dp.value[0] == 1 else 'y'
            const_cord = 'y' if self.dp.value[0] == 1 else 'x'
            edge = -1
            compare_func = int.__lt__
        else:
            changing_cord = 'x' if self.dp.value[0] == -1 else 'y'
            const_cord = 'y' if self.dp.value[0] == -1 else 'x'
            edge = self.picture.width + self.picture.height
            compare_func = int.__gt__
        for x, y in self.current_block:
            pixel = self.picture[x, y]
            if compare_func(getattr(pixel, changing_cord), edge):
                continue
            if (getattr(pixel, const_cord)
                    != getattr(self.current_pixel, const_cord)):
                continue
            edge = getattr(pixel, changing_cord)
            self.current_pixel = pixel

    def get_corner_pixel_direction(self) -> Direction:
        if self.dp == Direction.LEFT:
            return Direction.DOWN if self.cc == CC.LEFT else Direction.UP
        if self.dp == Direction.RIGHT:
            return Direction.UP if self.cc == CC.LEFT else Direction.DOWN
        if self.dp == Direction.UP:
            return Direction.LEFT if self.cc == CC.LEFT else Direction.RIGHT
        return Direction.RIGHT if self.cc == CC.LEFT else Direction.LEFT

    def find_uttermost_pixel_by_cc(self):
        corner_direction: Direction = self.get_corner_pixel_direction()
        while True:
            x = self.current_pixel.x + corner_direction.value[0]
            y = self.current_pixel.y + corner_direction.value[1]
            if not (self.is_correct_coords(x, y)
                    and self.picture[x, y].color
                    == self.current_pixel.color):
                break
            self.current_pixel = self.picture[x, y]

    def is_correct_coords(self, x: int, y: int) -> bool:
        return (0 <= x < self.picture.width
                and 0 <= y < self.picture.height
                and self.picture[x, y].color.hue != Hue.BLACK)

    def go_to_next_block(self, next_x: int, next_y: int) -> bool:
        next_pixel = self.picture[next_x, next_y]
        if next_pixel.color.rgb == (255, 255, 255):
            k = 0
            while True:
                x = next_pixel.x + self.dp.value[0]
                y = next_pixel.y + self.dp.value[1]
                if not self.is_correct_coords(x, y):
                    k += 1
                    self.dp = self.dp.next()
                    if k == 4:
                        return False
                else:
                    next_pixel = self.picture[x, y]
                    if next_pixel.color.rgb != (255, 255, 255):
                        self.current_pixel = next_pixel
                        return True
        hue_shift = (6 - self.current_pixel.color.hue
                     + next_pixel.color.hue) % 6
        lightness_shift = (3 - self.current_pixel.color.lightness
                           + next_pixel.color.lightness) % 3
        self.commands[hue_shift, lightness_shift]()
        self.current_pixel = next_pixel
        return True

    def process_picture(self):
        k = 0
        while k < 8:
            self.set_current_block()
            self.find_uttermost_pixel_by_dp()
            self.find_uttermost_pixel_by_cc()
            x = self.current_pixel.x + self.dp.value[0]
            y = self.current_pixel.y + self.dp.value[1]
            if not self.is_correct_coords(x, y):
                if k % 2 == 0:
                    self.cc = self.cc.next()
                else:
                    self.dp = self.dp.next()
                k += 1
            else:
                k = 0
                do_next_iteration = self.go_to_next_block(x, y)
                if not do_next_iteration:
                    break
