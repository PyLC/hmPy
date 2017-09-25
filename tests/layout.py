import pytest
from PyQt5.QtWidgets import QWidget, QApplication
from hmpy.layout import InterfaceLayout


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture(scope="module")
def item():
    return QWidget()


def test_count(app, item):
    layout = InterfaceLayout()
    layout.addItem(item)
    layout.addItem(item)
    assert layout.count() == 2


def test_itemAt_valid(app, item):
    layout = InterfaceLayout()
    layout.addItem(item)
    assert layout.itemAt(0) is item
    # Should not have been removed
    assert layout.itemAt(0) is item


def test_itemAt_invalid_low(app, item):
    layout = InterfaceLayout()
    layout.addItem(item)
    assert layout.itemAt(-1) is None


def test_itemAt_invalid_high(app, item):
    layout = InterfaceLayout()
    layout.addItem(item)
    assert layout.itemAt(1) is None


def test_takeAt_valid(app, item):
    layout = InterfaceLayout()
    layout.addItem(item)
    assert layout.takeAt(0) is item
    # Should have been removed
    assert layout.takeAt(0) is None


def test_takeAt_invalid_low(app, item):
    layout = InterfaceLayout()
    layout.addItem(item)
    assert layout.takeAt(-1) is None


def test_itemAt_invalid_high(app, item):
    layout = InterfaceLayout()
    layout.addItem(item)
    assert layout.takeAt(1) is None
