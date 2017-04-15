import importlib, inspect, sys
from PyQt5.QtCore import QObject


def get_connection_types():
    connection_types = {}
    types_module = __name__ + '.types'
    importlib.import_module(types_module)
    members = inspect.getmembers(sys.modules[types_module])
    for name, cls in members:
        if inspect.isclass(cls) and issubclass(cls, Connection):
            connection_types[name] = cls
    return connection_types


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
