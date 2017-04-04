from PyQt5.QtCore import QObject


class Connection(QObject):

    HOLDING_REGISTER = 1
    INPUT_REGISTER = 2
    DISCRETE_REGISTER = 3
    COIL = 4

    def __init__(self):
        super().__init__()

    def connect(self):
        pass

    def write(self, mem_type, address, value):
        pass

    def read(self, mem_type, address, count):
        pass
