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
        )

    def update(self, dt: float, camera: Camera):
        self.position = camera.position
