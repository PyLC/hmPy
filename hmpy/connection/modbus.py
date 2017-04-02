from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
from . import Connection
from PyQt5.QtCore import pyqtSignal


class ModbusConnection(Connection):

    connectedChanged = pyqtSignal(bool)

    def __init__(self, connection_ip="127.0.0.1", connection_port=502):
        """
        :param connection_ip IP to connected to, default 127.0.0.1
        :type connection_ip: str
        :param connection_port Port to connect to, default is 502
        :type connection_port: int
        """
        super().__init__()
        self.__connection_ip = connection_ip
        self.__connection_port = connection_port
        self.__connected = False

    def connect(self):
        """
        Connect the component to the PLC with the information given from the constructor
        :return: True or false based on the connection
        """
        self.__client = ModbusClient(self.__connection_ip, self.__connection_port)
        self.connected = self.__client.connect()
        return self.connected

    def disconnect(self):
        self.__client.close()
        self.connected = False

    @property
    def connected(self):
        """Accessor for connected attribute"""
        return self.__connected

    @connected.setter
    def connected(self, value):
        """Setter for connected attribute"""
        self.__connected = value;
        self.connectedChanged.emit(value)

    def set_connected(self, connected):
        """Set the connection state

        :param connected: boolean representing connection state
        """
        self.connected = connected
        self.connectedChanged.emit(connected)

    def write(self, mem_type, address, value):
        """
        :param mem_type: Constant signifying the type of memory to be written
        :param address: Address or number of the area to be written
        :param value: Value to be written to the PLC
        :return: Details of the request (use request.~) or None if there was no connection
        """
        request = None
        if self.connected:
            if mem_type == Connection.WRITE_REGISTER:
                request = self.__client.write_register(address, value)
            else:
                request = self.__client.write_coil(address, value)
        return request

    def read(self, mem_type, address, count):
        """
        :param mem_type: Constant signifying the type of memory to be read
        :param address: Address or number of the area to be read
        :param count: Number of bits to read
        :return: Response from the PLC, or None if there was no connection
        """
        response = None
        if self.connected:
            if mem_type == Connection.READ_REGISTER:
                response = self.__client.read_holding_registers(address, count)
            else:
                response = self.__client.read_coils(address, count)
        return response

    def get_connected(self):
        return self.connected