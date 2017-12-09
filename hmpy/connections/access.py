import pyodbc;

PREFERRED_DRIVER = 'Microsoft Access Driver (*.mdb, *.accdb)'
INCOMPATIBLE_DRIVERS_ERROR = "Only available 'Microsoft Access Driver's are outdated dont not support .accdb files"
MISSING_DRIVERS_ERROR = "No 'Microsoft Access Driver's found"

class AccessConnection:

    def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError("positional argument 'path' must be of type str")
        self._path = path

        self._driver = self._find_driver()

        self._connection = pyodbc.connect('DRIVER={%s};DBQ=%s;' % (self._driver, self._path))
        self._cursor = self._connection.cursor()

    def _find_driver(self):
        drivers = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
        drivers.remove(PREFERRED_DRIVER)
        fallback = None

        for driver in drivers:
            if driver == PREFERRED_DRIVER:
                return driver
            else:
                fallback = driver

        if fallback is None:
            raise EnvironmentError(MISSING_DRIVERS_ERROR)

        if self._path.split('.')[-1] != 'mdb':
            raise EnvironmentError(INCOMPATIBLE_DRIVERS_ERROR)

        return fallback;


    def get_table_info(self):
        return self._cursor.tables(tableType='TABLE')