from math import sqrt
from scipy.stats import uniform_direction

import numpy as np


# from https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection.html
def solve_quadratic(a, b, c):
    discr = b * b - 4 * a * c
    if discr < 0:
        return None
    elif discr == 0:
        x0 = x1 = -0.5 * b / a
    else:
        if b > 0:
            q = -0.5 * (b + sqrt(discr))
        else:
            q = -0.5 * (b - sqrt(discr))
        x0 = q / a
        x1 = c / q
    if x0 > x1:
        x0, x1 = x1, x0
    return x0, x1


def norm(vec):
    return vec / float(np.linalg.norm(vec))


def sample_square():
    return np.random.rand(2) - 0.5


rng = np.random.default_rng()
uniform_sphere_dist = uniform_direction(3)


def random_on_hemisphere(normal):
    vec = uniform_sphere_dist.rvs(1, random_state=rng)[0]
    if np.dot(vec, normal) < 0:
        vec = -vec
    return vec


def near_zero(vec):
    return np.allclose(vec, np.zeros(3))


def reflect(vec, normal):
    return vec - 2 * np.dot(vec, normal) * normal