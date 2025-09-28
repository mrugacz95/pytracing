from abc import ABC, abstractmethod
from scipy.stats import uniform_direction

from math_utils import norm, random_on_hemisphere, near_zero
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


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, hit_record):
        scatter_direction = hit_record.normal + random_on_hemisphere(hit_record.normal)

        if near_zero(scatter_direction):
            scatter_direction = hit_record.normal

        scattered = Ray(hit_record.p, norm(scatter_direction))
        attenuation = self.albedo
        return True, scattered, attenuation
