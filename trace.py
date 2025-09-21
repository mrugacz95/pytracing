from math import tan

from matplotlib import pyplot as plt
import numpy as np

from collisions import intersect
from math_utils import norm
from models import Camera, Sphere, Ray, Sun

WIDTH = 480
HEIGHT = 420


def render(camera, objects, sun):
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

            t, hit_obj = test_collision(ray, objects)
            if hit_obj is None:  # background
                framebuffer[y_pixel][x_pixel] = np.array(
                    [0.8 - (y_pixel / float(HEIGHT)) * 0.8,
                     0.8 - (y_pixel / float(HEIGHT)) * 0.8,
                     0.8]
                )
            else:
                # check shadow
                hit_point = ray.orig + ray.dir * t
                hit_point_normal = norm(hit_point - hit_obj.pos)
                light_dir = sun.pos - hit_point
                light_dir = norm(light_dir)
                light_ray = Ray(hit_point + light_dir * 0.00001, light_dir)  # add some bias to avoid self-intersection

                lt, light_collision_obj = test_collision(light_ray, objects)
                if light_collision_obj is not None:
                    framebuffer[y_pixel][x_pixel] = np.zeros(3)
                else:  # add smooth lighting
                    intensity = max(0, np.dot(light_dir, hit_point_normal))
                    framebuffer[y_pixel][x_pixel] = hit_obj.color * intensity

    return framebuffer


def test_collision(ray, objects):
    closest = float('inf')
    hit_obj = None
    for obj in objects:
        if isinstance(obj, Sphere):
            t = intersect(ray, obj)
            if t is not None and t < closest:
                closest = t
                hit_obj = obj
    return closest, hit_obj


def main():
    camera = Camera(pos=np.array([0.0, 0.0, -75.0]))

    sphere1 = Sphere(pos=np.array([1, 1, 25]), radius=4.5, color=np.array([1.0, 1.0, 0.0]))

    sphere2 = Sphere(pos=np.array([0, -15, -15]), radius=5.5, color=np.array([0.0, 0.0, 1.0]))

    sphere3 = Sphere(pos=np.array([3, -25, -25]), radius=2.5, color=np.array([1.0, 0.0, 0.0]))

    ground = Sphere(pos=np.array([103, 0, 0]), radius=100.0, color=np.array([0.0, 1.0, 0.2]))

    objects = [sphere1, sphere2, ground, sphere3]

    sun = Sun(pos=np.array([-50.0, -50.0, -100.0]))

    img = render(camera, objects, sun)

    plt.imshow(img)
    plt.show()

    # plt.imsave('test.png', img)


if __name__ == '__main__':
    main()
