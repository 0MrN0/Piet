from interpreter.interpreter import Interpreter
from picture_program.picture import Picture


inter = Interpreter(Picture.open_picture('palitra.png'))
inter.current_codel = inter.picture[3, 4]
inter.get_current_block()
for pix in inter.current_block:
    print(pix, end=' | ')
