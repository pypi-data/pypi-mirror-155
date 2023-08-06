import numpy as np
from itertools import cycle


def _sample_grading_class(d_min, d_max, V, chunk=100, seed=None):
    """
    seed:
        if None indicates that the user sets it.
    """
    radii = []
    sampled_volume = 0

    if seed is not None:
        np.random.seed(seed)

    while True:
        xs = np.random.random(chunk)
        rs = 0.5 * d_min * d_max / ((1 - xs) * d_max ** 3 + xs * d_min ** 3) ** (1 / 3)
        vs = sphere_volume(rs)

        if sampled_volume + vs < V:
            # Adding the particles will not yet reach the target volume, so we
            # can add them all at once
            sampled_volume += vs
            radii.append(rs)
        else:
            # Almost reached the target volume. Adding particles one by one.
            radii_tmp = []
            remaining_radii = cycle(rs)
            while sampled_volume < V:
                r = next(remaining_radii)
                sampled_volume += 4.0 / 3.0 * np.pi * r ** 3
                radii_tmp.append(r)
            radii.append(np.array(radii_tmp))
            break

    rs = np.concatenate(radii)
    rs_sort = np.sort(rs)
    return rs_sort[::-1]


def sphere_volume(rs, dr=0.0):
    """
    Given the radius list `rs`, computes the total sphere volume.
    """
    return 4.0 / 3.0 * np.pi * np.sum((np.asarray(rs) + dr) ** 3)


def sample_grading_curve(grading_curve, V, seed=6174, chunk=500):
    """
    Samples the radius distribution for a given grading curve consisting
    of N grading classes.

    grading_curve:
        list of N+1 tuples where the first entry defines the sieve diameter,
        the second one the relative volume fraction of particles passing that
        sieve. See some examples below.


    V:
        volume that is to be filled, usually the volume of the container
        multiplied by the particle volume fraction phi

        A box 4x3x2 with 50% particles would have V = 24 * 0.5 = 12
    seed:
        random seed
    """
    N = len(grading_curve) - 1
    diameters, volumes = zip(*grading_curve)

    V_check = 0.0
    for i_class in range(N):
        assert diameters[i_class] < diameters[i_class + 1]
        V_check += volumes[i_class + 1] - volumes[i_class]
    assert V_check < 1.0

    np.random.seed(6174)

    radii = []
    V_deviation = 0.0

    # The volume deviation is the difference between the expected volume after
    # sampling one class to the actual one. It is used to correct the
    # expected volume of the next class such that the total volume is matched
    # as close as possible.
    # As larger particles cause larger deviations (smaller number of samples
    # to reach the expected volume), we start at the largest grading class.
    # That way, the smaller classes can fix the sampling errors from the
    # larger ones. Thus, "reversed" below.
    for i_class in reversed(range(N)):
        d_min = diameters[i_class]
        d_max = diameters[i_class + 1]
        phi_class = volumes[i_class + 1] - volumes[i_class]

        V_expected = phi_class * V - V_deviation

        new_radii = _sample_grading_class(d_min, d_max, V_expected, chunk)

        V_deviation = sphere_volume(new_radii) - V_expected

        radii = np.append(radii, new_radii)

    return radii


class GradingCurves:
    """
    Taken from
    https://www.betontechnische-daten.de/de/2-7-1-kornzusammensetzung-sieblinien
    or DIN 1045-2
    """

    A8 = [
        (0.25, 0.05),
        (0.5, 0.14),
        (1.0, 0.21),
        (2.0, 0.36),
        (4.0, 0.61),
        (8.0, 1.0),
    ]
    B8 = [
        (0.25, 0.11),
        (0.5, 0.26),
        (1.0, 0.42),
        (2.0, 0.57),
        (4.0, 0.74),
        (8.0, 1.0),
    ]
    C8 = [
        (0.25, 0.21),
        (0.5, 0.39),
        (1.0, 0.57),
        (2.0, 0.71),
        (4.0, 0.85),
        (8.0, 1.0),
    ]

    A16 = [
        (0.25, 0.03),
        (0.5, 0.08),
        (1.0, 0.12),
        (2.0, 0.21),
        (4.0, 0.36),
        (8.0, 0.60),
        (16.0, 1.0),
    ]
    B16 = [
        (0.25, 0.08),
        (0.5, 0.20),
        (1.0, 0.32),
        (2.0, 0.42),
        (4.0, 0.56),
        (8.0, 0.76),
        (16.0, 1.0),
    ]
    C16 = [
        (0.25, 0.18),
        (0.5, 0.34),
        (1.0, 0.49),
        (2.0, 0.62),
        (4.0, 0.74),
        (8.0, 0.88),
        (16.0, 1.0),
    ]

    @staticmethod
    def fuller(d_min=4.0, d_max=16.0, q=0.5, N=None):
        if N is None:
            N = int(np.log2(d_max / d_min))

        diameters = np.geomspace(d_min, d_max, N + 1)
        volumes = [(d / d_max) ** q for d in diameters]

        return list(zip(diameters, volumes))


def n_largest(grading_curve, n):
    return grading_curve[-(n + 1) :]


def build_grading_curve(radii, V):
    r = np.array(radii[::-1])
    sphere_volumes = 4.0 / 3.0 * np.pi * r ** 3

    sieve_pass_volumes = np.cumsum(sphere_volumes)

    V_offset = V - sieve_pass_volumes[-1]
    return 2 * r, (sieve_pass_volumes + V_offset) / V
