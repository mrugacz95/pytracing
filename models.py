import numpy as np


class Camera():
    pos = np.zeros(3)
    dir = np.array([0.0,0.0,1.0])
    fov = 60

class Sphere():
    center = np.zeros(3)
    radius = 1.0
    color = np.array([1.0,1.0,0.0])

class Ray():
    orig = np.zeros(3)
    dir = np.zeros(3)

