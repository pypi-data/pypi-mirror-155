import numpy as np
from bola._cpp import Cube
import bola.packing
from bola import visu


def main():
    box = Cube(10, 10, 10)

    # 5 spheres in the middle, three of which are "loaded"
    spheres = np.array(
        [
            [1.0, 5.0, 5.0, 0.5],
            [2.0, 5.0, 5.0, 0.5],
            [3.0, 5.0, 5.0, 0.5],
            [6.0, 5.0, 5.0, 0.5],
            [7.0, 5.0, 5.0, 0.5],
        ]
    )

    N = len(spheres)
    vel = np.zeros((N, 3))
    vel[0, 0] = 1
    vel[1, 0] = 1
    vel[2, 0] = 1

    v = visu.SphereVisualizer(N)
    v.add_box(*box.l)
    v.update_txt(
        "Note that we can only visualize discrete events \nand no continuous motion... \n ... and you need to imagine the cables :P"
    )

    sim = bola.packing.edmd(box, spheres, vel, growth_rate=0.0)

    def update(_):
        sim.process(1)
        v.update_data(sim.spheres())

    animation = visu.Animation(v.window, update)
    animation.start()


if __name__ == "__main__":
    main()
