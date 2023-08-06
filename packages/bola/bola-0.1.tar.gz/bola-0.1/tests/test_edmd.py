from bola._cpp import *
import numpy as np
import pytest


def test_cpp_sphere_collision():
    s1 = Sphere()
    s1.x = [0, 0, 0]
    s1.v = [1, 1, 1]
    s1.r = 1.0

    s2 = Sphere()
    s2.x = [5, 5, 5]
    s2.v = [0, 0, 0]
    s2.r = 0.42
    s2.gr = 0.1

    effective_distance = np.linalg.norm(s2.x - s1.x) - (s2.r + s1.r)
    effective_velocity = np.linalg.norm(s1.v) + s2.gr

    e = s1.predict_collision(s2)
    assert e.t == pytest.approx(effective_distance / effective_velocity)


def test_cpp_wall_collision():
    s = Sphere()
    s.x = [4, 5, 5]
    s.v = [0.1, 0, 0]
    s.r = 1.0
    s.gr = 0.42

    box = Cube(10, 10, 10)

    effective_distance = 6 - s.r
    effective_velocity = np.linalg.norm(s.v) + s.gr

    e = box.predict_collision(s)
    assert e.t == pytest.approx(effective_distance / effective_velocity)
