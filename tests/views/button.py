from PyQt5.QtCore import Qt
from hmpy.views import ButtonView


def test_on_click(qtbot, mocker):
    view = ButtonView("test")
    mock = mocker.stub()
    view.on_click(mock)

    qtbot.addWidget(view)
    qtbot.mouseClick(view.btn, Qt.LeftButton)

    mock.assert_called_once()


def test_on_press(qtbot, mocker):
    mock = mocker.stub()
    view = ButtonView("test")
    view.on_press(mock)

    qtbot.addWidget(view)
    qtbot.mousePress(view.btn, Qt.LeftButton)

    mock.assert_called_once()


def test_on_release(qtbot, mocker):
    mock = mocker.stub()
    view = ButtonView("test")
    view.on_release(mock)

    qtbot.addWidget(view)
    qtbot.mousePress(view.btn, Qt.LeftButton)
    qtbot.mouseRelease(view.btn, Qt.LeftButton)

    mock.assert_called_once()
