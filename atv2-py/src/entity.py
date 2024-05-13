from typing import Optional, Callable, Any

import numpy as np
import OpenGL.GL as gl
import glm


class Model:
    vertices: np.ndarray
    texture_coords: np.ndarray
    texture_id: int
    draw_mode: int

    offset: int
    texture_offset: int

    def __init__(
        self,
        vertices: np.ndarray,
        texture_coords: np.ndarray,
        texture_id: int,
        draw_mode=gl.GL_TRIANGLES,
    ):
        self.vertices = vertices.astype(np.float32)
        self.texture_coords = texture_coords.astype(np.float32)
        self.texture_id = texture_id
        self.draw_mode = draw_mode
        self.offset = 0
        self.texture_offset = 0


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
        rotation: glm.vec3 = glm.vec3(1.0, 0.0, 0.0),
        angle: float = 0.0,
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
