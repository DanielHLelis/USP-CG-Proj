from typing import Optional, Callable, Any

import OpenGL.GL as gl
import glm

from model import Model


class Entity:
    model: Model
    position: glm.vec3
    scale: glm.vec3
    rotation: glm.vec3
    angle: float

    visible: bool  # Whether to draw the entity or not

    def __init__(
        self,
        model: Model,
        position: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        rotation: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        angle: float = 90,
        visible: bool = True,
        draw_mode: int = gl.GL_TRIANGLES,
    ):
        self.model = model
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.angle = angle
        self.visible = visible
        self.draw_mode = draw_mode

    def update(self, dt: int):
        # By default, do nothing
        pass

    def key_handler(self) -> Optional[Callable[[Any, int, int, int, int], None]]:
        pass

    def cursor_handler(
        self,
    ) -> Optional[Callable[[Any, float, float, float, float], None]]:
        pass
