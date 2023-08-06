import bola.packing
import bola.psd
from bola._cpp import *
import bola.mesh
import numpy as np


def main():
    grading = bola.psd.n_largest(bola.psd.GradingCurves.B16, 3)

    L = grading[-1][0] * 3

    box = Cube(L, L, L)
    phi = 0.6
    growth_rate = 0.1

    radii = bola.psd.sample_grading_curve(grading, box.volume() * phi)
    spheres = bola.packing.rsa(radii, box.l)

    sim = bola.packing.edmd(box, spheres)

    N = len(radii)
    for i in range(10):
        sim.process(100 * N)
        sim.synchronize(True)
        print(bola.packing.stats_string(sim), flush=True)

    # use new sphere positions from edmd but the old radii
    spheres = sim.spheres()
    spheres[:, 3] = radii

    dist = 2 * sim.t() * growth_rate
    bola.mesh.create(
        box,
        spheres,
        bola.mesh.GmshOptions(
            zslice=16,
            mesh_size_matrix=dist,
            mesh_size_aggregates=dist,
            out="stuff.xdmf",
        ),
        show=True,
    )


if __name__ == "__main__":
    main()
