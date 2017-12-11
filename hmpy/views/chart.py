from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries
from PyQt5.QtGui import QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPointF
from hmpy.views.view import View

__author__ = "Kody Emm"


class LineChart(View):
    """Below are some basic colours for a line, extracted so that no QT components need to be called outside our API"""
    white = Qt.white
    black = Qt.black
    red = Qt.red
    green = Qt.green
    blue = Qt.blue
    yellow = Qt.yellow

    def __init__(self, color, width):
        super().__init__()
        self.chart = QChart()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.chart.legend().hide()
        self.view.setMinimumHeight(self.sizeHint().height())
        self.view.setMinimumWidth(self.sizeHint().width())
        self.__init_line(color, width)
        self.chart.addSeries(self._area_series)
        self.chart.setAxisX(self._y_axis, self._area_series)
        self.chart.setAxisY(self._x_axis, self._area_series)

    def __init_line(self, colour, width):
        self._line = QLineSeries()
        self._area_line = QLineSeries()
        self._area_series = QAreaSeries(self._line, self._area_line)
        self.pen = self._area_series.pen()
        self._gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        if colour is not None:
            self.pen.setColor(colour)
            self._gradient.setColorAt(0.0, colour)
            self._gradient.setColorAt(1.0, colour)
            self._gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        self.pen.setWidthF(width)
        self._line.setPen(self.pen)
        self._area_series.setBrush(self._gradient)
        self._y_axis = QValueAxis()
        self._x_axis = QValueAxis()
        self._y_axis.alignment = Qt.AlignLeft
        self._x_axis.alignment = Qt.AlignRight

    def set_title(self, title):
        self.chart.setTitle(title)

    def paintEvent(self, event):
        size = event.rect().size()
        if size != self.view.size():
            self.view.resize(size)

    def add_data_to_line(self, x_data, y_data):
        """
        Currently when data is added to line the line also changes the range of the axes in that chart in order to properly
        display the data
        :param x_data Data (either list of single number), to add to the list
        :param y_data Data (either list or single number), to add to the list
        """
        if isinstance(x_data, list) and isinstance(y_data, list):
            if len(x_data) == len(y_data):
                for i in range(len(x_data)):
                    self._line.append(x_data[i], y_data[i])
                    self._area_line.append(x_data[i], 0)  # keep a second line at the X-axis
            else:
                raise Exception("X and Y data lists do not have equal amount of elements")
        else:
            self._line.append(x_data, y_data)
            self._area_line.append(x_data, 0)
        if self._line.count() > 100:
            self._line.removePoints(0, self._line.count() - 100)
            self._area_line.removePoints(0, self._area_line.count() - 100)
        limits = self._get_limits()
        self._y_axis.setRange(limits[0], limits[1])
        self._x_axis.setRange(limits[2], limits[3])

    def _get_limits(self):
        """
            :returns tuple
            [0] = min_y
            [1] = max_y
            [2] = min_x
            [3] = max_x
        """
        point_list = self._line.pointsVector()
        minimum_y = point_list[0].y()
        maximum_y = point_list[0].y()
        minimum_x = point_list[0].x()
        maximum_x = point_list[0].x()
        for i in point_list:
            if i.y() < minimum_y:
                minimum_y = i.y()
            elif i.y() > maximum_y:
                maximum_y = i.y()
            if i.x() < minimum_x:
                minimum_x = i.x()
            elif i.x() > maximum_x:
                maximum_x = i.x()
        return minimum_y, maximum_y, minimum_x, minimum_y
