import gmsh
from pathlib import Path
import numpy as np

geo = gmsh.model.geo


from dataclasses import dataclass


def _rectangle(xs, xe, mesh_size=0.1):
    """
    _rectangle from start point `xs` to end point `xe` with a
    given `mesh_size`.
    """
    ms = mesh_size
    p0 = geo.add_point(xs[0], xs[1], 0, ms)
    p1 = geo.add_point(xe[0], xs[1], 0, ms)
    p2 = geo.add_point(xe[0], xe[1], 0, ms)
    p3 = geo.add_point(xs[0], xe[1], 0, ms)

    l0 = geo.add_line(p0, p1)
    l1 = geo.add_line(p1, p2)
    l2 = geo.add_line(p2, p3)
    l3 = geo.add_line(p3, p0)

    loop = gmsh.model.geo.add_curve_loop([l0, l1, l2, l3])
    return loop


def _cuboid(xs, xe, mesh_size=0.1):
    """
    _cuboid from start point `xs` to end point `xe` with a
    given `mesh_size`.
    """
    ms = mesh_size
    # top points: z = ze
    p0 = geo.add_point(xs[0], xs[1], xe[2], ms)
    p1 = geo.add_point(xs[0], xe[1], xe[2], ms)
    p2 = geo.add_point(xe[0], xe[1], xe[2], ms)
    p3 = geo.add_point(xe[0], xs[1], xe[2], ms)
    # bottom points z = zs
    p4 = geo.add_point(xs[0], xs[1], xs[2], ms)
    p5 = geo.add_point(xs[0], xe[1], xs[2], ms)
    p6 = geo.add_point(xe[0], xe[1], xs[2], ms)
    p7 = geo.add_point(xe[0], xs[1], xs[2], ms)

    # top lines z = zs
    lT0 = geo.add_line(p0, p1)
    lT1 = geo.add_line(p1, p2)
    lT2 = geo.add_line(p2, p3)
    lT3 = geo.add_line(p3, p0)
    # bottom lines z = ze
    lB0 = geo.add_line(p4, p5)
    lB1 = geo.add_line(p5, p6)
    lB2 = geo.add_line(p6, p7)
    lB3 = geo.add_line(p7, p4)
    # connection zs --> ze
    lC0 = geo.add_line(p0, p4)
    lC1 = geo.add_line(p1, p5)
    lC2 = geo.add_line(p2, p6)
    lC3 = geo.add_line(p3, p7)

    # lineloops and surfaces
    s0 = geo.add_plane_surface([geo.add_curve_loop([-lT3, lC3, lB3, -lC0])])
    s1 = geo.add_plane_surface([geo.add_curve_loop([-lT1, lC1, lB1, -lC2])])
    s2 = geo.add_plane_surface([geo.add_curve_loop([-lT0, lC0, lB0, -lC1])])
    s3 = geo.add_plane_surface([geo.add_curve_loop([-lT2, lC2, lB2, -lC3])])
    s4 = geo.add_plane_surface([geo.add_curve_loop([lT0, lT1, lT2, lT3])])
    s5 = geo.add_plane_surface([geo.add_curve_loop([-lB3, -lB2, -lB1, -lB0])])

    return geo.add_surface_loop([s0, s1, s2, s3, s4, s5])


def _circle(xc, r, mesh_size=0.1):
    """
    geo.add_circle_arc with center `xc`, radius `r` and a given `mesh_size`.
    """
    ms = mesh_size
    p0 = gmsh.model.geo.add_point(xc[0], xc[1], 0, ms)
    p1 = gmsh.model.geo.add_point(xc[0] + r, xc[1], 0, ms)
    p2 = gmsh.model.geo.add_point(xc[0] - r, xc[1], 0, ms)

    c0 = gmsh.model.geo.add_circle_arc(p1, p0, p2)
    c1 = gmsh.model.geo.add_circle_arc(p2, p0, p1)

    loop = gmsh.model.geo.add_curve_loop([c0, c1])
    surface = gmsh.model.geo.add_plane_surface([loop])

    return loop, surface


