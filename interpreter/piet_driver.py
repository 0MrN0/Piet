from typing import Set, List, Tuple

from interpreter.colors import Hue
from interpreter.picture import Picture, Pixel
from interpreter.directions import Direction, CC
from interpreter.commands import (BaseCommand, Push, Pop, Calculate,
                                  Duplicate, InChar, InInt, OutInt,
                                  OutChar, Pointer, Switch, Roll, Not,
                                  Greater)


class PietDriver:
    def __init__(self, picture: Picture, step_by_step: bool):
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
        self.step_by_step = step_by_step
        self.dp: Direction = Direction.RIGHT
        self.cc: CC = CC.LEFT
        self.stack: List[int] = []
        self.current_command = BaseCommand(self.stack)
        self.current_pixel: Pixel = self.picture[0, 0]
        self.current_block: Set[Tuple[int, int]] = set()

    def change_picture(self, picture: Picture):
        self.picture = picture

    def no_action(self):
        self.current_command = BaseCommand(self.stack)
        self.current_command()

    def push(self):
        self.current_command = Push(self.stack, len(self.current_block))
        self.current_command()

    def pop(self):
        self.current_command = Pop(self.stack)
        self.current_command()

    def add(self):
        self.current_command = Calculate(self.stack, 'add', int.__add__, -1)
        self.current_command()

    def subtract(self):
        self.current_command = Calculate(self.stack,
                                         'subtract', int.__sub__, -1)
        self.current_command()

    def multiply(self):
        self.current_command = Calculate(self.stack,
                                         'multiply', int.__mul__, -1)
        self.current_command()

    def divide(self):
        self.current_command = Calculate(self.stack,
                                         'divide', int.__divmod__, 0)
        self.current_command()

    def mod(self):
        self.current_command = Calculate(self.stack, 'mod', int.__divmod__, 1)
        self.current_command()

    def not_operation(self):
        self.current_command = Not(self.stack)
        self.current_command()

    def greater(self):
        self.current_command = Greater(self.stack)
        self.current_command()

    def pointer(self):
        self.current_command = Pointer(self.stack, self.dp)
        self.current_command()
        self.dp = self.current_command.dp

    def switch(self):
        self.current_command = Switch(self.stack, self.cc)
        self.current_command()
        self.cc = self.current_command.cc

    def duplicate(self):
        self.current_command = Duplicate(self.stack)
        self.current_command()

    def roll(self):
        self.current_command = Roll(self.stack)
        self.current_command()

    def in_int(self):
        self.current_command = InInt(self.stack, self.step_by_step)
        self.current_command()

    def in_char(self):
        self.current_command = InChar(self.stack, self.step_by_step)
        self.current_command()

    def out_int(self):
        self.current_command = OutInt(self.stack, self.step_by_step)
        self.current_command()

    def out_char(self):
        self.current_command = OutChar(self.stack, self.step_by_step)
        self.current_command()

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
                if do_next_iteration and self.step_by_step:
                    print(f'текущая команда:\n{self.current_command}\n'
                          f'стэк: {self.stack}\n'
                          f'текущий пиксель: {self.current_pixel}\n'
                          'для продолжения нажмите enter\n')
                    input()
                if not do_next_iteration:
                    break
