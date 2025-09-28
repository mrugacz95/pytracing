from math import tan

from matplotlib import pyplot as plt
import numpy as np
from tqdm.std import tqdm

from collisions import intersect
from math_utils import norm
from models import Camera, Sphere, Ray, Sun


def render(camera, objects, sun):
    framebuffer = np.zeros((camera.height, camera.width, 3))
    aspect_ratio = camera.width / float(camera.height)
    scale = tan(np.deg2rad(camera.fov * 0.5))

    for y_pixel in tqdm(range(camera.height)):
        for x_pixel in range(camera.width):

            x = (2 * (x_pixel + 0.5) / float(camera.width) - 1) * aspect_ratio * scale
            y = (1 - 2 * (y_pixel + 0.5) / float(camera.height)) * scale
            direction = np.array([x, y, -1])
            direction = direction / np.linalg.norm(direction)
            ray = Ray(camera.pos, direction)

            t, hit_obj = test_collision(ray, objects)
            if hit_obj is None:  # background
                full_color = np.array([0.5, 0.8, 1.0])
                framebuffer[y_pixel][x_pixel] = ((1 - full_color) * (np.array([y_pixel, y_pixel, 0])) /
                                                 float(camera.height) + full_color)
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
    width = 580
    height = 420
    camera = Camera(width=width, height=height, pos=np.array([0.0, 0.0, 0.0]), fov=75)

    sphere1 = Sphere(pos=np.array([0, 0, -1]), radius=0.5, color=np.array([1.0, 1.0, 0.0]))

    ground = Sphere(pos=np.array([0, -100.5, -1]), radius=100.0, color=np.array([0.0, 1.0, 0.2]))

    objects = [sphere1, ground]

    sun = Sun(pos=np.array([50, 50, 50]))

    img = render(camera, objects, sun)

    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
