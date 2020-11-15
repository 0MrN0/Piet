from collections import deque
from typing import Set, List, Tuple

from interpreter.picture import Picture
from interpreter.pixel import Pixel


class Interpreter:
    def __init__(self, picture: Picture):
        # (сдвиг оттенка, сдвиг яркости) : команда
        self.commands = {(0, 0): None, (0, 1): self.push, (0, 2): self.pop,
                         (1, 0): self.add, (1, 1): self.subtract,
                         (1, 2): self.multiply, (2, 0): self.divide,
                         (2, 1): self.mod, (2, 2): self.not_operation,
                         (3, 0): self.greater, (3, 1): self.pointer,
                         (3, 2): self.switch, (4, 0): self.duplicate,
                         (4, 1): self.roll, (4, 2): self.in_int,
                         (5, 0): self.in_char, (5, 1): self.out_int,
                         (5, 2): self.out_char}
        self.picture = picture
        # сдвиг по оси х, сдвиг по оси y: (1, 0), (0, 1), (-1, 0), (0, -1)
        self.dp: Tuple[int, int] = (1, 0)
        # -1 - лево, 1 - право
        self.cc = -1
        self.in_process = True
        self.stack: List[int] = []
        self.current_pixel = picture[0, 0]
        self.current_block: List[Pixel] = []
        self.set_current_block()
        
    def change_picture(self, picture: Picture):
        self.picture = picture

    def set_current_block(self):
        self.current_block.clear()
        visited: Set[(int, int)] = set()
        queue: deque[Pixel] = deque()
        queue.append(self.current_pixel)
        while len(queue) != 0:
            current_pixel = queue.popleft()
            visited.add((current_pixel.x, current_pixel.y))
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 and dy != 0:
                        continue
                    x = current_pixel.x + dx
                    y = current_pixel.y + dy
                    if x >= self.picture.width or x < 0 or y >= self.picture.height or y < 0:
                        continue
                    pixel = self.picture[x, y]
                    if (x, y) in visited or pixel.color != self.current_pixel.color:
                        continue
                    queue.append(pixel)
        for cords in visited:
            self.current_block.append(self.picture[cords[0], cords[1]])

    def find_uttermost_pixel_by_dp(self):
        if self.dp[0] + self.dp[1] == 1:
            changing_cord = 'x' if self.dp[0] == 1 else 'y'
            const_cord = 'y' if self.dp[0] == 1 else 'x'
            edge = -1
            func = int.__gt__
        else:
            changing_cord = 'x' if self.dp[0] == -1 else 'y'
            const_cord = 'y' if self.dp[0] == -1 else 'x'
            edge = self.picture.width + self.picture.height
            func = int.__lt__
        for pixel in self.current_block:
            if (func(pixel.__dict__[changing_cord], edge)
                    and pixel.__dict__[const_cord]
                    == self.current_pixel.__dict__[const_cord]):
                edge = pixel.__dict__[changing_cord]
                self.current_pixel = pixel

    def get_corner_pixel_direction(self) -> Tuple[int, int]:
        if self.dp == (-1, 0):
            return (0, 1) if self.cc == -1 else (0, -1)
        if self.dp == (1, 0):
            return (0, -1) if self.cc == -1 else (0, 1)
        if self.dp == (0, -1):
            return (-1, 0) if self.cc == -1 else (1, 0)
        return (1, 0) if self.cc == -1 else (-1, 0)

    def find_uttermost_pixel_by_cc(self):
        corner_direction: Tuple[int, int] = self.get_corner_pixel_direction()
        while True:
            x = self.current_pixel.x + corner_direction[0]
            y = self.current_pixel.y + corner_direction[1]
            if self.is_correct_cords(x, y) and self.picture[x, y].color == self.current_block[0].color:
                self.current_pixel = self.picture[x, y]
            else:
                break

    def is_correct_cords(self, x: int, y: int) -> bool:
        return (0 <= x < self.picture.width
                and 0 <= y < self.picture.height)

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
        k = 1 if turn_count > 0 else -1
        for i in range(abs(turn_count)):
            self.turn_dp(k)

    def switch(self):
        if len(self.stack) == 0:
            return
        turn_count = self.stack.pop()
        for i in range(abs(turn_count)):
            self.cc *= -1

    def duplicate(self):
        if len(self.stack) == 0:
            return
        self.stack.append(self.stack[len(self.stack) - 1])

    # берем depth последних элементов листа и прокручиваем их с шагом count
    def roll(self):
        if len(self.stack) < 2:
            return
        count = self.stack.pop()
        depth = self.stack.pop()
        if depth < 2:
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
        if len(input_value) > 1:
            return
        self.stack.append(ord(input_value))

    def out_int(self):
        if len(self.stack) == 0:
            return
        print(self.stack.pop(), end='')

    def out_char(self):
        if len(self.stack) == 0:
            return
        try:
            print(chr(self.stack.pop()))
        except ValueError:
            return

    # k = -1 - против часовой стрелки, k = 1 - по часовой
    def turn_dp(self, k: int):
        if self.dp[0] == 0:
            x = self.dp[1] * (-k)
            y = 0
        else:
            x = 0
            y = self.dp[0] * k
        self.dp = (x, y)

    def go_to_next_block(self, next_pixel: Pixel):
        if next_pixel.color.rgb == (255, 255, 255):
            turns_count = 0
            while True:
                if turns_count == 8:
                    self.in_process = False
                    return
                x = next_pixel.x + self.dp[0]
                y = next_pixel.y + self.dp[1]
                if self.is_correct_cords(x, y):
                    next_pixel = self.picture[x, y]
                    if (next_pixel.color.rgb != (255, 255, 255)
                            and next_pixel.color.rgb != (0, 0, 0)):
                        break
                self.turn_dp(1)
                turns_count += 1
        hue_shift = abs(self.current_pixel.color.hue - next_pixel.color.hue)
        lightness_shift = abs(
            self.current_pixel.color.lightness - next_pixel.color.lightness)
        self.commands[hue_shift, lightness_shift]()

    def process_picture(self):
        while True:
            for k in range(8):
                # 1. найти самый крайний пиксель от текущего пикселя по направлению dp в рамках текущего блока
                self.find_uttermost_pixel_by_dp()
                # 2. в зависимости от сс выбрать угловой пиксель
                self.find_uttermost_pixel_by_cc()
                # 4. если можно, пройти в следующий блок по направлению dp и выйти из цикла иначе
                x = self.current_pixel.x + self.dp[0]
                y = self.current_pixel.y + self.dp[1]
                if (self.is_correct_cords(x, y)
                        and self.picture[x, y].color.rgb != (0, 0, 0)):
                    next_pixel = self.picture[x, y]
                    self.go_to_next_block(next_pixel)
                    break
                # 5. если k % 2 == 0 изменить cc, иначе изменить dp;
                elif k % 2 == 0:
                    self.cc *= -1
                else:
                    self.turn_dp(1)
