from . import _cpp
import numpy as np
import math


def rsa(
    radii,
    l=(
        1.0,
        1.0,
        1.0,
    ),
    n_tries=10000,
    seed=6174,
    ret_tries=False,
    progress=True,
):
    """
    Random sequential addition algorithm to place spheres in a box without
    overlaps as described in [1]_ and [2]_.

    Parameters
    ----------
    radii : ndarray, shape (n,)
        List of ``n`` sphere radii (> 0) to place. The radii are sorted by
        size before adding them.

    l : array_like, shape (3,)
        Box dimensions. The box then goes from (0,0,0) to *l,
        thus, (l[0], l[1], l[2]).

    n_tries : int
        Maximum number of allowed failed overlap checks before the algorithm
        terminates.

    seed : int
        Seed of the random number generator.

    ret_tries : bool
        If true, also returns the number of tries it took to place each sphere.

    progress : bool
        If true, shows a simple progress bar.

    Returns
    -------
    spheres : array_like, shape (n,4)
        Sphere matrix where each row contains [x, y, z, r]. Due to sorting by
        size, the order w.r.t. the input ``radii`` may change!

    tries : optional, array_like, shape (n,)
        Only returned with the ``ret_tries`` flag set.

    References
    ----------

    .. [1] Widom, B., 1966.
           Random sequential addition of hard spheres to a volume.
           The Journal of Chemical Physics, 44(10), pp.3888-3894.

    .. [2] Titscher, T. and Unger, J.F., 2015.
           Application of molecular dynamics simulations for the generation
           of dense concrete mesoscale geometries.
           Computers & Structures, 158, pp.274-284.

    Example
    -------
    Placing N=1000 monodisperse (equal size) spheres of radius R=0.1 in a
    LxLxL box with L=3.

    >>> from bola.packing import rsa
    >>> import numpy as np
    >>> N, R, L = 1000, 0.1, 3.
    >>> radii = np.full(N, R)
    >>> spheres = rsa(radii, (L, L, L))

    With vtk installed, you can have a look at the resulting packing
    >>> show(spheres, (L, L, L))

    """
    radii = np.asarray(radii)
    assert np.all(radii > 0.0)
    assert np.all(np.asarray(l) > 0.0)

    r_sort = -np.sort(-radii)  # small hack to sort reversed

    b = _cpp.Cube(*l)
    spheres, tries = _cpp.rsa(r_sort, b, seed, n_tries, progress)

    if ret_tries:
        return spheres, tries
    else:
        return spheres


def maxwell_boltzmann_velocities(n, temperature=273.15, seed=6174):
    """
    Velocities according to a maxwell-Boltzmann distribution in three
    dimensions. This is a good initial velocity for the EDMD algorithm.

    Parameters
    ----------
    n : int
        Number of velocities to generate.
    temperature : float
        Assumed temperature of the gas.
    seed : int
        Seed of the random number generator.

    Returns
    -------

    vs : ndarray, shape (n,3)
        Matrix of velocities where each of the ``n`` rows corresponds to the
        velocity components (v_x, v_y, v_z).
    """

    mb = _cpp.MaxwellBoltzmann(6174)
    vs = np.empty((n, 3))
    for v in vs:
        v = mb(temperature)
    return vs


def edmd(box, spheres, velocity=None, growth_rate=0.1, mass=1.0):
    """
    Event-driven molecular-dynamic (EDMD) simulation to grow (polydisperse)
    spheres in a box.

    All spheres move according to free-flight dynamics and grow over time.
    EDMD subsequently predicts and performs the next (closest in time)
    collision with another sphere or the box. See [1]_, [2]_ and especially
    [3]_ for details.

    References
    ----------
    .. [1] Lubachevsky, B.D. and Stillinger, F.H., 1990.
           Geometric properties of random disk packings.
           Journal of statistical Physics, 60(5), pp.561-583.

    .. [2] Donev, A., Torquato, S., Stillinger, F.H. and Connelly, R., 2004.
           Jamming in hard sphere and disk packings.
           Journal of applied physics, 95(3), pp.989-999.

    .. [3] Titscher, T. and Unger, J.F., 2015.
           Application of molecular dynamics simulations for the generation
           of dense concrete mesoscale geometries.
           Computers & Structures, 158, pp.274-284.
    """
    N = len(spheres)
    if velocity is None:
        velocity = maxwell_boltzmann_velocities(N)
    else:
        assert velocity.shape == (N, 3)

    if isinstance(growth_rate, float):
        growth_rate = np.full(N, growth_rate)
    else:
        assert len(growth_rate) == N

    if isinstance(mass, float):
        mass = np.full(N, mass)
    else:
        assert len(mass) == N

    sim = _cpp.Simulation(box, spheres, velocity, growth_rate, mass)
    return sim


def stats_string(sim):
    def human_format(number):
        """
        thanks to https://stackoverflow.com/a/45478574
        """
        units = ["", "K", "M", "G", "T", "P"]
        k = 1000.0
        magnitude = int(math.floor(math.log(number, k)))
        return "{:5.2f}{}".format(number / k ** magnitude, units[magnitude])

    info = "{:.4%} | ".format(sim.stats.pf)
    info += human_format(sim.stats.n_events) + " events | "
    info += "{:.2E} | ".format(sim.stats.collisionrate)
    info += "{:5.3f}s ".format(sim.t())
    return info


def show(spheres, box):
    from . import visu

    try:
        l = box.l
    except AttributeError:
        l = box

    v = visu.SphereVisualizer(len(spheres))
    v.add_box(*l)

    v.update_data(spheres[:, :3], spheres[:, 3])
    v.show()
