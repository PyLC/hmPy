from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QImage, QConicalGradient, QPalette, QPixmap
from PyQt5.QtCore import Qt, QRect


class LightView(QWidget):
    """View simulating an LED light."""

    def __init__(self, color=QColor(Qt.blue), parent=None):
        """Initialize the view

        :param color: QColor indicating the color of the light.
        :param parent: The parent QWidget.
        """
        super().__init__(parent)
        self.color = color
        self.__on = False

    @property
    def on(self):
        """Get 'on' class attribute.

        :return: the value of the 'on' attribute.
        """
        return self.__on

    @on.setter
    def on(self, to):
        """Set 'on' class attribute, trigger repaint.

        :param to: Boolean value.
        """
        self.__on = to
        self.repaint()

    def paintEvent(self, event):
        """Draw the light graphic onto the widget

        :param event: The paint event.
        """
        paint = QPainter()

        rect = event.rect()

        # Get drawing size and center
        led_rect = QRect(rect)
        size = led_rect.size()
        center = led_rect.center()

        smallest = size.width() if size.width() < size.height() else size.height()

        # Draw graphics on image first (double buffer)
        image = QImage(size, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)

        if self.on:
            fill_color = self.color
        else:
            fill_color = self.color.darker(250)

        # Set the border gradient
        border_gradient = QConicalGradient(center, -90)
        border_color = self.palette().color(QPalette.Dark)
        border_gradient.setColorAt(0.2, border_color)
        border_gradient.setColorAt(0.5, self.palette().color(QPalette.Light))
        border_gradient.setColorAt(0.8, border_color)


        # Draw graphic to image
        paint.begin(image)

        # Set brush and pen
        pen_width = smallest / 8.0
        paint.setBrush(QBrush(fill_color))
        paint.setPen(QPen(QBrush(border_gradient), smallest / 8.0))

        paint.setRenderHint(QPainter.Antialiasing)

        paint.drawEllipse(center, (smallest - pen_width) / 2, (smallest - pen_width) / 2)
        paint.end()

        # Draw image to widget
        paint.begin(self)
        paint.drawPixmap(1, 1, QPixmap.fromImage(image))
        paint.end()