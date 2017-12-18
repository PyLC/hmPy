"""This module defines the SwitchView class."""


from hmpy.views.view import View
from PyQt5.QtGui import QPainter, QImage, QPixmap, QConicalGradient, \
    QPalette
from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtCore import Qt, QSize


class SwitchView(View):
    """The Switch view creates a clickable switch for triggering actions."""

    class _SwitchButton(QAbstractButton):
        """Switch button component"""
        _SCALE = 100

        def __init__(self, parent, text=""):
            QAbstractButton.__init__(self, parent=parent)
            self.setCheckable(True)
            self._text = text
            self._pixmap_cache = {}

        def paintEvent(self, event):
            """Draw the Switch graphic"""
            # Attempt to fetch the cached pixmap for the current state
            image = self._pixmap_cache.get(self.isChecked(), None)

            if image is None:
                # If a cached pixmap is not set, generate one and cache it
                image = self._generate_pixmap(event.rect())

                self._pixmap_cache[self.isChecked()] = image

            # Draw image to view
            paint = QPainter()
            paint.begin(self)
            paint.drawPixmap(self.rect(), image)
            paint.end()

        def _generate_pixmap(self, rect):
            """Generate the pixmap representing the Switch's current state
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
            paint.translate(self.width() / 4, self.height() / 55)

            # Set the border gradient
            border_gradient = QConicalGradient(rect.center(), -30)
            border_color = self.palette().color(QPalette.Dark)
            border_gradient.setColorAt(0.2, border_color)
            border_gradient.setColorAt(0.5,
                                       self.palette().color(QPalette.Light))
            border_gradient.setColorAt(0.8, border_color)

            paint.setBrush(border_gradient)
            scale_x = self.width() / self._SCALE
            scale_y = self.height() / self._SCALE
            paint.drawRect(-20 * scale_x, 0,
                           85 * scale_x, 85 * scale_y)

            paint.setBrush(Qt.darkGray)
            paint.drawRect(-5 * scale_x, 10 * scale_y,
                           55 * scale_x, 70 * scale_y)

            if self.isChecked():
                paint.setBrush(Qt.green)
                paint.drawRect(-5 * scale_x, 10 * scale_y,
                               55 * scale_x, 35 * scale_y)
                paint.setBrush(Qt.darkGreen)
                paint.drawRect(-5 * scale_x, 8 * scale_y,
                               55 * scale_x, 10 * scale_y)
            else:
                paint.setBrush(Qt.red)
                paint.drawRect(-5 * scale_x, 45 * scale_y,
                               55 * scale_x, 35 * scale_y)
                paint.setBrush(Qt.darkRed)
                paint.drawRect(-5 * scale_x, 70 * scale_y,
                               55 * scale_x, 10 * scale_y)

            paint.save()

            paint.translate(self.width() / 2, 35 * scale_y)

            paint.setBrush(Qt.darkGray)
            paint.drawRect(-70 * scale_x, 50 * scale_y,
                           85 * scale_x, 12 * scale_y)

            paint.setPen(Qt.white)

            paint.drawText(-55*scale_x, 58 * scale_y, self._text)

            paint.restore()
            paint.end()

            # Convert to pixmap and return
            return QPixmap.fromImage(image)

    def __init__(self, text="", on=False):
        """Initialize the switch view.

        :param on: the state of the button"""
        super().__init__()
        self._button = self._SwitchButton(self, text)
        self._button.setChecked(on)

    @property
    def on(self):
        return self._button.isChecked()

    @on.setter
    def on(self, state):
        """
        Set the button state

        :param state:
        :return:
        """
        # check if state changed
        if state != self.on:
            self.toggle()

    def toggle(self):
        """Click the button to toggle the switch"""
        self._button.toggle()

    def on_toggle(self, callback):
        """Set callback for on click"""
        if callable(callback):
            self._button.toggled.connect(callback)
        else:
            raise ValueError("callback must be callable")

    def paintEvent(self, event):
        """Draw the Switch graphic onto the view"""
        rect = self.rect()
        size = QSize(rect.width()*.65,
                     rect.height()*.75)
        if size != self._button.size():
            self._button.resize(size)
