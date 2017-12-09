import pytest
from hmpy.views.switch import SwitchView
from PyQt5.QtCore import Qt


def test_on_init(qtbot):
    switch = SwitchView("", False)

    qtbot.addWidget(switch)
    assert not switch.on


def test_on_set(qtbot):
    switch = SwitchView("")
    switch.on = True

    qtbot.addWidget(switch)
    assert switch.on is True


def test_toggle_on_checked(qtbot):
    switch = SwitchView("", False)

    switch.toggle()
    qtbot.addWidget(switch)
    assert switch.on is True


def test_toggle_on_toggle(qtbot, mocker):
    mock = mocker.stub()
    switch = SwitchView("", False)
    switch.on_toggle(mock)

    switch.toggle()
    qtbot.addWidget(switch)

    mock.assert_called_once()


def test_on_toggle(qtbot, mocker):
    mock = mocker.stub()
    switch = SwitchView("")
    switch.on_toggle(mock)

    qtbot.addWidget(switch)
    qtbot.mouseClick(switch._button, Qt.LeftButton)

    mock.assert_called_once()
