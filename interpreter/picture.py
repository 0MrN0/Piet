from PIL import Image
from typing import List, Tuple
from dataclasses import dataclass

from interpreter.colors import Color


@dataclass(frozen=True, repr=True)
class Pixel:
    x: int
    y: int
    color: Color


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
        with Image.open(file_name) as pic:
            rows = [[Pixel(i, j, Color(pic.getpixel((i, j))))
                     for j in range(pic.size[1])]
                    for i in range(pic.size[0])]
        return cls(rows)
