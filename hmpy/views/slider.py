"""This module defines the Slider View class."""


from .view import View
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QPainter,QFont,QColor,QImage,QPixmap

class SliderView(View):
    """The Slider view creates a slider for input.

    :param minimum: minimum int value of slider.
    :param maximum: maximum int value of slider.
    :param current: starting value of slider.
    :param interval: distance each tick will travel on slider.
    :param interactive: can user interact with it on UI.
    """
    def __init__(self ,minimum=0, maximum=100,current=0,interval=2,interactive=True):
        """Initialize the slider view."""

        super().__init__()
        self.slider = QSlider(self)
        self.minimum_value = minimum;
        self.maximum_value = maximum;
        self.slider.setValue(current)
        self.tick_interval = interval;
        self.interactive = interactive
        self.slider.setGeometry(self.x(),self.y(),800,200)

    @property
    def interactive(self):
        return self.slider.isEnabled();

    @interactive.setter
    def interactive(self,interactive):
        self.slider.setEnabled(interactive)

    @property
    def fixed_width(self):
        return self.slider.width();

    @fixed_width.setter
    def fixed_width(self, width):
        self.slider.setFixedWidth(width);

    @property
    def tick_interval(self):
        return self.slider.tickInterval()

    @tick_interval.setter
    def tick_interval(self,interval):
        if interval <= 0:
            self.slider.setTickInterval(self.slider.tickInterval())
        else:
            self.slider.setTickInterval(interval)

    @property
    def maximum_value(self):
        return self.slider.maximum()

    @maximum_value.setter
    def maximum_value(self,maximum):
        if maximum < 0:
            self.slider.setMaximum(self.slider.maximum())
        else:
            self.slider.setMaximum(maximum)

    @property
    def minimum_value(self):
        return self.slider.minimum()

    @minimum_value.setter
    def minimum_value(self, minimum):
        if minimum >= 0:
            self.slider.setMinimum(minimum)
        else:
            self.slider.setMinimum(0)


    def paintEvent(self, event):

        qp = QPainter()
        rect = event.rect()

        slider_rect = QRect(rect)

        size = slider_rect.size()
        center = slider_rect.center()


        # Draw graphics on image first (double buffer)
        image = QImage(size, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)

        qp.begin(image)

        self.drawText(event, qp)
        qp.end()

    # Draw image to widget
        qp.begin(self)
        qp.drawPixmap(1, 1, QPixmap.fromImage(image))
        qp.end()

    def drawText(self, event, qp):

        qp.save()
        rects = QRect(event.rect())
        rects.setWidth(200)
        rects.setHeight(40)
        if (self.interactive):
            qp.setPen(QColor(50, 50, 255))
        else:
            qp.setPen(QColor(200, 200, 200))


        qp.setFont(QFont('Decorative', 15))

        qp.drawText(rects, Qt.AlignHCenter,str(self.slider.value()))
        qp.restore()

    def set_horizontal_orientation(self):
        self.slider.setOrientation(Qt.Horizontal)

    def set_vertical_orientation(self):
        self.slider.setOrientation(Qt.Vertical)

    def on_change(self, callback):
        self.slider.valueChanged.connect(callback)

