from PyQt5.QtCore import QObject


class Output(QObject):
    """Represents an output from a Component to a PLC

    :attribute value: The value of the output.
    """

    def __init__(self, register_type, address, connection):
        """Initialize the Output.

        :param register_type: PLC Register to write to.
        :param address: Address of the register to write to
        :param connection: Connection to the PLC.
        """
        super().__init__()
        self.__register_type = register_type
        self.__address = address
        self.__connection = connection
        self.__value = None

    def write(self):
        """Write a value to a plc. Executed whenever the value attribute is changed."""
        if not self.value is None:
            self.__connection.write(self.__register_type, self.__address, self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value != self.__value:
            self.__value = value
            self.write()
