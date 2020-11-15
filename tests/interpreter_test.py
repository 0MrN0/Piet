from interpreter.interpreter import Interpreter
from interpreter.picture import Picture

import pytest


@pytest.fixture
def interpreter():
    return Interpreter(Picture.open_picture('test_pictures/palette.png'))


@pytest.mark.parametrize(
    ('start_x', 'start_y', 'expected_pixels'), [
        (7, 4, {(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                (7, 4), (7, 3), (7, 2), (7, 1), (7, 0)}),
        (0, 0, {(0, 0)})
    ]
)
def test_set_current_block(interpreter, start_x, start_y, expected_pixels):
    interpreter.current_pixel = interpreter.picture[start_x, start_y]
    interpreter.set_current_block()
    actual_pixels = {(pixel.x, pixel.y)
                     for pixel in interpreter.current_block}
    assert actual_pixels.union(expected_pixels) == expected_pixels


@pytest.mark.parametrize(
    ('start_x', 'start_y', 'dp', 'expected_x_y'), [
        (4, 3, (1, 0), (6, 3)),
        (4, 2, (-1, 0), (0, 2)),
        (4, 3, (0, 1), (4, 4)),
        (4, 3, (0, -1), (4, 0)),
        (0, 0, (1, 0), (0, 0)),
        (0, 0, (-1, 0), (0, 0)),
        (0, 0, (0, -1), (0, 0)),
        (0, 0, (0, 1), (0, 0)),
    ]
)
def test_find_uttermost_by_dp(interpreter,
                              start_x, start_y, dp, expected_x_y):
    interpreter.change_picture(Picture
                               .open_picture('test_pictures/test_1.png'))
    interpreter.current_pixel = interpreter.picture[start_x, start_y]
    interpreter.set_current_block()
    interpreter.dp = dp
    interpreter.find_uttermost_pixel_by_dp()
    assert ((interpreter.current_pixel.x, interpreter.current_pixel.y)
            == expected_x_y)


@pytest.mark.parametrize(
    ('dp', 'cc', 'expected_direction'), [
        ((1, 0), 1, (0, 1)),
        ((1, 0), -1, (0, -1)),
        ((-1, 0), 1, (0, -1)),
        ((-1, 0), -1, (0, 1)),
        ((0, 1), 1, (-1, 0)),
        ((0, 1), -1, (1, 0)),
        ((0, -1), 1, (1, 0)),
        ((0, -1), -1, (-1, 0))
    ]
)
def test_get_corner_direction(interpreter, dp, cc, expected_direction):
    interpreter.dp = dp
    interpreter.cc = cc
    actual_direction = interpreter.get_corner_pixel_direction()
    assert expected_direction == actual_direction


@pytest.mark.parametrize(
    ('start_xy', 'dp', 'cc', 'expected_xy'), [
        ((4, 2), (1, 0), -1, (4, 0)),
        ((4, 2), (1, 0), 1, (4, 4)),
        ((2, 2), (0, 1), -1, (4, 2)),
        ((2, 2), (0, 1), 1, (0, 2)),
        ((4, 0), (0, -1), -1, (3, 0)),
        ((3, 0), (0, -1), 1, (4, 0)),
        ((4, 1), (-1, 0), -1, (4, 4)),
        ((4, 1), (-1, 0), 1, (4, 0)),
    ]
)
def test_find_uttermost_by_cc(interpreter, start_xy, dp, cc, expected_xy):
    interpreter.change_picture(Picture.open_picture('test_pictures/test_1.png'))
    interpreter.current_pixel = interpreter.picture[start_xy[0], start_xy[1]]
    interpreter.set_current_block()
    interpreter.dp = dp
    interpreter.cc = cc
    interpreter.find_uttermost_pixel_by_cc()
    assert (interpreter.current_pixel.x,
            interpreter.current_pixel.y) == expected_xy


def test_push(interpreter):
    interpreter.current_pixel = interpreter.picture[0, 3]
    interpreter.push()
    assert interpreter.stack[0] == 1
    interpreter.set_current_block()
    interpreter.push()
    assert interpreter.stack[1] == 10


def test_pop(interpreter):
    interpreter.pop()
    assert len(interpreter.stack) == 0
    interpreter.push()
    interpreter.push()
    interpreter.pop()
    assert len(interpreter.stack) == 1


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1]),
        ([1, 2], [3]),
        ([1, 2, 3, -3], [1, 2, 0])
    ]
)
def test_add(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.add()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([9], [9]),
        ([1, 2], [-1]),
        ([1, 2, 3, -2, 2], [1, 2, 3, -4]),
    ]
)
def test_subtract(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.subtract()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1]),
        ([1, 2], [2]),
        ([0, 9, 0], [0, 0]),
        ([1, 2, 3, -9, 2], [1, 2, 3, -18])
    ]
)
def test_multiply(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.multiply()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1]),
        ([1, 2, 3, 8, 4], [1, 2, 3, 2]),
        ([1, 2, 3], [1, 0]),
        ([1, 2, 3, 4, -9, 2], [1, 2, 3, 4, -5]),
        ([1, 2, 3, 4, 9, -2], [1, 2, 3, 4, -5])
    ]
)
def test_divide(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.divide()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([-1], [-1]),
        ([1, 2, 3, 7, 2], [1, 2, 3, 1]),
        ([1, -9, 5], [1, 1]),
        ([1, 9, -5], [1, 4])
    ]
)
def test_mod(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.mod()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([4], [0]),
        ([1, 2, 0], [1, 2, 1])
    ]
)
def test_not_operation(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.not_operation()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1]),
        ([1, 2, 3], [1, 0]),
        ([1, 2, 3, 4, 3], [1, 2, 3, 1])
    ]
)
def test_greater(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.greater()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'start_dp', 'expected_dp'), [
        ([], (1, 0), (1, 0)),
        ([2], (1, 0), (-1, 0)),
        ([1, 2, -9], (0, -1), (-1, 0)),
        ([1, 0], (0, 1), (0, 1))
    ]
)
def test_pointer(interpreter, start_stack, start_dp, expected_dp):
    interpreter.stack = list(start_stack)
    interpreter.dp = start_dp
    interpreter.pointer()
    assert interpreter.stack == start_stack[:-1]
    assert interpreter.dp == expected_dp


