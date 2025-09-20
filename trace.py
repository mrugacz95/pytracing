from matplotlib import pyplot as plt
import numpy as np

from collisions import intersect
from models import Camera, Sphere, Ray

WIDTH = 20
HEIGHT = 20

OBJECTS = []


def main():
    camera = Camera()
    camera.pos = np.array([0.0, 0.0, -5.0])
    camera.dir = np.array([0.0, 0.0, 1.0])

    sphere = Sphere()
    sphere.radius = 9.5

    OBJECTS.append(sphere)

    img = np.zeros((HEIGHT, WIDTH, 3))

    y_offset = round(HEIGHT / 2)
    x_offset = round(WIDTH / 2)
    for y, pos_y in enumerate(range(-y_offset, y_offset)):
        for x, pos_x in enumerate(range(-x_offset, x_offset)):
            ray = Ray()
            ray.orig = camera.pos
            ray.dir = camera.dir
            ray.orig = ray.orig + np.array([pos_y, pos_x, 0.0])

            for obj in OBJECTS:
                if test_collision(ray, obj):
                    img[y][x] = obj.color

    plt.imshow(img)
    plt.show()


def test_collision(ray, obj):
    if isinstance(obj, Sphere):
        return intersect(ray, obj)
    raise ValueError("Unknown object type")


if __name__ == '__main__':
    main()
