from collections import deque
from typing import Set, List, Tuple

from interpreter.picture import Picture
from interpreter.pixel import Pixel
from interpreter.colors import Colors


class Interpreter:
    def __init__(self, picture: Picture):
        self.picture = picture
        self.colors = Colors()
        self.dp: Tuple[int, int] = (1, 0)
        self.cc: int = -1
        self.stack: List[int] = []
        self.current_pixel: Pixel = picture[0, 0]
        self.current_block: Set[Pixel] = set()
        self.set_current_block()

    def set_current_block(self):
        self.current_block.clear()
        visited: Set[Pixel] = set()
        queue: deque[Pixel] = deque()
        queue.append(self.current_pixel)
        while len(queue) != 0:
            current_pixel: Pixel = queue.popleft()
            visited.add(current_pixel)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 and dy != 0:
                        continue
                    x: int = current_pixel.x + dx
                    y: int = current_pixel.y + dy
                    if x >= self.picture.width or x < 0 or y >= self.picture.height or y < 0:
                        continue
                    pixel: Pixel = self.picture[x, y]
                    if pixel in visited or pixel.color != self.current_pixel.color:
                        continue
                    queue.append(pixel)
        self.current_block = visited

    def find_uttermost_pixel_by_dp(self):
        if self.dp[0] + self.dp[1] == 1:
            changing_cord: str = 'x' if self.dp[0] == 1 else 'y'
            const_cord: str = 'y' if self.dp[0] == 1 else 'x'
            edge: int = -1
            func = int.__gt__
        else:
            changing_cord: str = 'x' if self.dp[0] == -1 else 'y'
            const_cord: str = 'y' if self.dp[0] == -1 else 'x'
            edge: int = self.picture.width + self.picture.height
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
            x: int = self.current_pixel.x + corner_direction[0]
            y: int = self.current_pixel.y + corner_direction[1]
            if self.is_correct_cords(x, y) and self.picture[x, y] in self.current_block:
                self.current_pixel = self.picture[x, y]
            else:
                break

    def is_correct_cords(self, x: int, y: int) -> bool:
        return (0 <= x < self.picture.width
                and 0 <= y < self.picture.height)

    def choose_next_block(self) -> bool:
        for k in range(8):
            self.find_uttermost_pixel_by_dp()#1. найти самый крайний пиксель от текущего пикселя по направлению dp в рамках текущего блока
            self.find_uttermost_pixel_by_cc()#2. в зависимости от сс выбрать угловой пиксель
            #4. если можно, пройти в следующий блок по направлению dp и выйти из цикла иначе
            #5. если k % 2 == 0 изменить cc, иначе изменить dp;
        return False
