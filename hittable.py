from abc import ABC, abstractmethod

import numpy as np

from math_utils import norm, solve_quadratic
from models import HitRecord, Ray


class Hittable(ABC):
    @abstractmethod
    def hit(self, ray, t_min, t_max):
        pass


class Sphere(Hittable):
    pos = np.zeros(3)
    radius = 1.0

    def __init__(self, pos, radius, material):
        self.pos = pos
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min, t_max):
        t = self.intersect(ray)
        if t is not None and t_min < t < t_max:
            hit_point = ray.orig + ray.dir * t
            hit_point_normal = norm(hit_point - self.pos)
            return HitRecord(
                p=hit_point,
                normal=hit_point_normal,
                t = t,
                front_face = np.dot(hit_point - self.pos, ray.dir) < 0,
                material = self.material
            )
        return None

    def intersect(self, ray: Ray):
        L = ray.orig - self.pos
        a = ray.dir.dot(ray.dir)
        b = 2 * ray.dir.dot(L)
        c = L.dot(L) - self.radius * self.radius
        solution = solve_quadratic(a, b, c)
        if solution is None:
            return None

        t0, t1 = solution

        if t0 > t1:
            t0, t1 = t1, t0

        if t0 < 0:
            t0 = t1
            if t0 < 0:
                return None
        t = t0
        return t
