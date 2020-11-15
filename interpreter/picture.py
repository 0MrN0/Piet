from PIL import Image
from interpreter.pixel import Pixel
from interpreter.colors import Colors, Color
from typing import List, Tuple


class Picture:
    def __init__(self, picture: List[List[Pixel]]):
        self.picture = picture
        self.width: int = len(self.picture)
        self.height: int = len(self.picture[0])

    def __getitem__(self, cord) -> Pixel:
        return self.picture[cord[0]][cord[1]]

    def __iter__(self) -> Tuple[int, int, Pixel]:
        for i in range(self.width):
            for j in range(self.height):
                yield j, i, self[j, i]

    @classmethod
    def open_picture(cls, file_name: str):
        rows = []
        row = []
        with Image.open(file_name) as pic:
            for i in range(pic.size[0]):
                for j in range(pic.size[1]):
                    rgb = pic.getpixel((i, j))
                    row.append(Pixel(
                        i, j, Color(rgb, Colors[rgb][1], Colors[rgb][0])))
                    if j == pic.size[1] - 1:
                        rows.append(row)
                        row = []
        return cls(rows)
