from math import tan

import numpy as np
from tqdm.std import tqdm

from collisions import intersect
from math_utils import norm, sample_square
from models import Ray, Sphere


class Camera:
    def __init__(self, width, height, pos=np.zeros(3), fov=60, samples=10):
        self.pos = pos
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

                color = np.zeros(3, dtype=float)

                for samples in range(self.samples):
                    x = (2 * (x_pixel + 0.5) / float(self.width) - 1) * aspect_ratio * scale
                    y = (1 - 2 * (y_pixel + 0.5) / float(self.height)) * scale

                    pixel_width = 2.0 * aspect_ratio * scale / self.width
                    pixel_height = 2.0 * scale / self.height

                    dx, dy = sample_square()
                    x += dx * pixel_width
                    y += dy * pixel_height

                    direction = np.array([x, y, -1])
                    direction = direction / np.linalg.norm(direction)


                    ray = Ray(self.pos, direction)
                    color += self.ray_color(ray, sun, objects, 2)

                color /= self.samples

                framebuffer[y_pixel][x_pixel] = color

        return framebuffer

    def ray_color(self, ray, sun, objects, depth):
        t, hit_obj = self.test_collision(ray, objects)
        if hit_obj is None:  # background
            full_color = np.array([0.5, 0.8, 1.0])
            return (1 - full_color) * (np.array([ray.dir[1], ray.dir[1], 0])) + full_color
        else:
            # check shadow
            hit_point = ray.orig + ray.dir * t
            hit_point_normal = norm(hit_point - hit_obj.pos)
            light_dir = sun.pos - hit_point
            light_dir = norm(light_dir)
            light_ray = Ray(hit_point + light_dir * 0.00001, light_dir)  # add some bias to avoid self-intersection

            lt, light_collision_obj = self.test_collision(light_ray, objects)
            if light_collision_obj is not None:
                return np.zeros(3)
            else:  # add smooth lighting
                intensity = max(0, np.dot(light_dir, hit_point_normal))
                return hit_obj.color * intensity

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
