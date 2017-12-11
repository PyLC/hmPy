from PyQt5.QtCore import QTimer


class Timer:

    def __init__(self, interval, action, recurring=True):
        self._action = action
        self._timer = QTimer()
        self._timer.setSingleShot(not recurring)
        self._timer.setInterval(interval)
        self._timer.timeout.connect(self._perform_action)

    @property
    def interval(self):
        return self._timer.interval()

    @interval.setter
    def interval(self, interval):
        self._timer.setInterval(interval)

    def set_action(self, action):
        self._action = action

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def _perform_action(self):
        self._action()