@pytest.mark.parametrize(
    ('start_stack', 'start_cc', 'expected_cc'), [
        ([], -1, -1),
        ([2], -1, -1),
        ([-3], 1, -1),
        ([3], -1, 1)
    ]
)
def test_switch(interpreter, start_stack, start_cc, expected_cc):
    interpreter.stack = list(start_stack)
    interpreter.cc = start_cc
    interpreter.switch()
    assert interpreter.stack == start_stack[:-1]
    assert interpreter.cc == expected_cc


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1, 1]),
        ([2, 3, -2], [2, 3, -2, -2])
    ]
)
def test_duplicate(interpreter, start_stack, expected_stack):
    interpreter.stack = start_stack
    interpreter.duplicate()
    assert interpreter.stack == expected_stack


@pytest.mark.parametrize(
    ('k', 'start_dp', 'expected_dp'), [
        (-1, (1, 0), (0, -1)),
        (-1, (0, 1), (1, 0)),
        (-1, (-1, 0), (0, 1)),
        (-1, (0, -1), (-1, 0)),
        (1, (1, 0), (0, 1)),
        (1, (0, 1), (-1, 0)),
        (1, (-1, 0), (0, -1)),
        (1, (0, -1), (1, 0))
    ]
)
def test_turn_dp(interpreter, k, start_dp, expected_dp):
    interpreter.dp = start_dp
    interpreter.turn_dp(k)
    assert interpreter.dp == expected_dp
