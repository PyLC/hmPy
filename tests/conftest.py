import pytest
from functools import partial


def assert_called_around(self, target, distance=1):
    # Helper method for mock fixture
    assert target - distance <= self.call_count <= target + distance


@pytest.fixture(scope="function")
def mock(mocker):
    stub = mocker.stub()
    stub.assert_called_around = partial(assert_called_around, stub)
    return stub
