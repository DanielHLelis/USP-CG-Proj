# CG 2024.1 - Assignment 2
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

from typing import Optional, Callable, Any

import glm
import numpy as np

from model import Model
from camera import Camera

from .entity import Entity
from light_source import LightSource


class GlowingEntity(Entity):
    light_source: LightSource

    def __init__(
        self,
        model: Model,
        position=glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        angle_x: float = 0.0,
        angle_y: float = 0.0,
        angle_z: float = 0.0,
        light_source: Optional[LightSource] = None,
        animator: Optional[Callable[[Any, float], None]] = None,
        **kwargs,
    ):
        super().__init__(
            model,
            **kwargs,
        )

        self.position = position
        self.scale = scale
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z

        if light_source is None:
            light_source = LightSource(
                position=np.array(position),
            )

        self.light_source = light_source

        self.light_sources = [self.light_source]
        self.animator = animator

    def update(self, dt: float, camera: Camera):
        self.light_source.position = np.array(self.position)
        if self.animator is not None:
            self.animator(self, dt)
