from typing import Any

import numpy as np
import OpenGL.GL as gl
import glm

from entity import Entity
from camera import Camera


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

    def _view_matrix(self, camera: Camera) -> np.ndarray:
        view = glm.lookAt(camera.position, camera.target, camera.up)
        return np.array(view).T

    def _projection_matrix(self, camera: Camera):
        projection = glm.perspective(glm.radians(camera.fov), camera.aspect_ratio, camera.near, camera.far)
        return np.array(projection).T

    def setup_camera(self, camera):
        view = self._view_matrix(camera)
        projection = self._projection_matrix(camera)

        gl.glUniformMatrix4fv(self.view_loc, 1, gl.GL_TRUE, view)
        gl.glUniformMatrix4fv(self.projection_loc, 1, gl.GL_TRUE, projection)

    def render(self, entity: Entity) -> None:
        model = entity.model

        mat = self._model_matrix(entity)
        gl.glUniformMatrix4fv(self.model_loc, 1, gl.GL_TRUE, mat)

        gl.glBindTexture(gl.GL_TEXTURE_2D, model.texture_id)
        gl.glDrawArrays(model.draw_mode, model.offset, len(model.vertices))
