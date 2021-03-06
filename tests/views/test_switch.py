import pytest
from hmpy.views.switch import SwitchView
from PyQt5.QtCore import Qt


def test_on_init(qtbot):
    # Test that the value is initialized properly
    switch = SwitchView("test", False)
    assert not switch.on


def test_on_set(qtbot):
    # Test that the value is set properly
    switch = SwitchView("test")
    switch.on = True
    assert switch.on is True


def test_toggle(qtbot):
    # Test that the switch on state toggles properly
    switch = SwitchView("test", on=False)
    # toggle on
    switch.toggle()
    assert switch.on is True
    switch.toggle()
    assert switch.on is False


def test_on_set_toggle(qtbot, mocker):
    mock = mocker.stub()
    switch = SwitchView("test", on=False)
    switch.on_toggle(mock)

    switch.on = True

    mock.assert_called_once()


def test_on_toggle(qtbot, mocker):
    mock = mocker.stub()
    switch = SwitchView("test")
    switch.on_toggle(mock)

    qtbot.addWidget(switch)
    qtbot.mouseClick(switch._button, Qt.LeftButton)

    mock.assert_called_once()
