from typing import Any

import numpy as np
import OpenGL.GL as gl
import glm

from entity import Entity


class Camera:
    position: glm.vec3
    target: glm.vec3
    fov: float
    up: glm.vec3

    def __init__(
        self,
        position=glm.vec3(0.0, 0.0, 5.0),
        target=glm.vec3(0.0, 0.0, 0.0),
        fov=45.0,
        up=glm.vec3(0.0, 1.0, 0.0),
    ):
        self.position = position
        self.target = target
        self.fov = fov
        self.up = up

    def view_matrix(self):
        view = glm.lookAt(self.position, self.target, self.up)
        return np.array(view).T

    def projection_matrix(self, aspect_ratio, near=0.1, far=100.0):
        projection = glm.perspective(glm.radians(self.fov), aspect_ratio, near, far)
        return np.array(projection).T

    def update(self, dt):
        pass


class Renderer:

    program: Any
    model_loc: Any
    view_loc: Any
    projection_loc: Any

    def __init__(
        self,
        program: Any,
        model_loc: Any,
        view_loc: Any,
        projection_loc: Any,
    ) -> None:
        self.program = program
        self.model_loc = model_loc
        self.view_loc = view_loc
        self.projection_loc = projection_loc

    def _model_matrix(self, entity: Entity) -> np.ndarray:

        rad_angle = np.radians(entity.angle)

        mat = glm.mat4(1.0)
        mat = glm.translate(mat, entity.position)
        mat = glm.rotate(
            mat,
            rad_angle,
            entity.rotation,
        )
        mat = glm.scale(
            mat,
            entity.scale,
        )

        return np.array(mat, dtype=np.float32).T

    def render(self, entity: Entity) -> None:
        model = entity.model

        gl.glBindTexture(gl.GL_TEXTURE_2D, model.texture_id)
