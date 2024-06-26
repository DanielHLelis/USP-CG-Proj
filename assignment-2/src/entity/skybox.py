# CG 2024.1 - Assignment 1
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

import glm

from model import Model
from camera import Camera

from .entity import Entity


class Skybox(Entity):

    def __init__(
        self,
        model: Model,
    ):
        super().__init__(
            model,
            scale=glm.vec3(5000.0, 5000.0, 5000.0),
            ignore_lighting=True,
        )

    def update(self, dt: float, camera: Camera):
        self.position = camera.position
