from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
from pymodbus3.exceptions import ModbusException
from hmpy.connection import Connection
from PyQt5.QtCore import pyqtSignal


class ModbusConnection(Connection):

    connected_changed = pyqtSignal(bool)

    def __init__(self, connection_ip, connection_port):
        """
        :param connection_ip IP to connected to, default 127.0.0.1
        :type connection_ip: str
        :param connection_port: Port to connect to, default is 502
        :type connection_port: int
        """
        super().__init__()
        self.__connection_ip = connection_ip
        self.__connection_port = connection_port
        self.__connected = False
        self.__client = None  # Added due to pep8 linting

    def connect(self):
        """
        Connect the component to the PLC with the information given from the constructor

        :return: True or false based on the connection
        """
        self.__client = ModbusClient(self.__connection_ip, self.__connection_port)
        self.connected = self.__client.connect()
        return self.connected

    def disconnect(self):
        """Close the ModBus client connection."""
        self.__client.close()
        self.connected = False

    def get_address(self):
        """Get the connection address

        :return: __connection_ip
        """
        return self.__connection_ip

    def get_port(self):
        """Get the connection port.

        :return: __connection_port
        """
        return self.__connection_port

    @property
    def connected(self):
        """Accessor for connected attribute

        :return: __connected
        """
        return self.__connected

    @connected.setter
    def connected(self, value):
        """Setter for connected attribute"""
        self.__connected = value
        self.connected_changed.emit(value)

    def write(self, mem_type, address, value):
        """
        :param mem_type: Constant signifying the type of memory to be written
        :param address: Address or number of the area to be written
        :param value: Value to be written to the PLC
        :return: Void
        """
        if self.connected:
            if mem_type == Connection.Registers.HOLDING_REGISTER:
                self.__client.write_register(address, value)
            elif mem_type == Connection.Registers.COIL:
                self.__client.write_coil(address, value)
            else:
                raise AttributeError

    def read(self, mem_type, address, count=1):
        """
        Method to read values from a connected PLC
        :param mem_type: Constant signifying the type of memory to be read 
        :param address: Address or number of the 
        area to be read 
        :param count: Optional number of registers/coils to read. Defaulted to 1 
        :return: Response from the PLC, or None if there was an error with the read (Exception reading, no connection) 
        coils return boolean, while registers return (if count>1 list of) ints 
        """
        response = None
        if self.connected:
            if mem_type == Connection.Registers.COIL or mem_type == Connection.Registers.DISCRETE_REGISTER:
                response = self.__read_coil(mem_type, address, count)
            else:
                response = self.__read_register(mem_type, address, count)
        return response

    def get_connected(self):
        return self.connected

    def __read_coil(self, mem_type, address, count):
        """
        Helper method for reading coils
        :param address: Address or number of the area to be read
        :param count: Number of bits to read
        :return: Boolean coil value
        """

        try:
            if mem_type == Connection.Registers.DISCRETE_REGISTER:
                response = self.__client.read_discrete_inputs(address, count)
            else:
                response = self.__client.read_coils(address, count)
            if count > 1:
                response = response.bits[:count]
            else:
                response = response.bits[0]
        except ModbusException:
            response = None
        except AttributeError:  # If there are no bits to the response object something went wrong
            response = None
        return response

    def __read_register(self, reg_type, address, count):
        """
        Helper method for reading holding registers
        :param: reg_type: Register type for reading
        :param address: Address or number of the area to be read
        :param count: Number of bits to read
        :return: Int register value
        """
        try:
            if reg_type == Connection.Registers.HOLDING_REGISTER:
                response = self.__client.read_holding_registers(address, count)
            elif reg_type == Connection.Registers.INPUT_REGISTER:
                response = self.__client.read_input_registers(address, count)
            if count > 1:
                response = response.registers[:count]
            else:
                response = response.registers[0]
        except ModbusException:
            response = None
        except AttributeError:  # If there are no bits to the response object something went wrong
            response = None
        return response
