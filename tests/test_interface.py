import pytest
from hmpy import Interface


@pytest.fixture(scope="module")
def interface():
    intf = Interface()
    yield intf
    intf = None


def test_multiple_instances(interface):
    """Test trying to create multiple instances of class Interface"""
    with pytest.raises(Exception):
        int2 = Interface()
