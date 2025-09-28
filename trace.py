import numpy as np
from matplotlib import pyplot as plt

from camera import Camera
from hittable import Sphere
from material import Lambertian
from models import Sun


def main():
    width = 580
    height = 420
    camera = Camera(width=width, height=height, pos=np.array([0.0, 0.0, 0.0]), fov=75)

    sphere1 = Sphere(pos=np.array([0, 0, -1]), radius=0.5, material=Lambertian(np.array([0.5, 0.5, 0.0])))

    ground = Sphere(pos=np.array([0, -100.5, -1]), radius=100.0, material=Lambertian(np.array([0.0, 0.5, 0.1])))

    objects = [sphere1, ground]

    sun = Sun(pos=np.array([50, 50, 50]))

    img = camera.render(objects, sun)

    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
