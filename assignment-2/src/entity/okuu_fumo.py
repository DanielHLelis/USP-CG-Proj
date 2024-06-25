# CG 2024.1 - Assignment 1
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

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
        angle_x: float = 0.0,
        angle_y: float = 0.0,
        angle_z: float = 0.0,
        rotation_speed: float = 180.0,
        handle_events: bool = True,
    ):
        super().__init__(
            model,
        )

        self.position = position
        self.rotation_speed = rotation_speed
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.scale = scale
        self.handle_events = handle_events

    def update(self, dt: float, camera: Camera):
        self.angle_y += self.rotation_speed * dt
        self.angle_y %= 360

    def key_handler(self) -> Optional[Callable[[Any, int, int, int, int], None]]:
        if not self.handle_events:
            return None

        def handler(win, key, scancode, action, mods):
            if key == glfw.KEY_LEFT and action == glfw.PRESS:
                self.rotation_speed += -90.0
            elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
                self.rotation_speed += 90.0
            elif key == glfw.KEY_UP and action == glfw.PRESS:
                self.scale *= 1.25
            elif key == glfw.KEY_DOWN and action == glfw.PRESS:
                self.scale /= 1.25

        return handler
