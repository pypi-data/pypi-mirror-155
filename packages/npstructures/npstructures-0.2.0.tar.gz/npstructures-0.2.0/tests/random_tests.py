import numpy as np
import pytest
from npstructures import RaggedArray


@pytest.fixture
def random_array():
    shape = tuple(np.random.randint(1, 100, 2))
    return np.random.rand(shape[0] * shape[1]).reshape(shape)


def test_cumsum(random_array):
    ra = RaggedArray.from_numpy_array(random_array)
    cm = np.cumsum(ra, axis=-1)
    assert np.all(cm.to_numpy_array(cm) == np.cumsum(random_array))
