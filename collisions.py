from math_utils import solve_quadratic
from models import Ray, Sphere


def intersect(ray: Ray, sphere: Sphere):
    L = ray.orig - sphere.center
    a = ray.dir.dot(ray.dir)
    b = 2 * ray.dir.dot(L)
    c = L.dot(L) - sphere.radius * sphere.radius
    solution = solve_quadratic(a, b, c)
    if solution is None:
        return False

    t0, t1 = solution

    if t0 > t1:
        t0, t1 = t1, t0

    if t0 < 0:
        t0 = t1
        if t0 < 0:
            return False
    t = t0
    return True
