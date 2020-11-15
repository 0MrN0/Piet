from interpreter.colors import Color


class Pixel:
    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return f'x: {self.x} y: {self.y} color: {self.color}'