def _sphere(xc, r, mesh_size=0.1):
    """
    _sphere with center `xc`, radius `r` and a given `mesh_size`.
    """
    ms = mesh_size
    p0 = geo.add_point(xc[0], xc[1], xc[2], ms)
    p1 = geo.add_point(xc[0] + r, xc[1], xc[2], ms)
    p2 = geo.add_point(xc[0], xc[1] + r, xc[2], ms)
    p3 = geo.add_point(xc[0], xc[1], xc[2] + r, ms)
    p4 = geo.add_point(xc[0] - r, xc[1], xc[2], ms)
    p5 = geo.add_point(xc[0], xc[1] - r, xc[2], ms)
    p6 = geo.add_point(xc[0], xc[1], xc[2] - r, ms)

    c0 = geo.add_circle_arc(p1, p0, p6)
    c1 = geo.add_circle_arc(p6, p0, p4)
    c2 = geo.add_circle_arc(p4, p0, p3)
    c3 = geo.add_circle_arc(p3, p0, p1)
    c4 = geo.add_circle_arc(p1, p0, p2)
    c5 = geo.add_circle_arc(p2, p0, p4)
    c6 = geo.add_circle_arc(p4, p0, p5)
    c7 = geo.add_circle_arc(p5, p0, p1)
    c8 = geo.add_circle_arc(p6, p0, p2)
    c9 = geo.add_circle_arc(p2, p0, p3)
    c10 = geo.add_circle_arc(p3, p0, p5)
    c11 = geo.add_circle_arc(p5, p0, p6)

    s0 = geo.add_surface_filling([geo.add_curve_loop([c4, c9, c3])])
    s1 = geo.add_surface_filling([geo.add_curve_loop([c8, -c4, c0])])
    s2 = geo.add_surface_filling([geo.add_curve_loop([c11, -c7, -c0])])
    s3 = geo.add_surface_filling([geo.add_curve_loop([c7, -c3, c10])])
    s4 = geo.add_surface_filling([geo.add_curve_loop([-c9, c5, c2])])
    s5 = geo.add_surface_filling([geo.add_curve_loop([-c10, -c2, c6])])
    s6 = geo.add_surface_filling([geo.add_curve_loop([-c1, -c6, -c11])])
    s7 = geo.add_surface_filling([geo.add_curve_loop([-c5, -c8, c1])])

    loop = geo.add_surface_loop([s0, s1, s2, s3, s4, s5, s6, s7])
    volume = geo.add_volume([loop])

    return loop, volume


@dataclass
class GmshOptions:
    order: int = 2

    interface_thickness: float = 0.0
    mesh_size_matrix: float = 0.05
    mesh_size_aggregates: float = 0.05

    alg2D: int = 1
    alg3D: int = 1
    recombine_alg: int = 0
    optimize: int = 2
    smoothing: int = 2

    phys_group_matrix = "Matrix"
    phys_group_aggregates = "Aggregates"
    phys_group_interfaces = "Interfaces"

    zslice: None = None
    zslice_rmin: float = None

    out: str = "out.msh"

    @property
    def dim(self):
        return 3 if self.zslice is None else 2

    def apply(self):
        gmsh.option.set_number("Mesh.ElementOrder", self.order)
        gmsh.option.set_number("Mesh.RecombinationAlgorithm", self.recombine_alg)
        gmsh.option.set_number("Mesh.Algorithm", self.alg2D)
        gmsh.option.set_number("Mesh.Algorithm3D", self.alg3D)
        gmsh.option.set_number("Mesh.Optimize", self.optimize)
        gmsh.option.set_number("Mesh.Smoothing", self.smoothing)


def _slice(spheres, z, rmin):
    s = np.asarray(spheres)
    # x and y stay when sliced, only the radius needs adaptation
    circles = s[:, (0, 1, 3)]
    circles[:, 2] = 0

    delta_z = np.abs(s[:, 2] - z)
    new_r_squared = s[:, 3] ** 2 - delta_z ** 2
    valid = new_r_squared > 0
    circles[valid, 2] = np.sqrt(new_r_squared[valid])

    valid_circles = circles[:, 2] > rmin
    if not np.any(valid_circles):
        raise RuntimeError(
            f"The slice at z={z} contained no cirlces (above rmin={rmin})!"
        )

    return circles[valid_circles]


def _write_mesh(out):
    out = Path(out)
    outmsh = out.with_suffix(".msh")

    gmsh.write(str(outmsh))

    if out.suffix != ".msh":
        # try to convert it using meshio
        import meshio

        mesh = meshio.read(outmsh)
        mesh.write(out)


def create(box, spheres, opts=GmshOptions(), show=False):
    try:
        l = box.l
    except AttributeError:
        l = box
    gmsh.initialize()

    if opts.zslice is None:
        matrix = _cuboid((0, 0, 0), l, mesh_size=opts.mesh_size_matrix)

        ls = [
            _sphere(c[:3], c[3], mesh_size=opts.mesh_size_aggregates) for c in spheres
        ]
        loops, surfaces = zip(*ls)
        matrix_volume = gmsh.model.geo.add_volume([matrix] + list(loops))

    else:
        assert 0 < opts.zslice < l[2]
        circles = _slice(
            spheres, opts.zslice, opts.zslice_rmin or opts.mesh_size_aggregates
        )

        matrix = _rectangle((0, 0), (l[0], l[1]), mesh_size=opts.mesh_size_matrix)
        ls = [
            _circle(c[:2], c[2], mesh_size=opts.mesh_size_aggregates) for c in circles
        ]
        loops, surfaces = zip(*ls)
        matrix_volume = gmsh.model.geo.add_plane_surface([matrix] + list(loops))

    gmsh.model.geo.add_physical_group(
        dim=opts.dim, tags=[matrix_volume], name=opts.phys_group_matrix
    )
    gmsh.model.geo.add_physical_group(
        dim=opts.dim, tags=surfaces, name=opts.phys_group_aggregates
    )

    gmsh.model.geo.synchronize()
    opts.apply()
    gmsh.model.mesh.generate(opts.dim)

    _write_mesh(opts.out)

    if show:
        gmsh.fltk.run()

    gmsh.finalize()
