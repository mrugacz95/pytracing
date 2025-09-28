from math import tan

import numpy as np
from tqdm.std import tqdm

from collisions import intersect
from math_utils import norm
from models import Ray, Sphere


class Camera:
    def __init__(self, width, height, pos=np.zeros(3), dir=np.array([0.0, 0.0, 1.0]), fov=60, samples=4):
        self.pos = pos
        self.dir = dir
        self.fov = fov
        self.width = width
        self.height = height
        self.samples = samples

    def render(self, objects, sun):
        framebuffer = np.zeros((self.height, self.width, 3))
        aspect_ratio = self.width / float(self.height)
        scale = np.tan(np.deg2rad(self.fov * 0.5))

        for y_pixel in tqdm(range(self.height)):
            for x_pixel in range(self.width):

                x = (2 * (x_pixel + 0.5) / float(self.width) - 1) * aspect_ratio * scale
                y = (1 - 2 * (y_pixel + 0.5) / float(self.height)) * scale
                direction = np.array([x, y, -1])
                direction = direction / np.linalg.norm(direction)
                ray = Ray(self.pos, direction)

                t, hit_obj = self.test_collision(ray, objects)
                if hit_obj is None:  # background
                    full_color = np.array([0.5, 0.8, 1.0])
                    framebuffer[y_pixel][x_pixel] = ((1 - full_color) * (np.array([y_pixel, y_pixel, 0])) /
                                                     float(self.height) + full_color)
                else:
                    # check shadow
                    hit_point = ray.orig + ray.dir * t
                    hit_point_normal = norm(hit_point - hit_obj.pos)
                    light_dir = sun.pos - hit_point
                    light_dir = norm(light_dir)
                    light_ray = Ray(hit_point + light_dir * 0.00001,
                                    light_dir)  # add some bias to avoid self-intersection

                    lt, light_collision_obj = self.test_collision(light_ray, objects)
                    if light_collision_obj is not None:
                        framebuffer[y_pixel][x_pixel] = np.zeros(3)
                    else:  # add smooth lighting
                        intensity = max(0, np.dot(light_dir, hit_point_normal))
                        framebuffer[y_pixel][x_pixel] = hit_obj.color * intensity

        return framebuffer

    def test_collision(self, ray, objects):
        closest = float('inf')
        hit_obj = None
        for obj in objects:
            if isinstance(obj, Sphere):
                t = intersect(ray, obj)
                if t is not None and t < closest:
                    closest = t
                    hit_obj = obj
        return closest, hit_obj
