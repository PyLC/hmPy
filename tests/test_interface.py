import pytest
from hmpy import Interface


@pytest.fixture(scope="module")
def interface():
    return Interface()


def test_multiple_instances(interface):
    # Test trying to create multiple instances of class Interface
    with pytest.raises(Exception):
        int2 = Interface()


def test_after(interface, qtbot, mocker):
    # Test that the .after method executes the action only once,
    # and after the expected delay
    action = mocker.stub()
    interface.after(10, action)
    action.assert_not_called()
    qtbot.wait(25)
    action.assert_called_once()


def test_every(interface, qtbot, mocker):
    # Test that the .every method executes the action at the expected interval
    action = mocker.stub()
    interface.every(100, action)
    action.assert_not_called()
    qtbot.wait(250)
    assert action.call_count == 2
