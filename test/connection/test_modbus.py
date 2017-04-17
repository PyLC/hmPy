import unittest
from unittest.mock import patch
from hmpy.connection import Connection
from hmpy.connection.types.modbus import ModbusConnection
from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
from pymodbus3.register_read_message import ReadInputRegistersResponse
from pymodbus3.bit_read_message import ReadDiscreteInputsResponse


class TestModbusConnection(unittest.TestCase):
    """Tests the modbus connection class"""

    def setUp(self):
        """Initialize necessary data connection"""
        self.connection = ModbusConnection("127.0.0.1", 502)
        self.triggered = False
        self.connection.connected_changed.connect(self.set_triggered)

    def tearDown(self):
        """Disconnection from any external resources"""
        self.connection.disconnect()

    def set_triggered(self):
        self.triggered = True

    @patch.object(ModbusClient, 'connect')
    def test_connect(self, mock_connect):
        self.connection.connect()
        mock_connect.assert_called_once()
        self.assertTrue(self.connection.connected)
        self.assertTrue(self.triggered)

    @patch.object(ModbusClient, 'write_coil')
    @patch.object(ModbusClient, 'connect')
    def test_write_coil(self, mock_connect, mock_write):
        self.connection.connect()
        self.connection.write(Connection.Registers.COIL, 1, True)
        mock_write.assert_called_once_with(1, True)

    @patch.object(ModbusClient, 'write_register')
    @patch.object(ModbusClient, 'connect')
    def test_write_holding_register(self, mock_connect, mock_write):
        self.connection.connect()
        self.connection.write(Connection.Registers.HOLDING_REGISTER, 1, 10)
        mock_write.assert_called_once_with(1, 10)

    @patch.object(ModbusClient, 'read_input_registers')
    @patch.object(ModbusClient, 'connect')
    def test_read_input_register(self, mock_connect, mock_read):
        self.connection.connect()
        mock_read.return_value = ReadInputRegistersResponse([0])
        self.assertEqual(self.connection.read(Connection.Registers.INPUT_REGISTER, 1, 1), 0)
        mock_read.assert_called_once_with(1, 1)

    @patch.object(ModbusClient, 'read_discrete_inputs')
    @patch.object(ModbusClient, 'connect')
    def test_read_discrete_register(self, mock_connect, mock_read):
        self.connection.connect()
        mock_read.return_value = ReadDiscreteInputsResponse([False])
        self.assertFalse(self.connection.read(Connection.Registers.DISCRETE_REGISTER, 1, 1))
        mock_read.assert_called_once_with(1, 1)