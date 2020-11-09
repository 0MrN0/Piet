from interpreter.interpreter import Interpreter
from interpreter.picture import Picture


interp = Interpreter(Picture.open_picture('test_1.png'))
interp.current_pixel = interp.picture[4, 3]
interp.dp = (-1, 0)
interp.find_uttermost_pixel_by_dp()
print(interp.current_pixel)
interp.find_uttermost_pixel_by_cc()
print(interp.current_pixel)
