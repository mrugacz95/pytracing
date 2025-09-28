import abc
from abc import ABC

import numpy as np


class Camera:
    pos = np.zeros(3)
    dir = np.array([0.0, 0.0, 1.0])
    fov = 60

    def __init__(self, width, height, pos=np.zeros(3), dir=np.array([0.0, 0.0, 1.0]), fov=60):
        self.pos = pos
        self.dir = dir
        self.fov = fov
        self.width = width
        self.height = height


class Hittable(ABC):
    @abc.abstractmethod
    def hit(self, ray, t_min, t_max):
        pass


class Sphere(Hittable):
    def hit(self, ray, t_min, t_max):
        pass

    pos = np.zeros(3)
    radius = 1.0
    color = np.array([1.0, 1.0, 0.0])

    def __init__(self, pos=np.zeros(3), radius=1.0, color=np.array([1.0, 1.0, 1.0])):
        self.pos = pos
        self.radius = radius
        self.color = color


class Ray:
    orig = np.zeros(3)
    dir = np.zeros(3)

    def __init__(self, orig=np.zeros(3), dir=orig):
        self.orig = orig
        self.dir = dir


class HitRecord:
    def __init__(self, p, normal, t, front_face):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face


class Sun:
    pos = np.zeros(3)

    def __init__(self, pos=np.zeros(3)):
        self.pos = pos
