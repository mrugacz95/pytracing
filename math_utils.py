# from https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection.html
from math import sqrt


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
