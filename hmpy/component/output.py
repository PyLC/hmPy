from PyQt5.QtCore import QObject, pyqtSlot


class Output(QObject):
    """Represents an output from a Component to a PLC

    :attribute value: The value of the output.
    """

    def __init__(self, address, connection):
        """Initialize the Output.

        :param address: Address of the register to write to
        :param connection: Connection to the PLC.
        """
        super().__init__()
        self.__address = address
        self.__connection = connection
        self.__connection.deleted.connect(self.deleted)
        self.__value = None

    def write(self):
        """Write a value to a plc. Executed whenever the value attribute is changed."""
        if not self.value is None and self.__connection is not None:
            self.__connection.write(self.__address, self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value != self.__value:
            self.__value = value
            self.write()

    @pyqtSlot()
    def deleted(self):
        """When the connection (PLC) is deleted, this causes the connection to become None"""
        self.__connection.deleted.disconnect(self.deleted)
        self.__connection = None
