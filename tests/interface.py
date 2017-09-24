import pytest
from hmpy import Interface


def test_multiple_instances():
    """Test trying to create multiple instances of class Interface"""
    int1 = Interface()
    with pytest.raises(Exception):
        int2 = Interface()
