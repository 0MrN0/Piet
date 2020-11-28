from interpreter.picture import Picture
from interpreter.piet_driver import PietDriver
from interpreter.directions import CodelChooser, Direction
from interpreter.commands import (Push, Pop, Duplicate,
                                  Pointer, Switch, Roll, Not,
                                  Greater, Add, Subtract, Multiply,
                                  Mod, Divide)

import sys
import pytest


@pytest.fixture
def driver():
    return PietDriver(
        Picture.open_picture('tests/test_pictures/palette.png'),
        False, sys.stdin, sys.stdout, sys.stderr)


def test_push(driver):
    driver.set_current_block()
    driver.current_command = Push()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
    assert driver.stack[0] == 1
    driver.current_pixel = driver.picture[0, 3]
    driver.set_current_block()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
    assert driver.stack[1] == 10


def test_pop(driver):
    driver.current_command = Pop()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
    assert len(driver.stack) == 0
    driver.current_command = Push()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
    driver.current_command = Pop()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.current_command = Add()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.stack = list(start_stack)
    driver.current_command = Subtract()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.stack = list(start_stack)
    driver.current_command = Multiply()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.stack = list(start_stack)
    driver.current_command = Divide()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.stack = list(start_stack)
    driver.current_command = Mod()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
    assert driver.stack == expected_stack


@pytest.mark.parametrize(
    ('start_stack', 'expected_stack'), [
        ([], []),
        ([4], [0]),
        ([1, 2, 0], [1, 2, 1])
    ]
)
def test_not(driver, start_stack, expected_stack):
    driver.stack = list(start_stack)
    driver.current_command = Not()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.stack = list(start_stack)
    driver.current_command = Greater()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.current_command = Pointer()
    driver.dp = driver.current_command(
        driver.stack, len(driver.current_block), driver.dp, driver.cc)
    assert driver.stack == start_stack[:-1]
    assert driver.dp == expected_dp


@pytest.mark.parametrize(
    ('start_stack', 'start_cc', 'expected_cc'), [
        ([], CodelChooser.LEFT, CodelChooser.LEFT),
        ([2], CodelChooser.LEFT, CodelChooser.LEFT),
        ([-3], CodelChooser.RIGHT, CodelChooser.LEFT),
        ([3], CodelChooser.LEFT, CodelChooser.RIGHT)
    ]
)
def test_switch(driver, start_stack, start_cc, expected_cc):
    driver.stack = list(start_stack)
    driver.cc = start_cc
    driver.current_command = Switch()
    driver.cc = driver.current_command(
        driver.stack, len(driver.current_block), driver.dp, driver.cc)
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
    driver.stack = list(start_stack)
    driver.current_command = Duplicate()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
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
    driver.current_command = Roll()
    driver.current_command(driver.stack,
                           len(driver.current_block), driver.dp, driver.cc)
    assert driver.stack == expected_stack
