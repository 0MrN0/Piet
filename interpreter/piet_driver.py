from typing import Set, List, Tuple

from interpreter.colors import Hue
from interpreter.picture import Picture, Pixel
from interpreter.directions import Direction, CodelChooser
from interpreter.commands import (BaseCommand, Push, Pop, Duplicate,
                                  InChar, InInt, OutInt, Pointer,
                                  OutChar, Switch, Roll, Not,
                                  Greater, Add, Subtract, Multiply,
                                  Mod, Divide)


class StepByStepExecutor:
    def __init__(self, driver: 'PietDriver'):
        self.driver = driver

    def continue_execution(self):
        self.driver.error_stream.write('Для продолжения нажмите enter\n')
        while True:
            char = self.driver.in_stream.read(1)
            if char == '\n':
                break

    def show_current_step(self):
        self.driver.error_stream.write(f'текущая команда'
                                       f':\n{self.driver.current_command}\n'
                                       f'стэк: {self.driver.stack}\n'
                                       f'текущий пиксель'
                                       f': {self.driver.current_pixel}\n')


class PietDriver:
    def __init__(self, picture: Picture, step_by_step: bool,
                 in_stream, out_stream, error_stream):
        # (сдвиг оттенка, сдвиг яркости) : команда
        self.commands = {(0, 0): BaseCommand, (0, 1): Push,
                         (0, 2): Pop, (1, 0): Add,
                         (1, 1): Subtract, (1, 2): Multiply,
                         (2, 0): Divide, (2, 1): Mod,
                         (2, 2): Not, (3, 0): Greater,
                         (3, 1): Pointer, (3, 2): Switch,
                         (4, 0): Duplicate, (4, 1): Roll,
                         (4, 2): InInt, (5, 0): InChar,
                         (5, 1): OutInt, (5, 2): OutChar}
        self.picture: Picture = picture
        self.step_by_step = StepByStepExecutor(self) if step_by_step else None
        self.error_stream = error_stream
        self.in_stream = in_stream
        self.out_stream = out_stream
        self.dp: Direction = Direction.RIGHT
        self.cc: CodelChooser = CodelChooser.LEFT
        self.stack: List[int] = []
        self.current_command = BaseCommand()
        self.current_pixel: Pixel = self.picture[0, 0]
        self.current_block: Set[Tuple[int, int]] = set()

    def change_picture(self, picture: Picture):
        self.picture = picture

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
            return Direction.DOWN \
                if self.cc == CodelChooser.LEFT else Direction.UP
        if self.dp == Direction.RIGHT:
            return Direction.UP \
                if self.cc == CodelChooser.LEFT else Direction.DOWN
        if self.dp == Direction.UP:
            return Direction.LEFT \
                if self.cc == CodelChooser.LEFT else Direction.RIGHT
        return Direction.RIGHT \
            if self.cc == CodelChooser.LEFT else Direction.LEFT

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

    def set_current_command(self, hue_shift: int, lightness_shift: int):
        if (self.current_command is InInt
                or self.current_command is InChar):
            self.current_command = self.commands[hue_shift, lightness_shift](
                self.in_stream, self.error_stream)
        elif (self.current_command is OutInt
              or self.current_command is OutChar):
            self.current_command = self.commands[hue_shift, lightness_shift](
                self.out_stream, self.error_stream)
        else:
            self.current_command = self.commands[hue_shift, lightness_shift]()

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
        self.current_command = self.commands[hue_shift, lightness_shift]
        self.set_current_command(hue_shift, lightness_shift)
        if isinstance(self.current_command, Switch):
            self.cc = self.current_command(self.stack,
                                           len(self.current_block),
                                           self.dp, self.cc)
        elif isinstance(self.current_command, Pointer):
            self.dp = self.current_command(self.stack,
                                           len(self.current_block),
                                           self.dp, self.cc)
        else:
            self.current_command(self.stack, len(self.current_block),
                                 self.dp, self.cc)
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
                    self.step_by_step.show_current_step()
                    self.step_by_step.continue_execution()
                if not do_next_iteration:
                    break
