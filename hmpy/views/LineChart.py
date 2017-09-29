from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter
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
        self.chart.addSeries(line.get_internal_line())
        self.chart.setAxisX(line.x_axis, line.get_internal_line())
        self.chart.setAxisY(line.y_axis, line.get_internal_line())

    def paintEvent(self, event):
        size = event.rect().size()
        if size != self.view.size():
            self.view.resize(size)

"""The Line class represents a single line within the LineChart"""
class Line:
    def __init__(self, colour=None, width=0.1):
        self._line = QLineSeries()
        self.pen = self._line.pen()
        if colour is not None:
            self.pen.setColor(colour)
        self.pen.setWidth(width)
        self._line.setPen(self.pen)
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
                    self._line.append(x_data[i], y_data[i])
            else:
                raise Exception("X and Y data lists do not have equal amount of elements")
        else:
            self._line.append(x_data, y_data)
        self.y_axis.setRange(self._get_y_limits()[0], self._get_y_limits()[1])
        self.x_axis.setRange(self._get_x_limits()[0], self._get_x_limits()[1])
    """
        :returns QLineSeries representation of the line
    """
    def get_internal_line(self):
        return self._line

    """
        :returns tuple, first element being the minimum Y value in the series, second element is the max Y value in the
        series
    """
    def _get_y_limits(self):
        list_of_y_points = []
        point_list = self._line.pointsVector()
        for i in point_list:
            # there needs to be a better way to do this
            list_of_y_points.append(i.y())
        return min(list_of_y_points), max(list_of_y_points)
    """
        :returns tuple, first element being the minimum X value in the series, second element is the max X value in the
        series
    """
    def _get_x_limits(self):
        list_of_x_points = []
        point_list = self._line.pointsVector()
        for i in point_list:
            list_of_x_points.append(i.x())
        return min(list_of_x_points), max(list_of_x_points)
