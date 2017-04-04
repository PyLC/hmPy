import unittest
import sys
from hmpy.connection import Connection
from hmpy.component.input import Input
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)


class TestInput(unittest.TestCase):
    """Tests the ComponentManager class"""

    def setUp(self):
        """Initialize a connection for the test."""
        self.connection = TestConnection()
        self.interval = 100
        self.succeeded = False

    def succeed(self):
        """Helper slot method. Sets class attribute succeeded to True when invoked."""
        self.succeeded = True

    def test_trigger_changed(self):
        """Test that the valueChanged signal is emitted when the value is changed."""
        self.input = Input(self.interval, Connection.READ_COIL, 0, self.connection)
        self.input.valueChanged.connect(self.succeed)
        self.connection.value = True
        QTest.qWait(self.interval * 5)

        self.assertTrue(self.succeeded)

    def test_trigger_not_changed(self):
        """Test that the valueChanged signal is not emitted when the value does not change."""
        self.input = Input(self.interval, Connection.READ_COIL, 0, self.connection)
        self.input.valueChanged.connect(self.succeed)

        QTest.qWait(self.interval * 5)

        self.assertFalse(self.succeeded)

    def test_read_coil(self):
        """Test that the input read has the correct value."""
        self.input = Input(self.interval, Connection.READ_COIL, 0, self.connection)
        self.connection.value = True
        QTest.qWait(self.interval * 5)
        self.assertTrue(self.input.value)

    # TODO tests - invalid connection, invalid register types, addresses?, invalid interval


class TestConnection(Connection):
    """Mock connection implementation for use in tests."""

    def __init__(self):
        """Initialize mock connection."""
        super().__init__()
        self.connected = True
        self.value = None

    def read(self, register_type, address, count):
        """Simple read implementation, returns own value attribute."""
        return self.value