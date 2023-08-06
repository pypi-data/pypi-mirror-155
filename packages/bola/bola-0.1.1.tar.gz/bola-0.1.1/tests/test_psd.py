from bola import psd
import numpy as np
import pytest


def test_volume():
    V_box = 50 ** 3
    phi = 0.7

    gc = psd.n_largest(psd.GradingCurves.A16, 5)
    radii = psd.sample_grading_curve(gc, V_box * phi)

    V_sampled = psd.sphere_volume(radii)
    V_expected = (1 - gc[0][1]) * phi * V_box

    assert V_sampled == pytest.approx(V_expected)
    np.testing.assert_almost_equal(np.sort(radii)[::-1], radii)
