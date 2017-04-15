import sys
import unittest
from hmpy.connection.manager import ConnectionManager
from hmpy.connection import Connection
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)


class TestConnectionManager(unittest.TestCase):
    """Tests the ConnectionManager class"""

    def setUp(self):
        """Initialize test data and ConnectionManager."""
        self.connection_name = "test"
        self.connection_address = "127.0.0.1"
        self.connection_port = 503
        self.connection_type = HelperConnection
        self.manager = ConnectionManager()
        self.triggered = False

    def tearDown(self):
        """Destroy all connections on the ConnectionManager."""
        self.manager.destroy_all()

    def set_triggered(self):
        """Helper method used as slot. Sets class attribute succeeded to True when invoked."""
        self.triggered = True

    def test_add(self):
        """Test adding a valid connection."""
        connection = self.manager.add(self.connection_name, self.connection_address, self.connection_port,
                                          self.connection_type)
        self.assertIsInstance(connection, Connection)

    def test_duplicate_add(self):
        """Test adding a connection where a connection with the same name already exists."""
        self.manager.add(self.connection_name, self.connection_address, self.connection_port, self.connection_type)
        with self.assertRaises(ValueError):
            self.manager.add(self.connection_name, self.connection_address, self.connection_port, self.connection_type)

    def test_destroy_valid(self):
        """Test destroying a connection that exists."""
        connection = self.manager.add(self.connection_name, self.connection_address, self.connection_port,
                                          self.connection_type)
        self.manager.destroy(self.connection_name)

        # Ensure connection was properly disconnected
        self.assertFalse(connection.get_connected())
        # Ensure connection was removed from manager
        self.assertFalse(self.manager.has_connection(self.connection_name))

    def test_destroy_invalid(self):
        """Test destroying a connection that does not exists."""
        with self.assertRaises(ValueError):
            self.manager.destroy(self.connection_name)

    def test_destroy_all(self):
        """Test that method destroy_all destroys all connections."""
        self.second_connection_name = self.connection_name + '_two'
        first_connection = self.manager.add(self.connection_name, self.connection_address, self.connection_port, self.connection_type)
        second_connection = self.manager.add(self.second_connection_name, self.connection_address, self.connection_port, self.connection_type)
        self.manager.destroy_all()

        # Test that the Connections were properly disconnected
        self.assertFalse(first_connection.get_connected())
        self.assertFalse(second_connection.get_connected())

        # Test that the Connections were removed from the ConnectionManager
        self.assertFalse(self.manager.has_connection(self.connection_name))
        self.assertFalse(self.manager.has_connection(self.second_connection_name))

        # Test that nothing remains in the ConnectionManager
        self.assertDictEqual(self.manager.get_connections(), {})

    def test_has_get_connection_valid(self):
        """Test getting and checking for a connection when it exists."""
        connection = self.manager.add(self.connection_name, self.connection_address, self.connection_port,
                                          self.connection_type)

        # Test that the returned Connection is in fact a Connection
        self.assertIsInstance(connection, Connection)
        # Test that the new Connection has been added to the connection manager under the proper name
        self.assertTrue(self.manager.has_connection(self.connection_name))
        # Test that the new connection can be properly retrieved from the ConnectionManager
        fetched = self.manager.get_connection(self.connection_name)
        self.assertEqual(fetched, connection)

    def test_has_get_connection_invalid(self):
        """Test getting and checking for a connection when it does not exist."""
        self.manager = ConnectionManager()
        has = self.manager.has_connection(self.connection_name)
        self.assertFalse(has)

        connection = self.manager.get_connection(self.connection_name)
        self.assertIsNone(connection)

    def test_connections_changed_emit(self):
        """Test that the connections_changed signal is emitted when connections are added or destroyed."""
        self.manager.connections_changed.connect(self.set_triggered)
        self.manager.add(self.connection_name, self.connection_address, self.connection_port,
                         self.connection_type)

        # Test if the slot was triggered when a new connection is added
        self.assertTrue(self.triggered)

        self.triggered = False
        self.manager.destroy(self.connection_name)
        # Test if the slot was triggered when a connection is detroyed
        self.assertTrue(self.triggered)

    def test_connected_connections_changed_emit(self):
        """Test that the connections_changed signal is emitted when a Connection's connected_changed signal is."""
        connection = self.manager.add(self.connection_name, self.connection_address, self.connection_port,
                         self.connection_type)
        self.manager.connections_changed.connect(self.set_triggered)
        connection.connected = False
        self.assertTrue(self.triggered)

    def test_destroyed_connections_changed_disconnected(self):
        """Test that a destroyed Connection's signals are properly disconnected from the ConnectionManager"""
        connection = self.manager.add(self.connection_name, self.connection_address, self.connection_port,
                         self.connection_type)
        self.manager.connections_changed.connect(self.set_triggered)
        self.manager.destroy(self.connection_name)
        self.triggered = False
        connection.connected = True
        self.assertFalse(self.triggered)


class HelperConnection(Connection):
    """Helper Connection class for testing ConnectionManager"""

    connected_changed = pyqtSignal(bool)

    def __init__(self, connection_ip, connection_port):
        super().__init__()
        self.__connection_ip = connection_ip
        self.__connection_port = connection_port
        self.__connected = False
        self.__client = None

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    @property
    def connected(self):
        return self.__connected

    @connected.setter
    def connected(self, value):
        self.__connected = value
        self.connected_changed.emit(value)

    def get_connected(self):
        return self.connected
