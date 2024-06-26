# CG 2024.1 - Assignment 2
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

from typing import Optional, Callable, List, Any

import OpenGL.GL as gl
import glm


from camera import Camera
from model import Model

from light_source import LightSource


class Entity:
    model: Model
    position: glm.vec3
    scale: glm.vec3
    angle_x: float
    angle_y: float
    angle_z: float

    visible: bool  # Whether to draw the entity or not

    light_sources: List[LightSource]

    ignore_lighting: bool

    def __init__(
        self,
        model: Model,
        position: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        angle_x: float = 0,  # pitch
        angle_y: float = 0,  # yaw
        angle_z: float = 0,  # roll
        visible: bool = True,
        draw_mode: int = gl.GL_TRIANGLES,
        light_sources: List[LightSource] = [],
        ignore_lighting: bool = False,
    ):
        self.model = model
        self.position = position
        self.scale = scale
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
        self.visible = visible
        self.draw_mode = draw_mode
        self.light_sources = light_sources
        self.ignore_lighting = ignore_lighting

    def update(self, dt: float, camera: Camera):
        # By default, do nothing
        pass

    def key_handler(self) -> Optional[Callable[[Any, int, int, int, int], None]]:
        pass

    def cursor_handler(
        self,
    ) -> Optional[Callable[[Any, float, float, float, float], None]]:
        pass

    @property
    def pitch(self) -> float:
        return self.angle_x

    @property
    def yaw(self) -> float:
        return self.angle_y

    @property
    def roll(self) -> float:
        return self.angle_z
