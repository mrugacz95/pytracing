import numpy as np
from matplotlib import pyplot as plt

from camera import Camera
from hittable import Sphere
from material import Lambertian, NormalColorMaterial, SharpShadowMaterial
from models import Sun


def main():
    width = 580
    height = 420
    camera = Camera(width=width, height=height, pos=np.array([0.0, 0.0, 0.0]), fov=75)

    objects = []

    sun = Sun(pos=np.array([50, 50, 50]))

    sphere1 = Sphere(pos=np.array([0, 0, -1]), radius=0.5, material=SharpShadowMaterial(
                        color=np.array([1.0, 1.0, 0.0]),
                        sun=sun,
                        objects=objects))



    ground = Sphere(pos=np.array([0, -100.5, -1]), radius=100.0,
                    material=SharpShadowMaterial(
                        color=np.array([0.0, 0.5, 0.1]),
                        sun=sun,
                        objects=objects))

    objects.append(sphere1)
    objects.append(ground)

    img = camera.render(objects, sun)

    plt.imshow(img)
    # plt.show()

    plt.savefig('test.png')


if __name__ == '__main__':
    main()
