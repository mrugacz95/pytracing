import numpy as np


class Camera:
    pos = np.zeros(3)
    dir = np.array([0.0, 0.0, 1.0])
    fov = 60

    def __init__(self, pos=np.zeros(3), dir=np.array([0.0, 0.0, 1.0]), fov=60):
        self.pos = pos
        self.dir = dir
        self.fov = fov


class Sphere:
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


class Sun:
    pos = np.zeros(3)

    def __init__(self, pos=np.zeros(3)):
        self.pos = pos