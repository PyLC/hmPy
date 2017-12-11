from PyQt5.QtGui import QColor
from hmpy.views import LEDView


def test_on_init():
    # Test that on is initialized properly
    led = LEDView(on=True)
    assert led.on is True

    led = LEDView(on=False)
    assert led.on is False


def test_on_set(mocker):
    # Test that on is set properly, triggers repaint
    led = LEDView(on=False)
    mocker.spy(led, 'repaint')

    led.on = True

    assert led.repaint.call_count == 1
    assert led.on is True


def test_color_init():
    # Test that color is initialized properly
    color = QColor()
    led = LEDView(color=color)

    assert led.color is color


def test_color_set(mocker):
    # Test that color is set properly, triggers repaint
    color = QColor()
    led = LEDView()
    mocker.spy(led, 'repaint')
    led.color = color

    assert led.repaint.call_count == 1
    assert led.color is color


def test_set_color_rgb():
    # Test setting color by rgb works as expected
    r = 1
    g = 127
    b = 255
    led = LEDView()
    led.set_color_rgb(r, g, b)

    assert led.color.red() == r
    assert led.color.green() == g
    assert led.color.blue() == b
