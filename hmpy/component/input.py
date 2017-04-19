from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot


class Input(QObject):
    """Represents an input to a Component from a PLC

    :attribute valueChanged: Signal emitted whenever the value changes.
    :attribute value: The value of the input.
    """
    valueChanged = pyqtSignal()

    def __init__(self, interval, register_type, address, connection):
        """Initialize the Input.

        :param interval: Polling interval in ms.
        :param register_type: PLC Register to read from.
        :param address: Address of the register to read from
        :param connection: Connection to the PLC.
        """
        super().__init__()
        self.__interval = interval
        self.__register_type = register_type
        self.__address = address
        self.__connection = connection
        self.__value = None
        if self.__connection is not None:
            self.__connection.deleted.connect(self.deleted)
        self.init_timer()

    def init_timer(self):
        """Initialize/start the polling timer"""
        self.__timer = QTimer()
        self.__timer.setInterval(self.__interval)
        self.__timer.timeout.connect(self.read)
        self.__timer.start(0)

    def read(self):
        """Read a value from the plc. Executed on timer timeout."""
        if self.__connection is not None:
            value = self.__connection.read(self.__register_type, self.__address, 1)
        else:
            value = None

        if not value is None:
            self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value != self.__value:
            self.__value = value
            self.valueChanged.emit()

    @pyqtSlot()
    def deleted(self):
        """When the connection (PLC) is deleted, this causes the connection to become None"""
        self.__connection.deleted.disconnect(self.deleted)
        self.__connection = None

