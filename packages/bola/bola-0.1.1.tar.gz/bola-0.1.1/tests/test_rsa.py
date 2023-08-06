from bola.packing import rsa
import numpy as np
import pytest


def test_rsa():
    phi = 0.3
    N = 1000
    r = np.ones(N) * (phi * 3 / (4 * N * np.pi)) ** (1 / 3)

    print(4 / 3 * np.pi * np.sum(r ** 3))
    spheres, tries = rsa(r, n_tries=100000, ret_tries=True)

    assert spheres is not None
    assert spheres.shape == (N, 4)

    print("Average number of tries:", np.average(tries))


def test_negative_radius():
    with pytest.raises(Exception):
        spheres = rsa(radii=[0.1, 0.1, -0.1])


def test_negative_box_dimension():
    with pytest.raises(Exception):
        spheres = rsa(radii=[0.1, 0.1, 0.1], l=(1, 1, -1))


def test_unsorted():
    spheres = rsa(radii=[0.01, 0.2, 0.1])
    np.testing.assert_almost_equal(spheres[:, 3], [0.2, 0.1, 0.01])
