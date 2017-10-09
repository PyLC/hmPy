import math
import pytest
from hmpy.views import LCDView


@pytest.fixture(scope="module")
def digits():
    return 10


def generate_int(x):
    # Generate an int as a power of 10 with x digits
    return math.pow(10, x - 1)


def test_value_init():
    # Test that the value is initialized properly
    val = 1234
    view = LCDView(val)
    assert view.lcd.value() == val


def test_value_set():
    # Test that the value is set properly
    val = 1234
    view = LCDView()
    view.value = val
    assert view.lcd.value() == val


def test_digit_count_init(digits):
    # Test that the digit count is initialized according to the value
    view = LCDView(generate_int(digits))
    assert view.lcd.digitCount() == digits


def test_digit_count_increase(digits):
    # Test that the digit count increases with the value
    view = LCDView(generate_int(digits - 1))
    view.value = generate_int(digits)
    assert view.lcd.digitCount() == digits


def test_digit_count_decrease(digits):
    # Test that the digit count decreases with the value
    view = LCDView(generate_int(digits + 1))
    view.value = generate_int(digits)
    assert view.lcd.digitCount() == digits


def test_digit_count_negative(digits):
    # Test that the digit count accounts for the - in negative values
    view = LCDView(-generate_int(digits))
    assert view.lcd.digitCount() == digits + 1
