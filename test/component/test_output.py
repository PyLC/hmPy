import unittest
from hmpy.connection import Connection
from hmpy.component.output import Output

class TestOutput(unittest.TestCase):
    """Tests the Output class"""

    def setUp(self):
        """Initialize a connection for the test."""
        self.connection = TestConnection()
        self.succeeded = False

    def succeed(self):
        """Helper slot method. Sets class attribute succeeded to True when invoked."""
        self.succeeded = True

    def test_write(self):
        """Test that changing the output value triggers a write on the connection with the appropriate values"""
        register = Connection.COIL
        address = 0
        value = 1
        self.output = Output(register, address, self.connection)
        self.output.value = value;
        self.assertEquals(self.connection.value, 1)
        self.assertEquals(self.connection.register, register)
        self.assertEquals(self.connection.address, address)

    # TODO tests - invalid connection, invalid register types, addresses?


class TestConnection(Connection):
    """Mock connection implementation for use in tests."""

    def __init__(self):
        """Initialize mock connection."""
        super().__init__()
        self.connected = True
        self.value = None
        self.address = None
        self.register = None

    def write(self, register_type, address, value):
        """Simple read implementation, returns own value attribute."""
        self.value = value
        self.address = address
        self.register = register_type