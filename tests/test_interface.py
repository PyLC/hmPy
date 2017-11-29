import pytest
from hmpy import Interface


@pytest.fixture(scope="module")
def interface():
    return Interface()


def test_multiple_instances(interface):
    # Test trying to create multiple instances of class Interface
    with pytest.raises(Exception):
        int2 = Interface()


def test_after(interface, qtbot, mock):
    # Test that the .after method executes the action only once,
    # and after the expected delay
    interface.after(10, mock)
    mock.assert_not_called()
    qtbot.wait(25)
    mock.assert_called_once()


def test_every(interface, qtbot, mock):
    # Test that the .every method executes the action at the expected interval
    interface.every(10, mock)
    mock.assert_not_called()
    qtbot.wait(100)
    mock.assert_called_around(10)
