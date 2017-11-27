from hmpy.views.LineChart import Line, LineChart
from PyQt5.QtCore import Qt
from PyQt5.Qt import QColor
import pytest


def test_on_init():
    line = Line(Line.yellow, 15)
    assert line.pen.color().name() == QColor(Qt.yellow).name()


def test_add_unequal_data_lists_to_line():
    line = Line(Line.yellow, 5)
    with pytest.raises(Exception):
        line.add_data_to_line([1, 2, 3, 4, 5], [1, 2, 3, 4])


def test_ranges():
    line = Line(Line.yellow, 5)
    line.add_data_to_line([1, 2, 3, 4, 100], [100, 200, 300, 400, 500])
    assert line.x_axis.max() == 100
    assert line.x_axis.min() == 1
    assert line.y_axis.max() == 500
    assert line.y_axis.min() == 100


def test_data_trim():
    line = Line(Line.yellow, 5)
    for i in range(0, 1000):
        line.add_data_to_line(i, i)
    assert line.get_area_line().lowerSeries().count() <= 100
    assert line.get_area_line().upperSeries().count() <= 100
