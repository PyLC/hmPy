import pytest
from hmpy.views.switch import SwitchView
from PyQt5.QtCore import Qt


def test_on_init(qtbot):
    # Test that the value is initialized properly
    switch = SwitchView(False)
    qtbot.addWidget(switch)
    assert not switch.on


def test_on_set(qtbot):
    # Test that the value is set properly
    switch = SwitchView()
    switch.on = True
    qtbot.addWidget(switch)
    assert switch.on is True


def test_toggle(qtbot):
    # Test that the switch on state toggles properly
    switch = SwitchView(False)
    # toggle on
    switch.toggle()
    qtbot.addWidget(switch)
    assert switch.on is True
    switch.toggle()
    assert switch.on is False


def test_on_toggle(qtbot, mocker):
    mock = mocker.stub()
    switch = SwitchView()
    switch.on_toggle(mock)

    qtbot.addWidget(switch)
    qtbot.mousePress(switch, Qt.LeftButton)

    mock.assert_called_once()
