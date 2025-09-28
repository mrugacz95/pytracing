import numpy as np
from matplotlib import pyplot as plt

from camera import Camera
from hittable import Sphere
from material import Lambertian, NormalColorMaterial, SharpShadowMaterial, Metal
from models import Sun


def main():
    width = 580
    height = 420
    camera = Camera(width=width, height=height, pos=np.array([0.0, 0.0, 1.0]), fov=60)

    material_left = Metal(albedo=np.array([0.8, 0.8, 0.8]))
    material_center = Lambertian(albedo=np.array([0.1, 0.2, 0.5]))
    material_right = Metal(albedo=np.array([0.8, 0.6, 0.2]))
    material_ground = Lambertian(albedo=np.array([0.8, 0.8, 0.0]))

    sphere_left = Sphere(pos=np.array([-1.0, 0, -1]), radius=0.5, material=material_left)
    sphere_center = Sphere(pos=np.array([0, 0, -1.2]), radius=0.5, material=material_center)
    sphere_right = Sphere(pos=np.array([1.0, 0, -1]), radius=0.5, material=material_right)

    ground = Sphere(pos=np.array([0, -100.5, -1]), radius=100.0, material=material_ground)

    objects = [sphere_left, sphere_center, sphere_right, ground]

    img = camera.render(objects)

    plt.imshow(img)
    # plt.show()

    plt.savefig('test.png')


if __name__ == '__main__':
    main()
