import importlib, inspect, sys
from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal


def get_connection_types():
    connection_types = {}
    types_module = __name__ + '.types'
    importlib.import_module(types_module)
    members = inspect.getmembers(sys.modules[types_module])
    for name, cls in members:
        if inspect.isclass(cls) and issubclass(cls, Connection):
            connection_types[name] = cls
    return connection_types


class RegisterTypes(Enum):
    HOLDING_REGISTER = 1
    INPUT_REGISTER = 2
    DISCRETE_REGISTER = 3
    COIL = 4


class Connection(QObject):

    connected_changed = pyqtSignal(bool)
    deleted = pyqtSignal()

    Registers = RegisterTypes

    def __init__(self):
        super().__init__()

    def connect(self):
        pass

    def disconnect(self):#Overridding and overridden?
        pass

    def write(self, mem_type, address, value):
        pass

    def read(self, mem_type, address, count):
        pass
