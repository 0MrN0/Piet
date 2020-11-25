from interpreter.piet_driver import PietDriver, CC, Direction
from interpreter.picture import Picture

import pytest
import unittest.mock


@pytest.fixture
def driver():
    return PietDriver(Picture.open_picture('tests/test_pictures/palette.png'), False)


def test_push(driver):
    driver.set_current_block()
    driver.push()
    assert driver.stack[0] == 1
    driver.current_pixel = driver.picture[0, 3]
    driver.set_current_block()
    driver.push()
    assert driver.stack[1] == 10


def test_pop(driver):
    driver.pop()
    assert len(driver.stack) == 0
    driver.push()
    driver.push()
    driver.pop()
    assert len(driver.stack) == 1


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1]),
        ([1, 2], [3]),
        ([1, 2, 3, -3], [1, 2, 0])
    ]
)
def test_add(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.add()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([9], [9]),
        ([1, 2], [-1]),
        ([1, 2, 3, -2, 2], [1, 2, 3, -4]),
    ]
)
def test_subtract(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.subtract()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1]),
        ([1, 2], [2]),
        ([0, 9, 0], [0, 0]),
        ([1, 2, 3, -9, 2], [1, 2, 3, -18])
    ]
)
def test_multiply(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.multiply()
    assert driver.stack == expected_stack


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
def test_divide(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.divide()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([-1], [-1]),
        ([1, 2, 3, 7, 2], [1, 2, 3, 1]),
        ([1, -9, 5], [1, 1]),
        ([1, 9, -5], [1, 4])
    ]
)
def test_mod(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.mod()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([4], [0]),
        ([1, 2, 0], [1, 2, 1])
    ]
)
def test_not_operation(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.not_operation()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1]),
        ([1, 2, 3], [1, 0]),
        ([1, 2, 3, 4, 3], [1, 2, 3, 1])
    ]
)
def test_greater(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.greater()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'start_dp', 'expected_dp'), [
        ([], Direction.RIGHT, Direction.RIGHT),
        ([2], Direction.RIGHT, Direction.LEFT),
        ([1, 2, -9], Direction.UP, Direction.LEFT),
        ([1, 0], Direction.DOWN, Direction.DOWN)
    ]
)
def test_pointer(driver, start_stack, start_dp, expected_dp):
    driver.stack = list(start_stack)
    driver.dp = start_dp
    driver.pointer()
    assert driver.stack == start_stack[:-1]
    assert driver.dp == expected_dp


@pytest.mark.parametrize(
    ('start_stack', 'start_cc', 'expected_cc'), [
        ([], CC.LEFT, CC.LEFT),
        ([2], CC.LEFT, CC.LEFT),
        ([-3], CC.RIGHT, CC.LEFT),
        ([3], CC.LEFT, CC.RIGHT)
    ]
)
def test_switch(driver, start_stack, start_cc, expected_cc):
    driver.stack = list(start_stack)
    driver.cc = start_cc
    driver.switch()
    assert driver.stack == start_stack[:-1]
    assert driver.cc == expected_cc


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1], [1, 1]),
        ([2, 3, -2], [2, 3, -2, -2])
    ]
)
def test_duplicate(driver, start_stack, expected_stack):
    driver.stack = start_stack
    driver.duplicate()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([1, 2, 3, -4, 2], [1, 2, 3, -4, 2]),
        ([1, 2, 3, 1, 2], [1, 2, 3]),
        ([1, 2, 3, 4, 5, 2, 1], [1, 2, 3, 5, 4]),
        ([1, 2, 3, 4, 5, 3, 1], [1, 2, 5, 3, 4]),
        ([1, 2, 3, 4, 5, 3, -1], [1, 2, 4, 5, 3]),
        ([1, 2, 3, 5, 1], [3, 1, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 4, -10], [1, 2, 3, 6, 7, 4, 5])
    ]
)
def test_roll(driver, start_stack, expected_stack):
    driver.stack = list(start_stack)
    driver.roll()
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('in_value', 'expected_stack'), [
        (25, [25]),
        ('a', []),
        ('lsdlsdfl', []),
        (0.67, [0])
    ]
)
def test_in_int(driver, in_value, expected_stack):
    with unittest.mock.patch('builtins.input', return_value=in_value):
        driver.in_int()
        assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('in_value', 'expected_stack'), [
        ('a', [97]),
        ('abc', []),
        (5, [])
    ]
)
def test_in_char(driver, in_value, expected_stack):
    with unittest.mock.patch('builtins.input', return_value=in_value):
        driver.in_char()
    assert driver.stack == expected_stack
