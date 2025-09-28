from abc import ABC, abstractmethod


class Material(ABC):
    @abstractmethod
    def scatter(self, ray):
        pass

class NormalColorMaterial(Material):
    def scatter(self, ray, hit_record):


