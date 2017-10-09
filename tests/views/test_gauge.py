import math
import pytest
from hmpy.views import GaugeView


def generate_int(x):
    # Generate an int as a power of 10 with x digits
    return math.pow(10, x - 1)


def test_value_init(qtbot):
    # Test that the value is initialized properly
    val = 1234
    view = GaugeView(val)
    qtbot.addWidget(view)

    assert view.value == val


def test_min_value_init(qtbot):
    # Test that the value is initialized properly
    min_val = 1234
    view = GaugeView(min_value=min_val)
    qtbot.addWidget(view)

    assert view.min_value == min_val


def test_max_value_init(qtbot):
    # Test that the value is initialized properly
    max_val = 1234
    view = GaugeView(max_value=max_val)
    qtbot.addWidget(view)

    assert view.max_value == max_val


def test_value_init(qtbot):
    # Test that the value is initialized properly
    val = 1234
    view = GaugeView(val)
    qtbot.addWidget(view)

    assert view.value == val


def test_min_value_set(qtbot):
    # Test that the value is initialized properly
    val = 1234
    view = GaugeView()
    view.min_value = val
    qtbot.addWidget(view)

    assert view.min_value == val


def test_max_value_set(qtbot):
    # Test that the value is initialized properly
    val = 1234
    view = GaugeView()
    view.max_value = val
    qtbot.addWidget(view)

    assert view.max_value == val


def test_calculate_needle_angle_min(qtbot):
    min_val = 10.0
    val = min_val
    view = GaugeView(val)
    view.min_value = min_val
    qtbot.addWidget(view)

    assert view._needle_angle == -135


def test_calculate_needle_angle_mid(qtbot):
    max_val = 100
    val = max_val / 2
    view = GaugeView(val)
    view.max_value = max_val
    qtbot.addWidget(view)

    assert view._needle_angle == 0.0


def test_calculate_needle_angle_max(qtbot):
    max_val = 133
    val = max_val
    view = GaugeView(val)
    view.max_value = max_val
    qtbot.addWidget(view)

    assert view._needle_angle == 135.0
