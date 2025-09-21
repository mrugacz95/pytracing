from math import tan

from matplotlib import pyplot as plt
import numpy as np

from collisions import intersect
from models import Camera, Sphere, Ray

WIDTH = 280
HEIGHT = 200


def render(camera, objects):

    framebuffer = np.zeros((HEIGHT, WIDTH, 3))
    aspect_ratio = WIDTH / float(HEIGHT)
    scale = tan(np.deg2rad(camera.fov * 0.5))

    for y_pixel in range(HEIGHT):
        for x_pixel in range(WIDTH):

            x = (2 * (y_pixel + 0.5) / float(WIDTH) - 1) * aspect_ratio * scale
            y = (1 - 2 * (x_pixel + 0.5) / float(HEIGHT)) * scale
            direction = np.array([x, y, 1])
            direction = direction / np.linalg.norm(direction)
            ray = Ray(camera.pos, direction)


            for obj in objects:
                if test_collision(ray, obj):
                    framebuffer[y_pixel][x_pixel] = obj.color

    return framebuffer

def test_collision(ray, obj):
    if isinstance(obj, Sphere):
        return intersect(ray, obj)
    raise ValueError("Unknown object type")


def main():
    camera = Camera(pos=np.array([0.0, 0.0, -35.0]))

    sphere1 = Sphere(radius=9.5, color=np.array([1.0, 1.0, 0.0]))

    sphere2 = Sphere(pos=np.array([3, 4, -12]), radius=9.5, color=np.array([0.0, 0.0, 1.0]))

    objects = [sphere1, sphere2]

    img = render(camera, objects)

    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
