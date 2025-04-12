import numpy as np
import pytest

import src.RandomMapGenerator


def test_rotateMap():
    small_map = np.array([[1, 2], [3, 4]])
    expected_result = np.array([[2, 4], [1, 3]])
    result = src.RandomMapGenerator.rotateMap(small_map)
    assert np.array_equal(result, expected_result)
