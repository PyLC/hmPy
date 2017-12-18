from PyQt5.QtGui import QColor
from hmpy.views import ProgressBarView
from pytest import raises


def test_title_init():
    # Test that title is initialized properly
    title = "water"
    progress_bar = ProgressBarView(title)

    assert progress_bar._title is title


def test_value_init():
    # Test that value is initialized properly
    value = 5
    progress_bar = ProgressBarView("water", value=value)

    assert progress_bar.value == value


def test_value_set(mocker):
    # Test that value is initialized properly
    value = 5
    progress_bar = ProgressBarView("water")
    mocker.spy(progress_bar, 'repaint')

    progress_bar.value = value

    assert progress_bar.repaint.call_count == 1
    assert progress_bar.value == value


def test_min_value_init():
    # Test that min value is initialized properly
    min_value = 50
    progress_bar = ProgressBarView("water", min_value=min_value)

    assert progress_bar.min_value == min_value


def test_min_value_set(mocker):
    # Test that min value is initialized properly
    min_value = 50
    progress_bar = ProgressBarView("water")
    mocker.spy(progress_bar, 'repaint')
    progress_bar.min_value = min_value

    assert progress_bar.repaint.call_count == 1
    assert progress_bar.min_value == min_value


def test_min_value_set_greater_than_max_value():
    # Test that max value is initialized properly
    min_value = 500

    with raises(ValueError):
        progress_bar = ProgressBarView("water", min_value=min_value, max_value=min_value - 1)


def test_max_value_init(mocker):
    # Test that max value is initialized properly
    max_value = 500
    progress_bar = ProgressBarView("water", max_value=max_value)

    assert progress_bar.max_value == max_value


def test_max_value_set(mocker):
    # Test that max value is initialized properly
    max_value = 500
    progress_bar = ProgressBarView("water")
    mocker.spy(progress_bar, 'repaint')
    progress_bar.max_value = max_value

    assert progress_bar.max_value == max_value


def test_max_value_set_smaller_than_min_value(mocker):
    # Test that max value is initialized properly
    max_value = 500

    with raises(ValueError):
        progress_bar = ProgressBarView("water", min_value=max_value + 1, max_value=max_value)


def test_set_value_below_min_value():
    # Test the value set with a
    # value below min, and ensure
    # the bar value equals min
    min_value = 0
    progress_bar = ProgressBarView("water", min_value=min_value)
    progress_bar.value = min_value - 1

    assert progress_bar.value == min_value - 1
    assert progress_bar._bar_value == min_value


def test_set_value_greater_than_max_value():
    # Test the value set with a
    # value greater than max, and ensure
    # the bar value equals max
    max_value = 500
    progress_bar = ProgressBarView("water", max_value=max_value)
    progress_bar.value = max_value + 1

    assert progress_bar.value == max_value + 1
    assert progress_bar._bar_value == max_value


def test_color_init():
    # Test that color is initialized properly
    color = QColor()
    progress_bar = ProgressBarView("water", color=color)

    assert progress_bar.color is color


def test_color_init():
    # Test that color is initialized properly
    color = QColor()
    progress_bar = ProgressBarView("water", color=color)

    assert progress_bar.color is color


def test_color_set(mocker):
    # Test that color is set properly, triggers repaint
    color = QColor()
    progress_bar = ProgressBarView("water")
    mocker.spy(progress_bar, 'repaint')
    progress_bar.color = color

    assert progress_bar.repaint.call_count == 1
    assert progress_bar.color is color


def test_set_color_rgb():
    # Test setting color by rgb works as expected
    r = 1
    g = 127
    b = 255
    progress_bar = ProgressBarView("water")
    progress_bar.set_color_rgb(r, g, b)

    assert progress_bar.color.red() == r
    assert progress_bar.color.green() == g
    assert progress_bar.color.blue() == b
