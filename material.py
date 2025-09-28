from abc import ABC, abstractmethod

import numpy as np
from scipy.stats import uniform_direction

from camera import Camera
from math_utils import norm, random_on_hemisphere, near_zero, reflect, refract
from models import Ray


class Material(ABC):
    @abstractmethod
    def scatter(self, ray, hit_record):
        pass


class NormalColorMaterial(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, hit_record):
        return False, None, (hit_record.normal + 1) / 2.0


class SharpShadowMaterial(Material):
    def __init__(self, color, sun, objects):
        self.color = color
        self.sun = sun
        self.objects = objects

    def scatter(self, ray, hit_record):
        light_dir = self.sun.pos - hit_record.p
        light_dir = norm(light_dir)
        light_ray = Ray(hit_record.p, light_dir)

        closest, hit_obj = Camera.test_collision(light_ray, self.objects)
        if hit_obj is not None:
            return False, None, np.zeros(3)  # black in shadow

        intensity = max(0, np.dot(light_dir, hit_record.normal))
        return False, None, self.color * intensity


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, hit_record):
        scatter_direction = hit_record.normal + random_on_hemisphere(hit_record.normal)

        if near_zero(scatter_direction):
            scatter_direction = hit_record.normal

        scattered = Ray(hit_record.p, norm(scatter_direction))
        attenuation = self.albedo

        if np.random.rand() < 0.5:
            return False, None, attenuation
        return True, scattered, attenuation


class Metal(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, hit_record):
        reflected = reflect(ray.dir, hit_record.normal)
        scattered = Ray(hit_record.p, reflected)
        attenuation = self.albedo
        return True, scattered, attenuation


class Dielectric(Material):
    def __init__(self, refraction):
        self.refraction = refraction  # Index of Refraction

    def scatter(self, ray, hit_record):
        attenuation = np.ones(3)
        ri = (1.0 / self.refraction) if hit_record.front_face else self.refraction
        unit_direction = norm(ray.dir)

        cos_theta = min(np.dot(-unit_direction, hit_record.normal), 1.0)
        sin_theta = np.sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = ri * sin_theta > 1.0

        if cannot_refract or self.reflectance(cos_theta, ri) > np.random.rand():
            direction = reflect(unit_direction, hit_record.normal)
        else:
            direction = refract(unit_direction, hit_record.normal, ri)

        scattered = Ray(hit_record.p, direction)
        return True, scattered, attenuation

    @staticmethod
    def reflectance(cosine, refraction_index):
        # Use Schlick's approximation for reflectance.
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * np.pow((1 - cosine), 5)
