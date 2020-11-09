from PIL import Image
from picture_program.pixel import Pixel
from typing import List


class Picture:
    def __init__(self, picture: List[List[Pixel]]):
        self.picture = picture
        self.width = len(self.picture)
        self.height = len(self.picture[0])

    def __getitem__(self, cord):
        return self.picture[cord[0]][cord[1]]

    def __iter__(self):
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
                    row.append(Pixel(i, j, pic.getpixel((i, j))))
                    if j == pic.size[1] - 1:
                        rows.append(row)
                        row = []
        return cls(rows)
