from collections import deque
from typing import Set, List

from picture_program.picture import Picture
from picture_program.pixel import Pixel
from interpreter.directions import BlockChooser
from interpreter.colors import Colors


class Interpreter:
    def __init__(self, picture: Picture):
        self.picture = picture
        self.codel_chooser = BlockChooser()
        self.colors = Colors()
        self.stack : List[int] = []
        self.current_block : Set[Pixel] = set()
        self.current_codel : Pixel = picture[0, 0]

    def get_current_block(self):
        visited = set()
        queue = deque()
        queue.append(self.current_codel)
        while len(queue) != 0:
            current_pixel = queue.popleft()
            visited.add(current_pixel)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x = current_pixel.x + dx
                    y = current_pixel.y + dy
                    if x >= self.picture.width or x < 0 or y >= self.picture.height or y < 0:
                        continue
                    pixel = self.picture[x, y]
                    if pixel in visited or pixel.color != self.current_codel.color:
                        continue
                    queue.append(pixel)
        self.current_block = visited

    def choose_next_block(self):
        i = 0
        k = 0
        self.get_current_block()
        #1. найти самый крайний кодел от текущего кодела по направлению dp в рамках текущего блока
        #2. self.codel_chooser.choose_next_codel()
        #3. пройти по направлению self.codel_chooser.next_codel в рамках текущего блока
        #4. если можно, пройти в следующий блок по направлению dp иначе
        #5. k += 1; если i = 0 изменить cp, i = 1 иначе изменить dp, i = 0
        #6. повторять пункты 1-5, пока не пройдем в следующий блок или пока k < 8
        pass
