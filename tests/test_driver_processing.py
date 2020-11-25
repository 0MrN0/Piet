from interpreter.piet_driver import PietDriver, CC, Direction
from interpreter.picture import Picture

import pytest
import unittest.mock


@pytest.fixture
def driver():
    return PietDriver(Picture.open_picture('tests/test_pictures/palette.png'), False)


@pytest.mark.parametrize(
    ('start_x', 'start_y', 'expected_pixels'), [
        (7, 4, {(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                (7, 4), (7, 3), (7, 2), (7, 1), (7, 0)}),
        (0, 0, {(0, 0)})
    ]
)
def test_set_current_block(driver, start_x, start_y, expected_pixels):
    driver.current_pixel = driver.picture[start_x, start_y]
    driver.set_current_block()
    assert driver.current_block.union(expected_pixels) == expected_pixels


@pytest.mark.parametrize(
    ('start_x', 'start_y', 'dp', 'expected_x_y'), [
        (4, 3, Direction.RIGHT, (6, 3)),
        (4, 2, Direction.LEFT, (0, 2)),
        (4, 3, Direction.DOWN, (4, 4)),
        (4, 3, Direction.UP, (4, 0)),
        (0, 0, Direction.DOWN, (0, 0)),
        (0, 0, Direction.LEFT, (0, 0)),
        (0, 0, Direction.UP, (0, 0)),
        (0, 0, Direction.RIGHT, (0, 0)),
    ]
)
def test_find_uttermost_by_dp(driver,
                              start_x, start_y, dp, expected_x_y):
    driver.change_picture(Picture
                          .open_picture('tests/test_pictures/test_1.png'))
    driver.current_pixel = driver.picture[start_x, start_y]
    driver.set_current_block()
    driver.dp = dp
    driver.find_uttermost_pixel_by_dp()
    assert ((driver.current_pixel.x, driver.current_pixel.y)
            == expected_x_y)


@pytest.mark.parametrize(
    ('dp', 'cc', 'expected_direction'), [
        (Direction.RIGHT, CC.RIGHT, Direction.DOWN),
        (Direction.RIGHT, CC.LEFT, Direction.UP),
        (Direction.LEFT, CC.RIGHT, Direction.UP),
        (Direction.LEFT, CC.LEFT, Direction.DOWN),
        (Direction.DOWN, CC.RIGHT, Direction.LEFT),
        (Direction.DOWN, CC.LEFT, Direction.RIGHT),
        (Direction.UP, CC.RIGHT, Direction.RIGHT),
        (Direction.UP, CC.LEFT, Direction.LEFT)
    ]
)
def test_get_corner_direction(driver, dp, cc, expected_direction):
    driver.dp = dp
    driver.cc = cc
    actual_direction = driver.get_corner_pixel_direction()
    assert expected_direction == actual_direction


def test_process_picture(driver):
    driver.change_picture(
        Picture.open_picture('tests/test_pictures/comparsion_int.png'))
    with unittest.mock.patch('builtins.input', return_value=5):
        driver.process_picture()


@pytest.mark.parametrize(
    ('start_xy', 'dp', 'cc', 'expected_xy'), [
        ((4, 2), Direction.RIGHT, CC.LEFT, (4, 0)),
        ((4, 2), Direction.RIGHT, CC.RIGHT, (4, 4)),
        ((2, 2), Direction.DOWN, CC.LEFT, (4, 2)),
        ((2, 2), Direction.DOWN, CC.RIGHT, (0, 2)),
        ((4, 0), Direction.UP, CC.LEFT, (3, 0)),
        ((3, 0), Direction.UP, CC.RIGHT, (4, 0)),
        ((4, 1), Direction.LEFT, CC.LEFT, (4, 4)),
        ((4, 1), Direction.LEFT, CC.RIGHT, (4, 0)),
    ]
)
def test_find_uttermost_by_cc(driver, start_xy, dp, cc, expected_xy):
    driver.change_picture(Picture
                          .open_picture('tests/test_pictures/test_1.png'))
    driver.current_pixel = driver.picture[start_xy[0], start_xy[1]]
    driver.set_current_block()
    driver.dp = dp
    driver.cc = cc
    driver.find_uttermost_pixel_by_cc()
    assert (driver.current_pixel.x,
            driver.current_pixel.y) == expected_xy
