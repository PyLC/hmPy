from PyQt5.QtCore import QObject


class Connection(QObject):

    WRITE_REGISTER = 1
    WRITE_COIL = 2
    READ_REGISTER = 1
    READ_COIL = 2

    def __init__(self):
        super().__init__()

    def connect(self):
        pass

    def write(self, mem_type, address, value):
        pass


    def read(self, mem_type, address, count):
        pass
