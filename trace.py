from matplotlib import pyplot as plt
import numpy as np

from collisions import intersect
from models import Camera, Sphere, Ray

WIDTH = 28
HEIGHT = 20


def render(camera, objects):
    img = np.zeros((HEIGHT, WIDTH, 3))

    y_offset = round(HEIGHT / 2)
    x_offset = round(WIDTH / 2)
    for y, pos_y in enumerate(range(-y_offset, y_offset)):
        for x, pos_x in enumerate(range(-x_offset, x_offset)):
            ray = Ray()
            ray.orig = camera.pos
            ray.dir = camera.dir
            ray.orig = ray.orig + np.array([pos_y, pos_x, 0.0])

            for obj in objects:
                if test_collision(ray, obj):
                    img[y][x] = obj.color

    return img

def test_collision(ray, obj):
    if isinstance(obj, Sphere):
        return intersect(ray, obj)
    raise ValueError("Unknown object type")


def main():
    camera = Camera(pos=np.array([0.0, 0.0, -15.0]))

    sphere1 = Sphere(radius=9.5, color=np.array([1.0, 1.0, 0.0]))

    sphere2 = Sphere(pos=np.array([3, 4, -12]), radius=9.5, color=np.array([0.0, 0.0, 1.0]))

    objects = [sphere1, sphere2]

    img = render(camera, objects)

    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
