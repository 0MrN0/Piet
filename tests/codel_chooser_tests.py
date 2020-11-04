from interpreter.directions import BlockChooser, Directions
import pytest


@pytest.fixture()
def codel_chooser():
    return BlockChooser()


def test_choose_next_codel(codel_chooser):
    codel_chooser.change_cc()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.DOWN

    codel_chooser.change_dp()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.LEFT

    codel_chooser.change_cc()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.RIGHT

    codel_chooser.change_dp()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.DOWN

    codel_chooser.change_cc()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.UP

    codel_chooser.change_dp()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.RIGHT

    codel_chooser.change_cc()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.LEFT

    codel_chooser.change_dp()
    codel_chooser.choose_next_codel()
    assert codel_chooser.next_codel == Directions.UP


def test_change_cc(codel_chooser):
    codel_chooser.change_cc()
    assert codel_chooser.cc == Directions.RIGHT
    codel_chooser.change_cc()
    assert codel_chooser.cc == Directions.LEFT


def test_change_dp(codel_chooser):
    codel_chooser.change_dp()
    assert codel_chooser.dp == Directions.DOWN
    codel_chooser.change_dp()
    assert codel_chooser.dp == Directions.LEFT
    codel_chooser.change_dp()
    assert codel_chooser.dp == Directions.UP
    codel_chooser.change_dp()
    assert codel_chooser.dp == Directions.RIGHT
