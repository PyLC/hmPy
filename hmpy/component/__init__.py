from PyQt5.QtCore import QObject


class Component(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_view(self, view):
        self.__view = view