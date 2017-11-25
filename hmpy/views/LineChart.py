from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries
from PyQt5.QtGui import QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPointF
from hmpy.views.view import View

__author__ = "Kody Emm"


class LineChart(View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart = QChart()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.chart.legend().hide()
        self.view.setMinimumHeight(self.sizeHint().height())
        self.view.setMinimumWidth(self.sizeHint().width())

    def set_title(self, title):
        self.chart.setTitle(title)

    def add_line(self, line):
        self.chart.addSeries(line.get_area_line())
        self.chart.setAxisX(line.x_axis, line.get_area_line())
        self.chart.setAxisY(line.y_axis, line.get_area_line())

    def paintEvent(self, event):
        size = event.rect().size()
        if size != self.view.size():
            self.view.resize(size)

"""The Line class represents a single line within the LineChart"""


class Line:

    """Below are some basic colours for a line, extracted so that no QT components need to be called outside our API,"""
    white = Qt.white
    black = Qt.black
    red = Qt.red
    green = Qt.green
    blue = Qt.blue
    yellow = Qt.yellow

    def __init__(self, colour=None, width=0.1):
        self._line_actual = QLineSeries()
        self._line_area = QLineSeries()
        self._area_series = QAreaSeries(self._line_actual, self._line_area)
        self.pen = self._area_series.pen()
        self._gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        if colour is not None:
            self.pen.setColor(colour)
            self._gradient.setColorAt(0.0, colour)
            self._gradient.setColorAt(1.0, colour)
            self._gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        self.pen.setWidth(width)
        self._line_actual.setPen(self.pen)
        self._area_series.setBrush(self._gradient)
        self.y_axis = QValueAxis()
        self.x_axis = QValueAxis()
        self.y_axis.alignment = Qt.AlignLeft
        self.x_axis.alignment = Qt.AlignRight
    """
    Currently when data is added to line the line also changes the range of the axes in that chart in order to properly
    display the data
    :param x_data Data (either list of single number), to add to the list
    :param y_data Data (either list or single number), to add to the list
    """
    def add_data_to_line(self, x_data, y_data):
        if isinstance(x_data, list) and isinstance(y_data, list):
            if len(x_data) == len(y_data):
                for i in range(len(x_data)):
                    self._line_actual.append(x_data[i], y_data[i])
                    self._line_area.append(x_data[i], 0)  # keep a second line at the X-axis
            else:
                raise Exception("X and Y data lists do not have equal amount of elements")
        else:
            self._line_actual.append(x_data, y_data)
            self._line_area.append(x_data, 0)
        if self._line_actual.count() > 100:
            self._line_actual.removePoints(0, self._line_actual.count() - 100)
            self._line_area.removePoints(0, self._line_actual.count() - 100)
        self.y_axis.setRange(self._get_y_limits()[0], self._get_y_limits()[1])
        self.x_axis.setRange(self._get_x_limits()[0], self._get_x_limits()[1])

    """
        :returns the area chart itself
    """

    def get_area_line(self):
        return self._area_series

    """
        :returns tuple, first element being the minimum Y value in the series, second element is the max Y value in the
        series
    """
    def _get_y_limits(self):
        list_of_y_points = []
        point_list = self._line_actual.pointsVector()
        for i in point_list:
            # TODO: there needs to be a better way to do this
            list_of_y_points.append(i.y())
        return min(list_of_y_points), max(list_of_y_points)
    """
        :returns tuple, first element being the minimum X value in the series, second element is the max X value in the
        series
    """
    def _get_x_limits(self):
        list_of_x_points = []
        point_list = self._line_actual.pointsVector()
        for i in point_list:
            # TODO: Better way to do this
            list_of_x_points.append(i.x())
        return min(list_of_x_points), max(list_of_x_points)
