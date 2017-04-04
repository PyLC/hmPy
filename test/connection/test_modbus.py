import unittest
from hmpy.connection import Connection
from hmpy.connection.modbus import ModbusConnection


class TestModbusConnection(unittest.TestCase):
    """Tests the modbus connection class"""

    def setUp(self):
        """Initialize necessary data connection"""
        self.connection = ModbusConnection("127.0.0.1", 502)

    def tearDown(self):
        """Disconnection from any external resources"""
        self.connection.disconnect()

    def test_connect(self):
        self.connection.connect()
        self.assertTrue(self.connection.connectedChanged)
        self.assertTrue(self.connection.connected)

        # Not entirely sure how to split these up. Stuff needs to be written to be read.
    def test_read_write_coil(self):
        self.connection.connect()
        self.connection.write(Connection.COIL, 1, True)
        self.assertTrue(self.connection.read(Connection.COIL, 1, 1))

    def test_read_write_holding_register(self):
        self.connection.connect()
        self.connection.write(Connection.HOLDING_REGISTER, 1, 10)
        self.assertEqual(self.connection.read(Connection.HOLDING_REGISTER, 1, 1), 10)

    def read_input_register(self):
        self.connection.connect()
        self.assertEqual(self.connection.read(Connection.INPUT_REGISTER, 1, 1), 0)

    def test_read_discrete_register(self):
        self.connection.connect()
        self.assertFalse(self.connection.read(Connection.DISCRETE_REGISTER, 1, 1))

if __name__ == '__main__':
    unittest.main()
