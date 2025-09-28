import numpy as np


class Ray:
    orig = np.zeros(3)
    dir = np.zeros(3)

    def __init__(self, orig=np.zeros(3), dir=orig):
        self.orig = orig
        self.dir = dir


class HitRecord:
    def __init__(self, p, normal, t, front_face, material):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.material = material


class Sun:
    pos = np.zeros(3)

    def __init__(self, pos=np.zeros(3)):
        self.pos = pos
