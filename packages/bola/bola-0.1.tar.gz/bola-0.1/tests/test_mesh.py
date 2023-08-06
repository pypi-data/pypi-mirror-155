from bola.mesh import create, GmshOptions
from tempfile import TemporaryDirectory
from pathlib import Path


def run(filename, zslice=None):
    spheres = [
        (0.25, 0.25, 0.5, 0.2),
        (0.25, 0.75, 0.5, 0.1),
        (0.75, 0.75, 0.5, 0.2),
        (0.75, 0.25, 0.5, 0.1),
    ]

    box = (1, 1, 1)

    with TemporaryDirectory() as tmp:
        p = Path(tmp) / filename
        create(box, spheres, GmshOptions(out=str(p), zslice=zslice))

        assert p.exists()


def test_2d_msh():
    run("stuff2d.msh")


def test_3d_xdmf():
    run("stuff3d.xdmf", zslice=0.35)
