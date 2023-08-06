import bola.packing
import bola.psd
from bola._cpp import *
from bola import visu
import numpy as np


def main():
    grading = bola.psd.n_largest(bola.psd.GradingCurves.B16, 3)

    L = grading[-1][0] * 2

    box = Cube(L, L, L)
    phi = 0.6
    growth_rate = 0.1

    radii = bola.psd.sample_grading_curve(grading, box.volume() * phi)
    spheres = bola.packing.rsa(radii, box.l)

    sim = bola.packing.edmd(box, spheres, growth_rate=growth_rate)

    N = len(radii)
    v = visu.SphereVisualizer(N)
    v.add_box(*box.l)

    def update(t):
        sim.process(10 * N)
        if t % 10 == 0:
            sim.synchronize(True)
        sphere_matrix = sim.spheres()
        v.update_data(sphere_matrix)
        v.update_txt(bola.packing.stats_string(sim))

    animation = visu.Animation(v.window, update, dt=1)
    animation.start()

    print(f"Final particle distance = {growth_rate * sim.t()} mm")


if __name__ == "__main__":
    main()
