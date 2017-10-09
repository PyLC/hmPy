from hmpy.views.view import View
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QImage, QConicalGradient, QPalette, QPixmap, QPolygon, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRect, QPoint, QPointF
from enum import Enum
import math


class GaugeView(View):
    """
    View simulating a Gauge.
    """

    def __init__(self, value=0, min_value=0, max_value=100, precision=2,
                 unit_text="", color=QColor(Qt.white)):
        """Initialize the view

        :param starting_value: starting value for the gauge.
        :param min_value: The minimum value of the gauge.
        :param max_value: The minimum value of the gauge.
        :param precision: The minimum value of the gauge.
        :param unit_text: The text displaying the unit of the gauge
        :param color: The background colour of the gauge
        """
        super().__init__()

        self._color = color
        self._unit_text = unit_text
        self.__value = value

        self.__min_value = min_value
        self.__max_value = max_value

        self._precision = precision

        self._pointText = []
        self._create_point_text()
        self._needle_angle = -135
        self._calculate_needle_angle()


    @property
    def value(self):
        """Get 'value' class attribute.

        :return: the value of the 'value' attribute.
        """
        return self.__value

    @value.setter
    def value(self, value):
        """Set 'value' class attribute, trigger repaint.

        :param to: Boolean value.
        """
        if value < self.__min_value:
            self.__value = self.__min_value
        elif value > self.__max_value:
            self.__value = self.__max_value
        else:
            self.__value = value

        self._calculate_needle_angle()
        self.repaint()

    @property
    def min_value(self):
        """Get 'min_value' class attribute.

        :return: the value of the 'min_value' attribute.
        """
        return self.__min_value

    @min_value.setter
    def min_value(self, min_value):
        """Set 'min_value' class attribute, trigger repaint.

        :param to: Boolean value.
        """
        self.__min_value = min_value

        self._calculate_needle_angle()
        self.repaint()

    @property
    def max_value(self):
        """Get 'max_value' class attribute.

        :return: the value of the 'max_value' attribute.
        """
        return self.__max_value

    @max_value.setter
    def max_value(self, max_value):
        """Set 'max_value' class attribute, trigger repaint.

        :param to: Boolean value.
        """
        self.__max_value = max_value

        self._calculate_needle_angle()
        self.repaint()

    def paintEvent(self, event):
        """Draw the gauge graphic onto the widget

        :param event: The paint event.
        """
        paint = QPainter()
        
        rect = event.rect()

        # Get drawing size and center
        gauge_rect = QRect(rect)
        size = gauge_rect.size()
        center = gauge_rect.center()

        smallest = size.width() if size.width() < size.height() else size.height()

        # Set the border gradient
        border_gradient = QConicalGradient(center, -90)
        border_color = self.palette().color(QPalette.Dark)
        border_gradient.setColorAt(0.2, border_color)
        border_gradient.setColorAt(0.5, self.palette().color(QPalette.Light))
        border_gradient.setColorAt(0.8, border_color)

        # Draw graphics on image first (double buffer)
        image = QImage(size, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)

        # Draw graphic to image
        paint.begin(image)

        # Set brush and pen
        pen_width = smallest / 18.0
        paint.setBrush(QBrush(self._color))
        paint.setRenderHint(QPainter.Antialiasing)

        paint.save()
        paint.setPen(QPen(QBrush(border_gradient), smallest / 18.0))
        
        paint.drawEllipse(center, (smallest - pen_width) / 2, (smallest - pen_width) / 2)

        border_color = self.palette().color(QPalette.Dark)
        border_gradient.setColorAt(0.2, border_color)
        border_gradient.setColorAt(0.5, self.palette().color(QPalette.Shadow))
        border_gradient.setColorAt(0.8, border_color)

        paint.setPen(QPen(QBrush(border_gradient), smallest / 25.0))
        paint.drawEllipse(center, ((smallest - pen_width) / 2) - smallest / 25.0, ((smallest - pen_width) / 2) - smallest / 25.0)

        paint.restore()

        self._draw_arc(paint, ((smallest - pen_width) / 2) - smallest / 15)
        self._draw_needle(paint)
        self._draw_markings(paint, ((smallest - pen_width) / 2) - smallest / 15)
        self._draw_value_text(paint)
        
        paint.end()

        # Draw image to widget
        paint.begin(self)
        paint.drawPixmap(1, 1, QPixmap.fromImage(image))
        paint.end()


    def _create_point_text(self):
        add = (self.__max_value - self.__min_value) / (275.0 / 25)
        value = self.__min_value

        for i in range(0, 12):
            self._pointText.append(("%%.%df" % self._precision) % value)
            value += add

    def _draw_value_text(self, paint):
        paint.save()

        paint.translate(self.width() / 2, self.height() / 2)

        smallest = self.width() / 2.5 if self.width() < self.height() else self.height() / 2.5

        font = QFont(self.font())
        font.setPixelSize(smallest / 8)
        paint.setFont(font)

        text = ("%%.%df" % self._precision) % self.__value

        font_metric = QFontMetrics(font)
        paint.drawText(0 - font_metric.width(text) / 2, smallest / 2, text)
        paint.drawText(0 - font_metric.width(self._unit_text) / 2, smallest / 2 + 20, self._unit_text)

        paint.restore()

    def _draw_markings(self, paint, radius):
        paint.save()

        paint.translate(self.width() / 2, self.height() / 2)

        smallest = self.width() / 2.5 if self.width() < self.height() else self.height() / 2.5

        font = QFont(self.font())
        font.setPixelSize(smallest / 10)
        paint.setFont(font)

        i = -140
        counter = 0

        paint.rotate(i)

        while i <= 135:
            if (i + 140) % 25 == 0:
                paint.drawLine(2, -smallest, 2, -(smallest - 10))
                paint.save()

                paint.resetTransform()
                paint.translate(self.width() / 2, self.height() / 2)

                x = ((radius * 0.75) * math.cos((i - 90) * math.pi / 180.0)) - (smallest / 8)
                y = ((radius * 0.75) * math.sin((i - 90) * math.pi / 180.0))

                paint.drawText(x, y, self._pointText[counter])
                counter += 1
                paint.restore()
            else:
                paint.drawLine(2, -smallest, 2, -(smallest - 5))

            paint.rotate(5)
            i += 5

        paint.restore()

    def _draw_arc(self, paint, radius):
        paint.save()
        paint.translate(self.width() / 2 - radius / 2, self.height() / 2 - radius / 2)

        grad = QConicalGradient(QPointF(radius / 2, radius / 2), 270.0)
        grad.setColorAt(.75, Qt.green)
        grad.setColorAt(.5, Qt.yellow)
        grad.setColorAt(.25, Qt.red)
        paint.setPen(QPen(QBrush(grad), radius / 18.0))
        paint.drawArc(QRect(-radius / 2 - 1.4, -radius / 2, radius * 2, radius * 2), 228 * 15.9, -((self._needle_angle + 135) * 16.1))
        paint.restore()

    def _draw_needle(self, paint):
        paint.save()
        paint.translate(self.width()/2, self.height()/2)

        scale = min(self.width() / 120.0, self.height() / 120.0)

        paint.scale(scale, scale)

        paint.setPen(QColor(255, 33, 33))
        paint.setBrush(Qt.red)

        needle = QPolygon([QPoint(-1, -32), QPoint(-3, 10), QPoint(3, 10), QPoint(1, -32)])
        paint.rotate(self._needle_angle)

        paint.drawPolygon(needle)

        paint.setPen(Qt.gray)
        paint.setBrush(Qt.gray)

        # Set the border gradient
        border_gradient = QConicalGradient(QPoint(0, 0), -90)
        border_color = self.palette().color(QPalette.Dark)
        border_gradient.setColorAt(0.2, border_color)
        border_gradient.setColorAt(0.5, self.palette().color(QPalette.Shadow))
        border_gradient.setColorAt(0.8, border_color)

        paint.drawEllipse(QPoint(0, 0), 5, 5)

        # Set the border gradient
        border_gradient = QConicalGradient(QPoint(0, 0), -90)
        border_color = self.palette().color(QPalette.Light)
        border_gradient.setColorAt(0.2, border_color)
        border_gradient.setColorAt(0.5, self.palette().color(QPalette.Light))
        border_gradient.setColorAt(0.8, border_color)

        paint.drawEllipse(QPoint(0, 0), 5, 5)

        paint.restore()

    def _calculate_needle_angle(self):
        """
        calculates the needle angle
        """
        self._needle_angle = ((270.0 * ((self.__value - self.__min_value) / (self.__max_value - self.__min_value))) - 135.0)



