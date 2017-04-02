class ConnectionManager(object):
    """Manages and controls access to all PLC Connections."""

    def __init__(self):
        """Initialize connection manager."""
        self.__connections = {}

    def connect(self, name, address, port, connection_type):
        """Add and initialize a new connection.

        :param name: Name of connection.
        :param address: Address to connect to.
        :param port: Port to connect on.
        :param connection_type: SubClass of Connection.
        :return: Instance of connection_type.
        :raise ValueError: When a connection already exists with the same name.
        """
        if self.has_connection(name):
            raise ValueError("A connection already exists with that name")

        connection = connection_type(address, port)
        connection.connect()
        self.__connections[name] = connection
        return connection

    def disconnect(self, name):
        """Terminate/remove a connection by name.

        :param name: Name of the connection to terminate.
        :raise ValueError: name does not match any existing connections
        """
        if not self.has_connection(name):
            raise ValueError("No connection exists with that name")

        self.__connections[name].disconnect()
        del self.__connections[name]

    def disconnect_all(self):
        """Terminate/remove all connections."""
        for key in list(self.__connections.keys()):
            self.disconnect(key)

    def get_connection(self, name):
        """Get a connection by name

        :param name: Name of the connection to return.
        :return: Connection object or None.
        """
        return self.__connections.get(name)

    def has_connection(self, name):
        """Check if a connection exists by name

        :param name: Name to check.
        :return: True if connection with name exists, False otherwise."""
        return name in self.__connections