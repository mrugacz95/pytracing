import numpy as np
from joblib import Parallel, delayed
from tqdm_joblib import tqdm_joblib

from math_utils import sample_square
from models import Ray


class Camera:
    MAX_DEPTH = 50

    def __init__(self, width, height, pos=np.zeros(3), fov=60, samples=20):
        self.pos = pos
        self.fov = fov
        self.width = width
        self.height = height
        self.samples = samples

    def render(self, objects):
        framebuffer = np.zeros((self.height, self.width, 3))
        aspect_ratio = self.width / float(self.height)
        scale = np.tan(np.deg2rad(self.fov * 0.5))

        def render_row(y_pixel):

            row = np.zeros((self.width, 3))

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
                    color += self.ray_color(ray, objects, depth=self.MAX_DEPTH)

                color /= self.samples

                row[x_pixel] = color

            return row

        with tqdm_joblib(total=self.height):
            framebuffer[:] = Parallel(n_jobs=8)(
                delayed(render_row)(y_pixel) for y_pixel in range(self.height)
            )

        framebuffer = np.sqrt(framebuffer)  # gamma correction

        return framebuffer

    def ray_color(self, ray, objects, depth):
        if depth <= 0:
            return np.zeros(3)

        t, hit_obj = self.test_collision(ray, objects)
        if hit_obj is not None:
            (scattered, new_ray, attenuation) = hit_obj.material.scatter(ray, hit_obj)
            if scattered:
                return attenuation * self.ray_color(new_ray, objects, depth - 1)
            return attenuation  # no scattering, return color directly?

        full_color = np.array([0.5, 0.8, 1.0])
        return (1 - full_color) * (np.array([ray.dir[1], ray.dir[1], 0])) + full_color

    @staticmethod
    def test_collision(ray, objects):
        closest = float('inf')
        hit_obj = None
        for obj in objects:
            hit_record = obj.hit(ray, 0.001, closest)
            if hit_record is not None and hit_record.t < closest:
                closest = hit_record.t
                hit_obj = hit_record
        return closest, hit_obj
