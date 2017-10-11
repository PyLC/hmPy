import pytest
from hmpy.views import DialView


def test_value_init(qtbot):
    # Test that the value is initialized properly
    val = 50
    view = DialView(val)

    qtbot.addWidget(view)

    assert view.value == val


def test_min_value_init(qtbot):
    # Test that the minimum value is initialized properly
    val = 50
    view = DialView(min_value=val)

    qtbot.addWidget(view)

    assert view.min_value == val


def test_max_value_init(qtbot):
    # Test that the maximum value is initialized properly
    val = 50
    view = DialView(max_value=val)

    qtbot.addWidget(view)

    assert view.max_value == val


def test_value_set(qtbot):
    # Test that the value is set properly
    val = 50
    view = DialView()
    view.value = val

    qtbot.addWidget(view)

    assert view.value == val


def test_min_value_set(qtbot):
    # Test that the minimum value is set properly
    val = 1234
    view = DialView()
    view.min_value = val

    qtbot.addWidget(view)

    assert view.min_value == val


def test_max_value_set(qtbot):
    # Test that the maximum value is set properly
    val = 1234
    view = DialView()
    view.max_value = val

    qtbot.addWidget(view)

    assert view.max_value == val
