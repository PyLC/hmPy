"""This module defines the LEDView class."""

from hmpy.views.view import View
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QImage, QConicalGradient, QPalette, QPixmap, QRadialGradient
from PyQt5.QtCore import Qt, QPointF


class LEDView(View):
    """View simulating a LED with boolean state."""

    _DARK_FACTOR = 250
    _BORDER_RATIO = 16.0

    def __init__(self, on=False, color=QColor(Qt.red)):
        super().__init__()
        self._state = on
        self._color = color

        # Since there is only two states, cache them, instead of repainting on change
        self._pixmap_cache = {}

    @property
    def on(self):
        """Get 'on' class attribute.

        :return: the Boolean value of the 'on' attribute.
        """
        return self._state

    @on.setter
    def on(self, to):
        """Set 'on' class attribute, trigger repaint.

        :param to: Boolean value."""
        self._state = to
        self.repaint()

    @property
    def color(self):
        """Get 'color' class attribute

        :return: the QColor value of the 'color' attribute."""
        return self._color

    @color.setter
    def color(self, to):
        """Set 'color' class attribute, trigger repaint.

        :param to: QColor value
        """
        self._color = to
        self._pixmap_cache = {}
        self.repaint()

    def set_color_rgb(self, r, g, b):
        """Set the LED color by rgb

        :param r: red value.
        :param g: green value.
        :param b: blue value.
        """
        self.color = QColor(r, g, b)

    def paintEvent(self, event):
        """Draw the LED graphic

        :param event: The paint event.
        """
        # Attempt to fetch the cached pixmap for the current state
        image = self._pixmap_cache.get(self.on)

        if image is None:
            # If a cached pixmap is not set, generate one and cache it
            image = self._generate_pixmap(event.rect())
            self._pixmap_cache[self.on] = image

        # Draw image to view
        paint = QPainter()
        paint.begin(self)
        paint.drawPixmap(1, 1, image)
        paint.end()

    def _generate_pixmap(self, rect):
        """Generate the pixmap representing the LED's current state

        :param rect: the QRectangle representing the view.
        :return:
        """
        paint = QPainter()

        # Get view size and center
        size = rect.size()
        center = rect.center()

        # LED should be drawn in a square, find the smallest side length
        smallest = size.width() if size.width() < size.height() else size.height()

        # Set the LED color
        if self.on:
            fill_color = self._color
        else:
            fill_color = self._color.darker(self._DARK_FACTOR)
        fill_gradient = QRadialGradient(center, smallest / 4.0 * 3, QPointF(center.x(), size.height() / 6.0))
        fill_gradient.setColorAt(0.0, fill_color.lighter(150))
        fill_gradient.setColorAt(0.5, fill_color.lighter(120))
        fill_gradient.setColorAt(1.0, fill_color)

        # Set the border
        border_gradient = QConicalGradient(center, -90)
        border_gradient.setColorAt(0.2, self.palette().color(QPalette.Dark))
        border_gradient.setColorAt(0.5, self.palette().color(QPalette.Light))
        border_gradient.setColorAt(0.8, self.palette().color(QPalette.Dark))

        # Draw graphics to image (double buffer)
        image = QImage(size, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)

        paint.begin(image)
        pen_width = smallest / self._BORDER_RATIO
        paint.setBrush(QBrush(fill_gradient))
        paint.setPen(QPen(QBrush(border_gradient), pen_width))

        paint.setRenderHint(QPainter.Antialiasing)

        paint.drawEllipse(center, (smallest - pen_width) / 2, (smallest - pen_width) / 2)
        paint.end()

        # Convert to pixmap and return
        return QPixmap.fromImage(image)
