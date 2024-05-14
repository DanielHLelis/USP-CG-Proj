from typing import Optional, Callable, Any

import glm
import glfw

from model import Model
from camera import Camera

from .entity import Entity


class OkuuFumo(Entity):

    def __init__(
        self,
        model: Model,
        position=glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        rotation: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        angle: float = 0.0,
        rotation_speed: float = 180.0,
    ):
        super().__init__(
            model,
        )

        self.position = position
        self.rotation_speed = rotation_speed
        self.rotation = rotation
        self.angle = angle
        self.scale = scale

    def update(self, dt: float, camera: Camera):
        self.angle += self.rotation_speed * dt

    def key_handler(self) -> Optional[Callable[[Any, int, int, int, int], None]]:
        def handler(win, key, scancode, action, mods):
            if key == glfw.KEY_LEFT and action == glfw.PRESS:
                self.rotation_speed += -90.0
            elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
                self.rotation_speed += 90.0
            elif key == glfw.KEY_UP and action == glfw.PRESS:
                self.scale += glm.vec3(0.1, 0.1, 0.1)
            elif key == glfw.KEY_DOWN and action == glfw.PRESS:
                self.scale -= glm.vec3(0.1, 0.1, 0.1)

        return handler
