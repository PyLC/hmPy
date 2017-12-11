from hmpy.views.chart import LineChart
from PyQt5.QtCore import Qt
from PyQt5.Qt import QColor
import pytest


def test_add_unequal_data_lists_to_line():
    chart = LineChart(LineChart.yellow, 5)
    with pytest.raises(Exception):
        chart.add_data_to_line([1, 2, 3, 4, 5], [1, 2, 3, 4])


def test_ranges():
    chart = LineChart(LineChart.yellow, 5)
    chart.add_data_to_line([1, 2, 3, 4, 100], [100, 200, 300, 400, 500])
    assert chart._x_axis.max() == 100
    assert chart._x_axis.min() == 1
    assert chart._y_axis.max() == 500
    assert chart._y_axis.min() == 100


def test_data_trim():
    chart = LineChart(LineChart.yellow, 5)
    for i in range(0, 1000):
        chart.add_data_to_line(i, i)
    assert chart._area_series.lowerSeries().count() <= 100
    assert chart._area_series.upperSeries().count() <= 100
