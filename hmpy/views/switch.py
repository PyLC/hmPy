"""This module defines the SwitchView class."""


from hmpy.views.view import View
from PyQt5.QtGui import QPainter, QImage, QPixmap, QConicalGradient, QPalette
from PyQt5.QtCore import Qt


class SwitchView(View):
    """The Switch view creates a clickable switch for triggering actions."""

    _SCALE = 100

    def __init__(self, on=False):
        """Initialize the switch view.

        :param on: the state of the button"""
        super().__init__()
        self._state = on
        self.mousePressEvent = self._mouse_press_event
        self._on_toggle = None

        self._pixmap_cache = {}

    def paintEvent(self, event):
        """Draw the Switch graphic

        :param event: The paint event.
        """

        # Attempt to fetch the cached pixmap for the current state
        image = self._pixmap_cache.get(self.on, None)

        if image is None:
            # If a cached pixmap is not set, generate one and cache it
            image = self._generate_pixmap(event.rect())
            self._pixmap_cache[self.on] = image

        # Draw image to view
        paint = QPainter()
        paint.begin(self)
        paint.drawPixmap(self.rect(), image)
        paint.end()

    @property
    def on(self):
        return self._state

    @on.setter
    def on(self, to):
        self._state = to
        self.repaint()

    def toggle(self):
        self._state = not self._state
        if self._on_toggle is not None:
            self._on_toggle()
        self.repaint()

    def on_toggle(self, callback):
        self._on_toggle = callback

    def _mouse_press_event(self, event):
        self.toggle()

    def _generate_pixmap(self, rect):
        """Generate the pixmap representing the LED's current state
        :param rect: the QRectangle representing the view.
        :return:
        """
        paint = QPainter()

        # Get view size and center
        size = rect.size()

        # Draw graphics to image (double buffer)
        image = QImage(size, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)

        paint.begin(image)

        # Set the border gradient
        border_gradient = QConicalGradient(rect.center(), -30)
        border_color = self.palette().color(QPalette.Dark)
        border_gradient.setColorAt(0.2, border_color)
        border_gradient.setColorAt(0.5, self.palette().color(QPalette.Light))
        border_gradient.setColorAt(0.8, border_color)

        paint.setBrush(border_gradient)
        scale_x = self.width() / self._SCALE
        scale_y = self.height() / self._SCALE

        paint.drawRect(0, 0, 95 * scale_x, 45 * scale_y)
        paint.setBrush(Qt.darkGray)
        paint.drawRect(8 * scale_x, 10 * scale_y, 80 * scale_x, 25 * scale_y)

        if self._state:
            paint.setBrush(Qt.green)
            paint.drawRect(48 * scale_x, 10 * scale_y,
                           40 * scale_x, 25 * scale_y)
            paint.setBrush(Qt.darkGreen)
            paint.drawRect(80 * scale_x, 10 * scale_y,
                           8 * scale_x, 25 * scale_y)
        else:
            paint.setBrush(Qt.red)
            paint.drawRect(8 * scale_x, 10 * scale_y,
                           40 * scale_x, 25 * scale_y)
            paint.setBrush(Qt.darkRed)
            paint.drawRect(8 * scale_x, 10 * scale_y,
                           8 * scale_x, 25 * scale_y)

        paint.end()

        # Convert to pixmap and return
        return QPixmap.fromImage(image)
