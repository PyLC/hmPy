import unittest
from hmpy.connection.manager import ConnectionManager
from hmpy.connection import Connection
from hmpy.connection.modbus import ModbusConnection


class TestConnectionManager(unittest.TestCase):
    """Tests the ConnectionManager class"""

    def setUp(self):
        """Initialize test data and ConnectionManager."""
        self.connection_name = "test"
        self.connection_address = "127.0.0.1"
        self.connection_port = 503
        self.connection_type = ModbusConnection
        self.manager = ConnectionManager()

    def tearDown(self):
        """Terminate all Connections from the ConnectionManager."""
        self.manager.disconnect_all()

    def test_connect(self):
        """Test adding a valid connection."""
        connection = self.manager.connect(self.connection_name, self.connection_address, self.connection_port, self.connection_type)
        self.assertIsInstance(connection, Connection)

    def test_duplicate_connect(self):
        """Test adding a connection where a connection with the same name already exists."""
        self.manager.connect(self.connection_name, self.connection_address, self.connection_port, self.connection_type)
        with self.assertRaises(ValueError):
           self.manager.connect(self.connection_name, "127.0.0.2", 504, ModbusConnection)

    def test_disconnect_valid(self):
        """Test removing a connection that exists."""
        connection = self.manager.connect(self.connection_name, self.connection_address, self.connection_port,
                                          self.connection_type)
        self.manager.disconnect(self.connection_name)

        has = self.manager.has_connection(self.connection_name)
        self.assertFalse(has)

        # Ensure that the connection is being terminated and not just removed
        connected = connection.get_connected()
        self.assertFalse(connected)

    def test_disconnect_invalid(self):
        """Test removing a connection that does not exists."""
        with self.assertRaises(ValueError):
            self.manager.disconnect(self.connection_name)

    def test_has_get_connection_valid(self):
        """Test getting and checking for a connection when it exists."""
        connection = self.manager.connect(self.connection_name, self.connection_address, self.connection_port,
                                     self.connection_type)
        self.assertIsInstance(connection, Connection)

        has = self.manager.has_connection(self.connection_name)
        self.assertTrue(has)

        fetched = self.manager.get_connection(self.connection_name)
        self.assertIsInstance(connection, Connection)
        self.assertEqual(fetched, connection)

    def test_has_get_connection_invalid(self):
        """Test getting and checking for a connection when it does not exist."""
        self.manager = ConnectionManager()
        has = self.manager.has_connection(self.connection_name)
        self.assertFalse(has)

        connection = self.manager.get_connection(self.connection_name)
        self.assertIsNone(connection)



